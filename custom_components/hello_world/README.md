# Hello World Home Assistant Component

Een simpele "Hello World" custom component voor Home Assistant.

## Installatie

1. Kopieer de `hello_world` folder naar je `custom_components` directory:
   ```
   <config_dir>/custom_components/hello_world/
   ```

2. Voeg de volgende configuratie toe aan je `configuration.yaml`:
   ```yaml
   hello_world:

   sensor:
     - platform: hello_world
   ```

3. Herstart Home Assistant

## Gebruik

Na het herstarten:
- Check de logs om het "Hello World" bericht te zien
- De sensor `sensor.hello_world` wordt aangemaakt
- De sensor toont de huidige tijd

## Bestanden

- `__init__.py` - Main component setup
- `manifest.json` - Component metadata
- `sensor.py` - Sensor platform implementation
- `README.md` - Deze documentatie

## Uitbreidingen

Je kunt dit component uitbreiden met:
- Switches
- Binary sensors
- Services
- Config flow (UI configuratie)
- Events en automations
