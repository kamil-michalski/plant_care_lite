"""Constants for Plant Care Lite integration."""

DOMAIN = "plant_care_lite"

SUMMER_MONTHS = range(4, 10)  # April – September

PLANT_GROUPS: dict[str, dict[str, int]] = {
    "succulent": {
        "summer_days": 14,
        "winter_days": 30,
    },
    "drought_tolerant": {
        "summer_days": 10,
        "winter_days": 21,
    },
    "tropical": {
        "summer_days": 7,
        "winter_days": 14,
    },
    "climbing": {
        "summer_days": 7,
        "winter_days": 14,
    },
    "fern": {
        "summer_days": 3,
        "winter_days": 5,
    },
}

CONF_PLANT_NAME = "name"
CONF_PLANT_GROUP = "group"

STORAGE_VERSION = 1
STORAGE_KEY_PREFIX = "plant_care_lite_"

STATUS_OK = "ok"
STATUS_WATER = "water"

SENSOR_WATERING_INTERVAL = "watering_interval"
SENSOR_LAST_WATERED = "last_watered"
SENSOR_STATUS = "status"
BUTTON_WATER_NOW = "water_now"
