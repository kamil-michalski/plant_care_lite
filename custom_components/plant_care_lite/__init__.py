"""Plant Care Lite – Home Assistant custom integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_PLANT_GROUP, CONF_PLANT_NAME, DOMAIN
from .coordinator import PlantCareCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Plant Care Lite from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = PlantCareCoordinator(
        hass=hass,
        entry_id=entry.entry_id,
        plant_name=entry.data[CONF_PLANT_NAME],
        plant_group=entry.data[CONF_PLANT_GROUP],
    )

    await coordinator.async_load()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator: PlantCareCoordinator = hass.data[DOMAIN].get(entry.entry_id)

    if coordinator:
        await coordinator.async_unload()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        hass.data.pop(f"{DOMAIN}_entities_{entry.entry_id}", None)

    return unload_ok
