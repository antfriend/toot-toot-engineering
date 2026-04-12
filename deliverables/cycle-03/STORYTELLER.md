---
cycle: 03
role: Storyteller
---

# Cycle 03 Storyteller

## The experience

An Agent 32 device is a device that knows things. It carries its knowledge in a TTDB file baked into its own flash — not pulled from a network, not fetched from a card you might forget to insert. It's *always there*, because it's *part of the device*.

The K10 TTDB Navigator expresses this: power it on, hear the two-note toot that says "I'm ready," and see the first record of your knowledge graph appear on screen. Tap the right side to move forward through ideas. Tap the left side to go back. Tilt the device when your hands are full. Hear a crisp beep confirm each step, and a two-note chime when you wrap around and the list begins again.

The UI is not decorated. It shows the TTDB name, a window of nearby records with the current one highlighted, the record ID, and a preview of the body text. A small status line confirms the filesystem is mounted and the file was found. Two dark rectangles at the bottom of the screen mark the touch zones. Simple, intentional, enough.

This device doesn't need a server. It doesn't need Wi-Fi. It needs a TTDB file and someone who wants to navigate it.

## Narrative thread to maintain

The design choice to use LittleFS instead of SD is not just technical — it is a statement of intent. An Agent 32 device whose knowledge lives in embedded flash is a **self-contained artifact**. Like a reference card laminated and kept in a pocket, it is complete, durable, and independent. The SD slot remains available for other purposes (audio, photos, logs). The knowledge is not on the card. The knowledge is in the device.

Keep this framing in the solution: LittleFS is the knowledge layer. SD is optional peripheral storage. They are not interchangeable by accident.
