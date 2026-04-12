// k10_a32_navigator.ino
// A32 TTDB Navigator for UniHiker K10
//
// Reads a TTDB file from LittleFS (embedded flash, not SD card).
// Touch screen zones + buttons A/B + tilt gesture for navigation.
// Interactive sounds: startup melody, nav beep, wrap-around chime.
//
// Deploy the data partition first:
//   pio run --target uploadfs
// This uploads data/ttdb.md to the K10 flash as /ttdb.md.
//
// References:
//   A32-RFC-0001 (Architecture)
//   A32-RFC-0002 (TTDB Storage / LittleFS)
//   A32-RFC-0003 (Agent Loop)
//   TTDB-RFC-0001 (File Format)

#include "unihiker_k10.h"
#include <LittleFS.h>
#include "lvgl.h"

// ---------------------------------------------------------------------------
// Hardware instances
// ---------------------------------------------------------------------------
UNIHIKER_K10 k10;
Music music;

// ---------------------------------------------------------------------------
// Display config
// ---------------------------------------------------------------------------
const uint8_t SCREEN_DIR = 2;  // Portrait

// Portrait pixel dimensions (240 wide x 280 tall)
const int16_t SCREEN_W    = 240;
const int16_t SCREEN_H    = 280;
const int16_t SCREEN_MID  = 120;

// Touch zones occupy the bottom strip of the screen
const int16_t TOUCH_Y     = 245;
const int16_t TOUCH_H     = 32;
const int16_t TOUCH_GAP   = 3;

// ---------------------------------------------------------------------------
// Color palette (0xRRGGBB)
// ---------------------------------------------------------------------------
const uint32_t C_BG      = 0x000000;
const uint32_t C_TEXT    = 0x00FF66;
const uint32_t C_MUTED   = 0x2E7D32;
const uint32_t C_ACCENT  = 0x00E676;
const uint32_t C_SELECT  = 0xCCFF90;
const uint32_t C_TOUCH   = 0x003300;
const uint32_t C_TOUCH_L = 0x004400;  // highlight on touch zone borders

// ---------------------------------------------------------------------------
// TTDB / storage
// ---------------------------------------------------------------------------
const char* TTDB_PATH = "/ttdb.md";

const uint8_t  MAX_RECORDS    = 24;
const uint16_t MAX_BODY_CHARS = 260;

struct Record {
  String id;
  String title;
  String body;
};

Record   records[MAX_RECORDS];
uint8_t  recordCount  = 0;
int      curIdx       = 0;
String   dbName       = "TTDB";
bool     fsOk         = false;
bool     ttdbOk       = false;
uint32_t ttdbSize     = 0;
String   fsStatus     = "FS: --";
String   fileStatus   = "";

// ---------------------------------------------------------------------------
// Input debounce
// ---------------------------------------------------------------------------
unsigned long lastBtnMs   = 0;
unsigned long lastTiltMs  = 0;
unsigned long lastTouchMs = 0;

const unsigned long BTN_DEBOUNCE_MS   = 220;
const unsigned long TILT_DEBOUNCE_MS  = 260;
const unsigned long TOUCH_DEBOUNCE_MS = 300;

// Touch edge-detection: track previous point to detect new taps
static lv_point_t prevTouchPt = {0, 0};

// ---------------------------------------------------------------------------
// setup()
// ---------------------------------------------------------------------------
void setup() {
  k10.begin();
  playStartupToot();

  k10.initScreen(SCREEN_DIR);
  k10.creatCanvas();

  // Boot splash
  k10.canvas->canvasClear(C_BG);
  k10.canvas->canvasCircle(SCREEN_MID, 110, 28, C_TEXT, C_TEXT, true);
  k10.canvas->canvasText("A32 Boot", 2, C_ACCENT);
  k10.canvas->canvasText("LittleFS...", 4, C_MUTED);
  k10.canvas->updateCanvas();

  // Mount embedded filesystem
  fsOk = LittleFS.begin(true);
  fsStatus = fsOk ? "FS: OK" : "FS: FAIL";

  loadTTDB();
  render();
}

// ---------------------------------------------------------------------------
// loop()
// ---------------------------------------------------------------------------
void loop() {
  handleButtons();
  handleTilt();
  handleTouch();
  delay(12);
}

// ---------------------------------------------------------------------------
// Sound
// ---------------------------------------------------------------------------
void playStartupToot() {
  // Two ascending tones: "ready"
  music.playTone(196, 2000);
  music.playTone(262, 4000);
}

void playNavToot() {
  // Single mid tone: step taken
  music.playTone(330, 1200);
}

void playWrapChime() {
  // Two-note descend/ascend: wrapped around the list
  music.playTone(523, 800);
  music.playTone(392, 1200);
}

// ---------------------------------------------------------------------------
// Input handlers
// ---------------------------------------------------------------------------
void handleButtons() {
  unsigned long now = millis();
  if (now - lastBtnMs < BTN_DEBOUNCE_MS) return;
  if (k10.buttonA->isPressed()) { selectPrev(); lastBtnMs = now; return; }
  if (k10.buttonB->isPressed()) { selectNext(); lastBtnMs = now; }
}

void handleTilt() {
  unsigned long now = millis();
  if (now - lastTiltMs < TILT_DEBOUNCE_MS) return;
  if      (k10.isGesture(TiltLeft))  { selectPrev(); lastTiltMs = now; }
  else if (k10.isGesture(TiltRight)) { selectNext(); lastTiltMs = now; }
}

// Touch: poll the LVGL pointer input device.
// lv_indev_get_point() returns the last registered touch point.
// A new tap is detected when the point changes while inside a touch zone.
void handleTouch() {
  unsigned long now = millis();
  if (now - lastTouchMs < TOUCH_DEBOUNCE_MS) return;

  lv_indev_t* dev = lv_indev_get_next(NULL);
  while (dev != NULL) {
    if (lv_indev_get_type(dev) == LV_INDEV_TYPE_POINTER) {
      lv_point_t pt;
      lv_indev_get_point(dev, &pt);

      // Treat a changed point inside the bottom touch strip as a tap
      bool moved = (pt.x != prevTouchPt.x || pt.y != prevTouchPt.y);
      if (moved && pt.y >= TOUCH_Y && pt.y < (TOUCH_Y + TOUCH_H)) {
        if (pt.x < SCREEN_MID) selectPrev();
        else                   selectNext();
        lastTouchMs = now;
      }
      prevTouchPt = pt;
      break;
    }
    dev = lv_indev_get_next(dev);
  }
}

// ---------------------------------------------------------------------------
// Navigation
// ---------------------------------------------------------------------------
void selectPrev() {
  if (!recordCount) return;
  bool wrap = (curIdx == 0);
  curIdx = (curIdx - 1 + recordCount) % recordCount;
  wrap ? playWrapChime() : playNavToot();
  render();
}

void selectNext() {
  if (!recordCount) return;
  bool wrap = (curIdx == (int)(recordCount - 1));
  curIdx = (curIdx + 1) % recordCount;
  wrap ? playWrapChime() : playNavToot();
  render();
}

// ---------------------------------------------------------------------------
// TTDB loading from LittleFS
// ---------------------------------------------------------------------------
void loadTTDB() {
  recordCount = 0;
  dbName      = "ttdb.md";
  ttdbOk      = false;
  ttdbSize    = 0;
  fileStatus  = "";

  if (!fsOk) {
    dbName = "LittleFS failed";
    addFallbackRecord();
    return;
  }

  File f = LittleFS.open(TTDB_PATH, "r");
  if (!f) {
    dbName     = "TTDB missing";
    fileStatus = "Upload data/ttdb.md";
    addFallbackRecord();
    return;
  }

  ttdbOk   = true;
  ttdbSize = f.size();
  fileStatus = String(ttdbSize) + "B";

  bool   inMmpdb  = false;
  int    cur      = -1;

  while (f.available() && recordCount < MAX_RECORDS) {
    String line = f.readStringUntil('\n');
    line.trim();
    if (line.length() == 0) continue;

    // mmpdb header block
    if (line.startsWith("```mmpdb"))          { inMmpdb = true;  continue; }
    if (line.startsWith("```") && inMmpdb)    { inMmpdb = false; continue; }
    if (inMmpdb && line.startsWith("db_name:")) {
      dbName = line.substring(8);
      dbName.trim();
      dbName.replace("\"", "");
      dbName.replace("'",  "");
      continue;
    }

    if (line.startsWith("---")) continue;

    // Record header
    if (line.startsWith("@LAT")) {
      cur++;
      if (cur >= MAX_RECORDS) break;
      records[cur]       = Record();
      records[cur].id    = extractId(line);
      records[cur].title = records[cur].id;
      records[cur].body  = "";
      recordCount        = cur + 1;
      continue;
    }

    // Title
    if (cur >= 0 && line.startsWith("## ")) {
      records[cur].title = line.substring(3);
      continue;
    }

    // Body text
    if (cur >= 0) appendBody(records[cur].body, line);
  }

  f.close();
  if (recordCount == 0) addFallbackRecord();
}

String extractId(const String& line) {
  int p = line.indexOf(" |");
  return (p > 0) ? line.substring(0, p) : line;
}

void appendBody(String& body, const String& line) {
  if (body.length() >= MAX_BODY_CHARS) return;
  if (body.length() > 0) body += ' ';
  String clean = line;
  clean.replace("**", "");
  clean.replace("*",  "");
  body += clean;
  if (body.length() > MAX_BODY_CHARS) body = body.substring(0, MAX_BODY_CHARS);
}

void addFallbackRecord() {
  recordCount        = 1;
  records[0].id     = "@LAT0.0LON0.0";
  records[0].title  = "No TTDB";
  records[0].body   = "Run: pio run --target uploadfs  to upload data/ttdb.md to flash.";
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------
void render() {
  k10.canvas->canvasClear(C_BG);
  renderHeader();
  renderList();
  renderPreview();
  renderStatus();
  renderTouchZones();
  k10.canvas->updateCanvas();
}

void renderHeader() {
  // DB name at top
  String label = dbName;
  if (label.length() > 24) label = label.substring(0, 24);
  k10.canvas->canvasText(label, 1, C_ACCENT);
}

void renderList() {
  if (recordCount == 0) {
    k10.canvas->canvasText("No records.", 3, C_MUTED);
    return;
  }
  // Show a 5-row window centred on curIdx
  int start = max(0, curIdx - 2);
  int end   = min((int)recordCount, start + 5);
  int row   = 3;
  for (int i = start; i < end; i++) {
    String label = records[i].title;
    if (label.length() > 22) label = label.substring(0, 22);
    if (i == curIdx)
      k10.canvas->canvasText("> " + label, row, C_SELECT);
    else
      k10.canvas->canvasText("  " + label, row, C_TEXT);
    row++;
  }
}

void renderPreview() {
  if (!recordCount) return;
  Record& rec = records[curIdx];

  // Record ID (coordinate)
  String idLine = rec.id;
  if (idLine.length() > 26) idLine = idLine.substring(0, 26);
  k10.canvas->canvasText(idLine, 9, C_MUTED);

  // Body preview (first 80 chars)
  String preview = rec.body;
  if (preview.length() > 80) preview = preview.substring(0, 80) + "...";
  k10.canvas->canvasText(preview, 11, C_TEXT);

  // Position indicator
  String pos = String(curIdx + 1) + "/" + String(recordCount);
  k10.canvas->canvasText(pos, 13, C_MUTED);
}

void renderStatus() {
  // Filesystem and file status on rows 14-15
  k10.canvas->canvasText(fsStatus,   14, fsOk   ? C_MUTED : C_SELECT);
  k10.canvas->canvasText(fileStatus, 15, ttdbOk ? C_MUTED : C_SELECT);
}

void renderTouchZones() {
  // PREV zone (left half, bottom strip)
  k10.canvas->canvasRectangle(
    0, TOUCH_Y,
    SCREEN_MID - TOUCH_GAP, TOUCH_H,
    C_TOUCH_L, C_TOUCH, true
  );
  // NEXT zone (right half, bottom strip)
  k10.canvas->canvasRectangle(
    SCREEN_MID + TOUCH_GAP, TOUCH_Y,
    SCREEN_MID - TOUCH_GAP, TOUCH_H,
    C_TOUCH_L, C_TOUCH, true
  );
  // Labels using pixel-positioned text
  k10.canvas->canvasText("< PREV", 5, TOUCH_Y + 8, C_ACCENT,
                          Canvas::eCNAndENFont16, 1, false);
  k10.canvas->canvasText("NEXT >", SCREEN_MID + 8, TOUCH_Y + 8, C_ACCENT,
                          Canvas::eCNAndENFont16, 1, false);
}
