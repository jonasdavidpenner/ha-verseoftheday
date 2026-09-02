# Icon-Dateien für die Brands-Einreichung

Home Assistant zeigt Integrations-Icons nur an, wenn sie im zentralen Repository
[home-assistant/brands](https://github.com/home-assistant/brands) liegen. Dieses
Verzeichnis enthält die fertig benannten Dateien in genau der dort erwarteten
Struktur.

## So reichst du das Icon ein

1. Forke https://github.com/home-assistant/brands
2. Kopiere den Ordner
   `custom_integrations/youversion_votd/` (mit `icon.png`, `icon@2x.png`,
   `logo.png`, `logo@2x.png`) in den Fork.
3. Öffne einen Pull Request.

Anforderungen (bereits erfüllt):
- `icon.png` = 256×256, `icon@2x.png` = 512×512, PNG mit Transparenz.
- Der Ordnername muss der Domain entsprechen: `youversion_votd`.

Nach dem Merge erscheint das Icon automatisch in Home Assistant und HACS – ein
Update der Integration selbst ist dafür nicht nötig.
