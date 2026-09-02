"""Config Flow für die YouVersion Verse-of-the-Day Integration.

Der App Key ist fest im Code hinterlegt (siehe const.APP_KEY). Der Nutzer
wählt hier nur die Sprache und anschließend die konkrete Bibelübersetzung.
"""

from __future__ import annotations

import logging
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
    CONF_BIBLE_ID,
    CONF_BIBLE_NAME,
    CONF_LANGUAGE,
    DEFAULT_LANGUAGE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class YouVersionConfigFlow(ConfigFlow, domain=DOMAIN):
    """Führt den Nutzer durch Sprach- und Übersetzungsauswahl."""

    VERSION = 1

    def __init__(self) -> None:
        self._bibles: list[dict] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Schritt 1: Sprache wählen."""
        errors: dict[str, str] = {}
        if user_input is not None:
            language = user_input[CONF_LANGUAGE]
            session = async_get_clientsession(self.hass)
            client = YouVersionClient(session, bible_id=0)
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
