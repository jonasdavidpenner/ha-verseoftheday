"""Sensor-Plattform für den Verse of the Day."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import YouVersionConfigEntry
from .const import CONF_BIBLE_NAME, DOMAIN
from .coordinator import YouVersionCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: YouVersionConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Richtet den Sensor aus einem Config Entry ein."""
    coordinator = entry.runtime_data
    async_add_entities([YouVersionVotdSensor(coordinator, entry)])


class YouVersionVotdSensor(CoordinatorEntity[YouVersionCoordinator], SensorEntity):
    """Sensor, dessen Zustand die Vers-Referenz ist; der Text steht in den Attributen.

    Der Sensor ist die Hauptfunktion des Geräts, daher `_attr_name = None`:
    Anzeigename und Entity-ID entsprechen dem Gerätenamen ("Verse of the Day"),
    ohne doppelten Namensteil.

    Hintergrund zum Zustand: Ein Sensor-State ist auf 255 Zeichen begrenzt. Da
    Verse laenger sein koennen, ist der Zustand die Referenz (z. B. "John 3:16"),
    der volle Text liegt im Attribut `text`.
    """

    _attr_has_entity_name = True
    _attr_name = None
    _attr_icon = "mdi:book-cross"

    def __init__(
        self, coordinator: YouVersionCoordinator, entry: YouVersionConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_votd"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Verse of the Day",
            manufacturer="YouVersion",
            model=entry.data.get(CONF_BIBLE_NAME, "Bible"),
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        return data.get("reference")

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        data = self.coordinator.data or {}
        return {
            "text": data.get("content"),
            "reference": data.get("reference"),
            "passage_id": data.get("passage_id"),
        }
