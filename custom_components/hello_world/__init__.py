"""The Hello World integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.discovery import async_load_platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "hello_world"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Hello World component."""
    _LOGGER.info("Hello World component is starting up!")
    
    # Store data in hass.data
    hass.data[DOMAIN] = {
        "message": "Hello from Home Assistant!"
    }
    
    # Log een welkomstbericht
    _LOGGER.warning("🎉 Hello World component succesvol geladen!")
    
    # Load the sensor platform
    if DOMAIN in config:
        await async_load_platform(hass, "sensor", DOMAIN, {}, config)
    
    return True
