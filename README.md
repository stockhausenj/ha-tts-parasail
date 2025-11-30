# Parasail Text-to-Speech for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that provides text-to-speech (TTS) capabilities using Parasail AI's TTS models.

## Features

- **High-Quality Speech Synthesis**: Uses Parasail AI's TTS models
- **Easy Configuration**: Simple setup through Home Assistant UI
- **Privacy-Focused**: Uses Parasail AI's secure API
- **Integration with Home Assistant**: Works seamlessly with Assist, automations, and scripts

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/stockhausenj/ha-tts-parasail`
5. Select "Integration" as the category
6. Click "Add"
7. Find "Parasail Text-to-Speech" in the integration list and click "Download"
8. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/parasail_tts` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Parasail Text-to-Speech"
4. Enter your Parasail API key (get one at https://www.parasail.io/)
5. Select your preferred TTS model
6. Click "Submit"

## Usage

Once configured, the Parasail TTS provider will be available in Home Assistant. You can use it with:

- **Assist Pipeline**: Configure it as your TTS provider in Settings → Voice Assistants
- **Automations**: Use the TTS service in your automation scripts
- **Scripts**: Call the TTS service from your scripts

### Example: Configure in Assist Pipeline

1. Go to Settings → Voice Assistants
2. Create a new assistant or edit an existing one
3. Under "Text-to-speech", select "Parasail TTS"
4. Save your changes

### Example: Use in Automation

```yaml
automation:
  - alias: "Welcome Home"
    trigger:
      - platform: state
        entity_id: person.john
        to: "home"
    action:
      - service: tts.speak
        target:
          entity_id: tts.parasail_tts_parasail_resemble_tts_en
        data:
          message: "Welcome home!"
          media_player_entity_id: media_player.living_room
```

### Example: Use in Script

```yaml
script:
  announce_time:
    sequence:
      - service: tts.speak
        target:
          entity_id: tts.parasail_tts_parasail_resemble_tts_en
        data:
          message: "The current time is {{ now().strftime('%I:%M %p') }}"
          media_player_entity_id: media_player.kitchen
```

## Supported Models

- `parasail-resemble-tts-en` (Default)
  - High-quality English speech synthesis
  - Natural-sounding voice
  - Low latency

## API Key

You need a Parasail API key to use this integration. Get one at:
https://www.parasail.io/

Parasail offers competitive pricing for API access to TTS models.

## Troubleshooting

### "Invalid API key" error
- Verify your API key is correct
- Check that your Parasail account is active
- Ensure you have sufficient API credits

### TTS not working in Assist
- Make sure the integration is properly configured
- Check Home Assistant logs for errors
- Verify your media player is working

### Audio quality issues
- Check your media player volume settings
- Ensure stable internet connection
- Check Home Assistant logs for API errors

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/stockhausenj/ha-tts-parasail/issues).

## License

This project is licensed under the MIT License.

## Credits

- Built using [Parasail AI](https://www.parasail.io/)
- Inspired by the Home Assistant community
