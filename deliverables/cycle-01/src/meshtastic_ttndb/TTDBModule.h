#pragma once

#include <Arduino.h>

// Minimal Meshtastic module stub for TTDB logging.
// Intended to be integrated into the Meshtastic firmware build.

class TTDBModule {
public:
    void setup();
    void onPacketReceived(uint32_t fromId, const char *text);
    void onNodeInfo(uint32_t nodeNum, const char *shortName, const char *longName);

private:
    bool ensureFS();
    void appendLine(const String &line);
};
