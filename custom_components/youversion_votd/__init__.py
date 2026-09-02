"""Die Integration 'Bibelvers des Tages (YouVersion)'."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import YouVersionClient
from .const import CONF_APP_KEY, CONF_BIBLE_ID
from .coordinator import YouVersionCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type YouVersionConfigEntry = ConfigEntry[YouVersionCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: YouVersionConfigEntry
) -> bool:
    """Richtet einen Config Entry ein."""
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
