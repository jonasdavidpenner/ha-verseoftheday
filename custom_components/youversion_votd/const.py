"""Konstanten für die YouVersion Verse-of-the-Day Integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "youversion_votd"

# Konfigurationsschlüssel (im Config Entry gespeichert)
CONF_APP_KEY = "app_key"
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
