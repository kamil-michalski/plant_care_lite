"""Sensor platform for Plant Care Lite integration."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_PLANT_GROUP,
    CONF_PLANT_NAME,
    DOMAIN,
    SENSOR_LAST_WATERED,
    SENSOR_STATUS,
    SENSOR_WATERING_INTERVAL,
    STATUS_OK,
    STATUS_WATER,
)
from .coordinator import PlantCareCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Plant Care Lite sensors for a config entry."""
    coordinator: PlantCareCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        PlantWateringIntervalSensor(coordinator, entry),
        PlantLastWateredSensor(coordinator, entry),
        PlantStatusSensor(coordinator, entry),
    ]

    async_add_entities(entities)

    # Schedule the first status check after entities are registered
    coordinator.schedule_next_check(
        lambda: hass.async_create_task(_refresh_sensors(hass, entry.entry_id))
    )


async def _refresh_sensors(hass: HomeAssistant, entry_id: str) -> None:
    """Ask all sensors for this entry to refresh their state."""
    for entity in hass.data.get(f"{DOMAIN}_entities_{entry_id}", []):
        entity.async_write_ha_state()


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class PlantCareBaseSensor(SensorEntity):
    """Base class for Plant Care Lite sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PlantCareCoordinator,
        entry: ConfigEntry,
        key: str,
    ) -> None:
        self.coordinator = coordinator
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data[CONF_PLANT_NAME],
            manufacturer="Plant Care Lite",
            model=entry.data[CONF_PLANT_GROUP],
        )

    async def async_added_to_hass(self) -> None:
        """Register this entity for manual refresh calls."""
        entity_list = self.hass.data.setdefault(
            f"{DOMAIN}_entities_{self._entry.entry_id}", []
        )
        entity_list.append(self)

    async def async_will_remove_from_hass(self) -> None:
        """Deregister this entity."""
        entity_list = self.hass.data.get(
            f"{DOMAIN}_entities_{self._entry.entry_id}", []
        )
        if self in entity_list:
            entity_list.remove(self)


# ---------------------------------------------------------------------------
# Watering interval sensor
# ---------------------------------------------------------------------------

class PlantWateringIntervalSensor(PlantCareBaseSensor):
    """Shows the current recommended watering interval in days."""

    _attr_icon = "mdi:calendar-clock"
    _attr_native_unit_of_measurement = "d"
    _attr_translation_key = SENSOR_WATERING_INTERVAL

    def __init__(self, coordinator: PlantCareCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, SENSOR_WATERING_INTERVAL)

    @property
    def native_value(self) -> int:
        """Return the current interval in days."""
        return self.coordinator.get_interval()


# ---------------------------------------------------------------------------
# Last watered sensor
# ---------------------------------------------------------------------------

class PlantLastWateredSensor(PlantCareBaseSensor):
    """Shows the timestamp of the last watering."""

    _attr_icon = "mdi:water-clock"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_translation_key = SENSOR_LAST_WATERED

    def __init__(self, coordinator: PlantCareCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, SENSOR_LAST_WATERED)

    @property
    def native_value(self) -> datetime | None:
        """Return the last watered timestamp."""
        return self.coordinator.last_watered


# ---------------------------------------------------------------------------
# Status sensor
# ---------------------------------------------------------------------------

class PlantStatusSensor(PlantCareBaseSensor):
    """Shows whether the plant needs watering."""

    _attr_translation_key = SENSOR_STATUS

    def __init__(self, coordinator: PlantCareCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry, SENSOR_STATUS)

    @property
    def native_value(self) -> str:
        """Return 'ok' or 'water'."""
        return self.coordinator.get_status()

    @property
    def icon(self) -> str:
        """Return icon based on status."""
        if self.coordinator.get_status() == STATUS_OK:
            return "mdi:check-circle"
        return "mdi:water-alert"
