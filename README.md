# Bibelvers des Tages (YouVersion) – Home Assistant Integration

Zeigt den täglichen Bibelvers der [YouVersion Platform API](https://developers.youversion.com/)
als Sensor **und** als eigene, hübsch formatierte Lovelace-Karte an – in der
Bibelübersetzung deiner Wahl.

## Funktionen

- Sensor mit
  - **Zustand:** die Referenz (z. B. `Matthäus 6:34`)
  - **Attributen:** `text` (voller Verstext), `reference`, `passage_id`
- **Eigene Karte** `custom:votd-card` – wird von der Integration automatisch
  bereitgestellt und registriert (keine manuelle Ressource nötig)
- Einrichtung über die Oberfläche: nur Sprache und Übersetzung wählen
- App Key ist fest im Code hinterlegt – Nutzer brauchen keinen eigenen Key

## Vor der Installation: App Key eintragen

Diese Integration hat den YouVersion App Key **fest verdrahtet**. Trag deinen
Key in `custom_components/youversion_votd/const.py` ein:

```python
APP_KEY = "HIER_DEINEN_APP_KEY_EINTRAGEN"
```

Den Key bekommst du auf [platform.youversion.com](https://platform.youversion.com)
(App anlegen). Akzeptiere dort außerdem die **Lizenz** der Übersetzung(en), die
du anbieten willst – nur lizenzierte Bibeln erscheinen in der Auswahl.

> Hinweis: In einem öffentlichen Repository ist der Key für alle sichtbar. Für
> den nicht-kommerziellen Gebrauch ist das laut YouVersion zulässig; bei
> Missbrauch kann der Key jedoch rate-limitiert werden.

## Installation über HACS

1. HACS → Drei-Punkte-Menü → **Benutzerdefinierte Repositories**.
2. URL dieses Repositories eintragen, Kategorie **Integration**, hinzufügen.
3. „Bibelvers des Tages" suchen und herunterladen.
4. Home Assistant neu starten.
5. **Einstellungen → Geräte & Dienste → Integration hinzufügen** → „Bibelvers des Tages".

Nach dem Neustart steht die Karte automatisch zur Verfügung (sie taucht auch im
Karten-Auswahldialog unter „Bibelvers des Tages" auf).

## Die Karte verwenden

Minimal:

```yaml
type: custom:votd-card
entity: sensor.bibelvers_des_tages_verse_of_the_day
```

Mit eigenem Titel:

```yaml
type: custom:votd-card
entity: sensor.bibelvers_des_tages_verse_of_the_day
title: Vers des Tages
```

Die Karte zeigt den Verstext in Serifenschrift mit farblichem Akzentbalken und
die Referenz kursiv darunter. Sie passt sich automatisch an helle und dunkle
Themes an.

## Alternative: Markdown-Karte

Falls du lieber ohne die eigene Karte arbeitest:

```yaml
type: markdown
content: >
  {{ state_attr('sensor.bibelvers_des_tages_verse_of_the_day', 'text') }}

  *— {{ state_attr('sensor.bibelvers_des_tages_verse_of_the_day', 'reference') }}*
```

## Hinweise

- Der Vers wechselt einmal täglich (nach lokaler Zeit von Home Assistant).
- Die Integration fragt die API stündlich ab, um Tageswechsel und Neustarts
  abzudecken.

## Lizenz

MIT – siehe [LICENSE](LICENSE). Bibeltexte unterliegen den jeweiligen Lizenzen
der Verlage bzw. von YouVersion.
