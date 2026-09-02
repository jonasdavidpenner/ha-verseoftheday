"""DataUpdateCoordinator für den Vers des Tages."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import YouVersionClient, YouVersionError
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class YouVersionCoordinator(DataUpdateCoordinator[dict]):
    """Koordiniert den täglichen Abruf des Verses des Tages."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: YouVersionClient,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
            config_entry=entry,
        )
        self._client = client

    async def _async_update_data(self) -> dict:
        # Lokale Zeit von Home Assistant nutzen, damit der Tageswechsel passt.
        day_of_year = dt_util.now().timetuple().tm_yday
        try:
            return await self._client.async_get_verse_of_the_day(day_of_year)
        except YouVersionError as err:
            raise UpdateFailed(str(err)) from err
