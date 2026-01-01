"""Hello World sensor platform."""
import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "hello_world"


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Hello World sensor platform."""
    _LOGGER.info("Setting up Hello World sensor platform")
    
    # Voeg de sensor toe
    async_add_entities([HelloWorldSensor()], True)


class HelloWorldSensor(SensorEntity):
    """Representation of a Hello World sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._attr_name = "Hello World"
        self._attr_unique_id = "hello_world_sensor"
        self._state = "Hello from Home Assistant!"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:hand-wave"

    async def async_update(self):
        """Update the sensor."""
        # Hier kun je logica toevoegen om de state te updaten
        current_time = datetime.now().strftime("%H:%M:%S")
        self._state = f"Hello World! Time: {current_time}"
        _LOGGER.debug(f"Sensor updated: {self._state}")
