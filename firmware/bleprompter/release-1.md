---
layout: firmware_manifest.json
permalink: /firmware/bleprompter/release-1/manifest.json
---
{
  "name": "BlePrompter Release 1",
  "builds": [
    {
      "chipFamily": "ESP32-C3",
      "parts": [
        { "path": "{{ '/assets/firmware/bleprompter/release-1/firmware.bin' | relative_url }}", "offset": 0 }
      ]
    }
  ]
}
