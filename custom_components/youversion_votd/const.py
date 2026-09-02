"""Konstanten für die YouVersion Verse-of-the-Day Integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "youversion_votd"

# ---------------------------------------------------------------------------
# App Key fest verdrahtet.
# Trag hier deinen App Key von platform.youversion.com ein.
# Hinweis: In einem oeffentlichen Repo ist dieser Key fuer alle sichtbar.
# Fuer den nicht-kommerziellen Gebrauch ist das laut YouVersion in Ordnung;
# beachte aber, dass der Key bei Missbrauch rate-limitiert werden koennte.
# ---------------------------------------------------------------------------
APP_KEY = "HIER_DEINEN_APP_KEY_EINTRAGEN"

# Konfigurationsschlüssel (im Config Entry gespeichert)
CONF_BIBLE_ID = "bible_id"
CONF_BIBLE_NAME = "bible_name"
CONF_LANGUAGE = "language"

DEFAULT_LANGUAGE = "de"

# API
API_BASE = "https://api.youversion.com/v1"
APP_KEY_HEADER = "X-YVP-App-Key"

# Frontend / eigene Lovelace-Karte
URL_BASE = f"/{DOMAIN}"
CARD_FILENAME = "votd-card.js"

# Der Vers des Tages wechselt nur um Mitternacht; stündlich prüfen reicht,
# um den Tageswechsel zeitnah abzubilden und Restarts abzufangen.
UPDATE_INTERVAL = timedelta(hours=1)
