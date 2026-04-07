"""Button platform for Plant Care Lite integration."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BUTTON_WATER_NOW,
    CONF_PLANT_GROUP,
    CONF_PLANT_NAME,
    DOMAIN,
)
from .coordinator import PlantCareCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Plant Care Lite button for a config entry."""
    coordinator: PlantCareCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([PlantWaterNowButton(coordinator, entry)])


class PlantWaterNowButton(ButtonEntity):
    """Button to record a watering event."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:watering-can"
    _attr_translation_key = BUTTON_WATER_NOW

    def __init__(
        self,
        coordinator: PlantCareCoordinator,
        entry: ConfigEntry,
    ) -> None:
        self.coordinator = coordinator
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{BUTTON_WATER_NOW}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data[CONF_PLANT_NAME],
            manufacturer="Plant Care Lite",
            model=entry.data[CONF_PLANT_GROUP],
        )

    async def async_press(self) -> None:
        """Handle button press – record watering and refresh sensors."""
        def _refresh():
            self.hass.async_create_task(_refresh_sensors(self.hass, self._entry.entry_id))

        await self.coordinator.async_water_now(_refresh)

        # Also refresh button state itself
        self.async_write_ha_state()


async def _refresh_sensors(hass: HomeAssistant, entry_id: str) -> None:
    """Refresh all sensor entities for this entry."""
    for entity in hass.data.get(f"{DOMAIN}_entities_{entry_id}", []):
        entity.async_write_ha_state()
