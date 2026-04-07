"""Coordinator for Plant Care Lite integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    PLANT_GROUPS,
    STORAGE_KEY_PREFIX,
    STORAGE_VERSION,
    SUMMER_MONTHS,
)

_LOGGER = logging.getLogger(__name__)


class PlantCareCoordinator:
    """Manages state and storage for a single plant entry."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry_id: str,
        plant_name: str,
        plant_group: str,
    ) -> None:
        """Initialize the coordinator."""
        self.hass = hass
        self.entry_id = entry_id
        self.plant_name = plant_name
        self.plant_group = plant_group

        self._store: Store = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY_PREFIX}{entry_id}",
        )
        self._last_watered: datetime | None = None
        self._unsub_scheduled: list = []

    # ------------------------------------------------------------------
    # Setup / teardown
    # ------------------------------------------------------------------

    async def async_load(self) -> None:
        """Load persisted data from storage."""
        data = await self._store.async_load()
        if data and "last_watered" in data:
            try:
                self._last_watered = dt_util.parse_datetime(data["last_watered"])
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "%s: could not parse stored last_watered value: %s",
                    self.plant_name,
                    data.get("last_watered"),
                )
                self._last_watered = None

    async def async_unload(self) -> None:
        """Cancel any scheduled callbacks."""
        for unsub in self._unsub_scheduled:
            unsub()
        self._unsub_scheduled.clear()

    # ------------------------------------------------------------------
    # Season / interval logic
    # ------------------------------------------------------------------

    @staticmethod
    def get_season() -> str:
        """Return 'summer' or 'winter' based on current month."""
        month = dt_util.now().month
        return "summer" if month in SUMMER_MONTHS else "winter"

    def get_interval(self) -> int:
        """Return the current watering interval in days."""
        season = self.get_season()
        key = "summer_days" if season == "summer" else "winter_days"
        return PLANT_GROUPS[self.plant_group][key]

    # ------------------------------------------------------------------
    # Watering state
    # ------------------------------------------------------------------

    @property
    def last_watered(self) -> datetime | None:
        """Return the last watered timestamp."""
        return self._last_watered

    def get_status(self) -> str:
        """Return 'ok' or 'water' based on elapsed days vs interval."""
        from .const import STATUS_OK, STATUS_WATER

        if self._last_watered is None:
            return STATUS_WATER

        now = dt_util.now()
        elapsed = (now - self._last_watered).days
        return STATUS_OK if elapsed < self.get_interval() else STATUS_WATER

    async def async_water_now(self, on_update_callback) -> None:
        """Record current timestamp as last watered and reschedule check."""
        self._last_watered = dt_util.now()
        await self._store.async_save(
            {"last_watered": self._last_watered.isoformat()}
        )
        self._reschedule_check(on_update_callback)
        on_update_callback()

    # ------------------------------------------------------------------
    # Scheduling
    # ------------------------------------------------------------------

    def schedule_next_check(self, on_update_callback) -> None:
        """Schedule or immediately fire the next status check."""
        if self._last_watered is None:
            return

        interval = self.get_interval()
        next_check: datetime = self._last_watered + timedelta(days=interval)
        now = dt_util.now()

        if next_check <= now:
            # Interval already elapsed – fire callback immediately
            on_update_callback()
        else:
            self._schedule_at(next_check, on_update_callback)

    def _reschedule_check(self, on_update_callback) -> None:
        """Cancel existing scheduled check and set a new one."""
        for unsub in self._unsub_scheduled:
            unsub()
        self._unsub_scheduled.clear()
        self.schedule_next_check(on_update_callback)

    def _schedule_at(self, run_at: datetime, callback) -> None:
        """Register a one-shot callback at a specific datetime."""
        from homeassistant.helpers.event import async_track_point_in_time

        def _handle(_now):
            callback()

        unsub = async_track_point_in_time(self.hass, _handle, run_at)
        self._unsub_scheduled.append(unsub)
