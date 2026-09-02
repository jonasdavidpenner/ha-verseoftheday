# Verse of the Day (YouVersion) – Home Assistant Integration

<p align="left"><img src="icons/icon.png" width="120" alt="Verse of the Day icon"></p>

Shows the daily Bible verse from the [YouVersion Platform API](https://developers.youversion.com/)
as a sensor **and** as a dedicated, nicely formatted Lovelace card – in the
Bible translation of your choice.

## Features

- A sensor with
  - **State:** the reference (e.g. `John 3:16`)
  - **Attributes:** `text` (full verse text), `reference`, `passage_id`
- A **custom card** `custom:votd-card` – bundled and auto-registered by the
  integration (no manual resource needed)
- Full UI setup (config flow), available in English and German
- Automatic reauth prompt if the App Key expires

## Requirements

Each user provides their **own App Key**:

1. Register at [platform.youversion.com](https://platform.youversion.com) and
   create an app to obtain an App Key.
2. Accept the **license** for the translation(s) you want in the portal – only
   licensed Bibles show up in the selection.

## Installation via HACS

1. HACS → three-dot menu → **Custom repositories**.
2. Add this repository's URL, category **Integration**.
3. Search for “Verse of the Day” and download it.
4. Restart Home Assistant.
5. **Settings → Devices & services → Add integration** → “Verse of the Day”.
6. Enter your App Key, pick a language and a translation.

After the restart the card is available automatically (it also appears in the
card picker as “Verse of the Day”).

## Using the card

```yaml
type: custom:votd-card
entity: sensor.verse_of_the_day
```

With a custom title:

```yaml
type: custom:votd-card
entity: sensor.verse_of_the_day
title: Daily Verse
```

The card shows the verse text in a serif font with a colored accent bar and the
reference in italics below. It adapts to light and dark themes.

## Alternative: Markdown card

```yaml
type: markdown
content: >
  {{ state_attr('sensor.verse_of_the_day', 'text') }}

  *— {{ state_attr('sensor.verse_of_the_day', 'reference') }}*
```

## Notes

- The verse changes once per day (based on Home Assistant's local time).
- The integration polls the API hourly to cover the day change and restarts.

## Icon

The integration ships an icon (see `icons/`). Home Assistant only shows
integration icons that live in the central
[home-assistant/brands](https://github.com/home-assistant/brands) repository, so
to make the icon appear in the HA UI and in HACS, submit the prepared files in
`brands/custom_integrations/youversion_votd/` as a pull request to that repo. See
`brands/README.md` for the exact steps.

## License

MIT – see [LICENSE](LICENSE). Bible texts are subject to the respective licenses
of the publishers / YouVersion.
