"""Config Flow für die YouVersion Verse-of-the-Day Integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import YouVersionAuthError, YouVersionClient, YouVersionError
from .const import (
    CONF_APP_KEY,
    CONF_BIBLE_ID,
    CONF_BIBLE_NAME,
    CONF_LANGUAGE,
    DEFAULT_LANGUAGE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class YouVersionConfigFlow(ConfigFlow, domain=DOMAIN):
    """Führt den Nutzer durch App-Key-Eingabe und Übersetzungsauswahl."""

    VERSION = 1

    def __init__(self) -> None:
        self._app_key: str | None = None
        self._bibles: list[dict] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Schritt 1: App Key und Sprache."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._app_key = user_input[CONF_APP_KEY]
            language = user_input[CONF_LANGUAGE]
            session = async_get_clientsession(self.hass)
            client = YouVersionClient(session, self._app_key, 0)
            try:
                self._bibles = await client.async_list_bibles(language)
            except YouVersionAuthError:
                errors["base"] = "invalid_auth"
            except YouVersionError:
                errors["base"] = "cannot_connect"
            else:
                if not self._bibles:
                    errors["base"] = "no_bibles"
                else:
                    return await self.async_step_bible()

        schema = vol.Schema(
            {
                vol.Required(CONF_APP_KEY): str,
                vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_bible(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Schritt 2: Übersetzung aus den lizenzierten Bibeln wählen."""
        if user_input is not None:
            bible_id = int(user_input[CONF_BIBLE_ID])
            name = next(
                (b["title"] for b in self._bibles if b["id"] == bible_id),
                str(bible_id),
            )
            await self.async_set_unique_id(str(bible_id))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Bibelvers des Tages ({name})",
                data={
                    CONF_APP_KEY: self._app_key,
                    CONF_BIBLE_ID: bible_id,
                    CONF_BIBLE_NAME: name,
                },
            )

        options = [
            SelectOptionDict(value=str(b["id"]), label=b["title"])
            for b in self._bibles
        ]
        schema = vol.Schema(
            {
                vol.Required(CONF_BIBLE_ID): SelectSelector(
                    SelectSelectorConfig(
                        options=options, mode=SelectSelectorMode.DROPDOWN
                    )
                ),
            }
        )
        return self.async_show_form(step_id="bible", data_schema=schema)

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Startet den Reauth-Flow, wenn der App Key abgelehnt wurde."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Fragt einen neuen App Key ab und aktualisiert den Eintrag."""
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            client = YouVersionClient(
                session, user_input[CONF_APP_KEY], entry.data[CONF_BIBLE_ID]
            )
            try:
                await client.async_validate()
            except YouVersionAuthError:
                errors["base"] = "invalid_auth"
            except YouVersionError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(
                    entry, data_updates={CONF_APP_KEY: user_input[CONF_APP_KEY]}
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_APP_KEY): str}),
            errors=errors,
        )
