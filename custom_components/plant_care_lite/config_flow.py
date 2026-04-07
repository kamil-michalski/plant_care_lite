"""Config flow for Plant Care Lite integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_PLANT_GROUP,
    CONF_PLANT_NAME,
    DOMAIN,
    PLANT_GROUPS,
)


class PlantCareLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Plant Care Lite."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            name: str = user_input.get(CONF_PLANT_NAME, "").strip()
            group: str = user_input.get(CONF_PLANT_GROUP, "")

            if not name:
                errors[CONF_PLANT_NAME] = "name_empty"
            elif self._name_exists(name):
                errors[CONF_PLANT_NAME] = "name_exists"

            if not errors:
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_PLANT_NAME: name,
                        CONF_PLANT_GROUP: group,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_PLANT_NAME): str,
                vol.Required(CONF_PLANT_GROUP): vol.In(list(PLANT_GROUPS.keys())),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    def _name_exists(self, name: str) -> bool:
        """Check if a plant with the given name already exists."""
        existing_entries = self.hass.config_entries.async_entries(DOMAIN)
        return any(
            entry.data.get(CONF_PLANT_NAME, "").lower() == name.lower()
            for entry in existing_entries
        )
