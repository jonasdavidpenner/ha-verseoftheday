"""Die Integration 'Bibelvers des Tages (YouVersion)'."""

from __future__ import annotations

import logging

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import YouVersionClient
from .const import CARD_FILENAME, CONF_APP_KEY, CONF_BIBLE_ID, DOMAIN, URL_BASE
from .coordinator import YouVersionCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type YouVersionConfigEntry = ConfigEntry[YouVersionCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: YouVersionConfigEntry
) -> bool:
    """Richtet einen Config Entry ein."""
    # Eigene Lovelace-Karte einmalig registrieren (unabhängig von Einträgen).
    await _async_register_frontend(hass)

    session = async_get_clientsession(hass)
    client = YouVersionClient(
        session,
        entry.data[CONF_APP_KEY],
        entry.data[CONF_BIBLE_ID],
    )

    coordinator = YouVersionCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: YouVersionConfigEntry
) -> bool:
    """Entlädt einen Config Entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_register_frontend(hass: HomeAssistant) -> None:
    """Stellt die gebündelte Karte bereit und lädt sie im Frontend.

    Wird über ein Flag in hass.data gegen Mehrfachregistrierung abgesichert,
    falls mehrere Übersetzungen (Einträge) eingerichtet sind.
    """
    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get("frontend_registered"):
        return

    card_url = f"{URL_BASE}/{CARD_FILENAME}"
    card_path = hass.config.path(f"custom_components/{DOMAIN}/www/{CARD_FILENAME}")

    await hass.http.async_register_static_paths(
        [StaticPathConfig(card_url, card_path, False)]
    )
    # Lädt die Karte als ES-Modul auf allen Dashboards -> customElements.define.
    add_extra_js_url(hass, card_url)

    domain_data["frontend_registered"] = True
    _LOGGER.debug("YouVersion-Karte registriert unter %s", card_url)
