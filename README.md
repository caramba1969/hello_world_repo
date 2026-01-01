# Hello World - Home Assistant Custom Component

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Een simpele "Hello World" custom component voor Home Assistant.

## Installatie via HACS

1. Open HACS in Home Assistant
2. Klik op de 3 puntjes rechtsboven → "Custom repositories"
3. Voeg deze repository toe: `https://github.com/caramba1969/custom_components`
4. Categorie: "Integration"
5. Zoek naar "Hello World" en installeer
6. Herstart Home Assistant

## Handmatige installatie

1. Kopieer de `custom_components/hello_world` folder naar je Home Assistant `custom_components` directory:
   ```
   <config_dir>/custom_components/hello_world/
   ```
2. Herstart Home Assistant

## Configuratie

Voeg het volgende toe aan je `configuration.yaml`:

```yaml
hello_world:

sensor:
  - platform: hello_world
```

## Gebruik

Na het herstarten:
- Check de logs om het "Hello World" bericht te zien
- De sensor `sensor.hello_world` wordt aangemaakt
- De sensor toont de huidige tijd

## Functies

- ✅ Basis integration setup
- ✅ Sensor platform met real-time klok
- ✅ Logging voorbeelden
- ✅ HACS compatible

## Licentie

MIT License
