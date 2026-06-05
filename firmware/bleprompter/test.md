---
layout: firmware_manifest.json
permalink: /firmware/bleprompter/test/manifest.json
---
{
  "name": "BlePrompter Test",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        { "path": "{{ '/assets/firmware/bleprompter/test/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
