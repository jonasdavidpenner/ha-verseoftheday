# Bibelvers des Tages (YouVersion) – Home Assistant Integration

Zeigt den täglichen Bibelvers der [YouVersion Platform API](https://developers.youversion.com/)
als Sensor in Home Assistant an – in der Bibelübersetzung deiner Wahl.

## Funktionen

- Ein Sensor `sensor.bibelvers_des_tages`
  - **Zustand:** die Referenz (z. B. `Johannes 3:16`)
  - **Attribute:**
    - `text` – der vollständige Verstext
    - `reference` – die menschenlesbare Referenz
    - `passage_id` – die USFM-Kennung (z. B. `JHN.3.16`)
- Einrichtung komplett über die Oberfläche (App Key eingeben, Sprache und
  Übersetzung wählen)
- Automatische Reauth-Abfrage, falls der App Key abläuft

## Voraussetzungen

1. Registriere dich auf [platform.youversion.com](https://platform.youversion.com)
   und lege eine App an, um einen **App Key** zu erhalten.
2. Akzeptiere im Portal die **Lizenz** der Übersetzung(en), die du nutzen willst.
   Nur lizenzierte Bibeln erscheinen in der Auswahl.

## Installation über HACS

1. HACS → Drei-Punkte-Menü → **Benutzerdefinierte Repositories**.
2. URL dieses Repositories eintragen, Kategorie **Integration**, hinzufügen.
3. „Bibelvers des Tages" suchen und herunterladen.
4. Home Assistant neu starten.
5. **Einstellungen → Geräte & Dienste → Integration hinzufügen** → „Bibelvers des Tages".

## Manuelle Installation

Kopiere den Ordner `custom_components/youversion_votd/` in dein
`config/custom_components/`-Verzeichnis und starte Home Assistant neu.

## Anzeige des Verstextes auf dem Dashboard

Da der Sensor-Zustand auf 255 Zeichen begrenzt ist, steht der volle Text im
Attribut `text`. Beispiel mit einer Markdown-Karte:

```yaml
type: markdown
content: >
  ## {{ state_attr('sensor.bibelvers_des_tages', 'reference') }}

  {{ state_attr('sensor.bibelvers_des_tages', 'text') }}
```

## Hinweise

- Der Vers wechselt einmal täglich (nach lokaler Zeit von Home Assistant).
- Die Integration fragt die API stündlich ab, um den Tageswechsel und Neustarts
  abzudecken.

## Lizenz

MIT – siehe [LICENSE](LICENSE). Bibeltexte unterliegen den jeweiligen Lizenzen
der Verlage bzw. von YouVersion.
