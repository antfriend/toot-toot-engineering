#include "TTDBModule.h"
#include <FS.h>
#ifdef ESP32
#include <LittleFS.h>
#endif

static const char *kLogPath = "/ttdb.log";

bool TTDBModule::ensureFS() {
#ifdef ESP32
    return LittleFS.begin(true);
#else
    return false;
#endif
}

void TTDBModule::appendLine(const String &line) {
#ifdef ESP32
    File file = LittleFS.open(kLogPath, FILE_APPEND);
    if (!file) {
        return;
    }
    file.println(line);
    file.close();
#endif
}

void TTDBModule::setup() {
    ensureFS();
}

void TTDBModule::onPacketReceived(uint32_t fromId, const char *text) {
    // Minimal JSONL record. Timestamp is injected by the gateway when synced.
    String line = String("{\"kind\":\"message\",\"from_id\":\"meshtastic:") +
                  String(fromId) +
                  String("\",\"content\":\"") +
                  String(text) +
                  String("\",\"content_type\":\"text\"}");
    appendLine(line);
}

void TTDBModule::onNodeInfo(uint32_t nodeNum, const char *shortName, const char *longName) {
    String line = String("{\"kind\":\"node\",\"id\":\"meshtastic:") +
                  String(nodeNum) +
                  String("\",\"label\":\"") +
                  String(shortName) +
                  String("\",\"roles\":[\"radio_node\"],\"interfaces\":{\"lora\":true}}");
    appendLine(line);
}
