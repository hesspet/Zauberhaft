---
layout: firmware_manifest.json
permalink: /firmware/bleprompter/debug/manifest.json
---
{
  "name": "BlePrompter Debug",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        { "path": "{{ '/assets/firmware/bleprompter/debug/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
