"""Essent Dynamic Pricing sensor platform."""
import logging
from datetime import datetime, timedelta
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "essent_dynamic_pricing"
API_URL = "https://www.essent.nl/api/public/tariffmanagement/dynamic-prices/v1/"
SCAN_INTERVAL = timedelta(hours=1)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Essent Dynamic Pricing sensor from a config entry."""
    
    async def async_update_data():
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(API_URL) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"API returned status {response.status}")
                        return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="essent_dynamic_pricing",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Create sensors
    sensors = [
        EssentCurrentPriceSensor(coordinator, entry),
        EssentNextHourPriceSensor(coordinator, entry),
        EssentTodayAveragePriceSensor(coordinator, entry),
        EssentTodayMinPriceSensor(coordinator, entry),
        EssentTodayMaxPriceSensor(coordinator, entry),
    ]
    
    async_add_entities(sensors, True)


class EssentPriceSensorBase(SensorEntity):
    """Base class for Essent price sensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._entry_id = entry.entry_id
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "€/kWh"
        self._attr_icon = "mdi:cash"
        self._attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()

    def _get_current_hour_tariff(self):
        """Get the tariff for the current hour."""
        if not self.coordinator.data:
            return None
        
        now = datetime.now()
        
        try:
            prices = self.coordinator.data.get("prices", [])
            for day_data in prices:
                if day_data.get("date") == now.strftime("%Y-%m-%d"):
                    electricity = day_data.get("electricity", {})
                    tariffs = electricity.get("tariffs", [])
                    for tariff in tariffs:
                        start = datetime.fromisoformat(tariff["startDateTime"])
                        end = datetime.fromisoformat(tariff["endDateTime"])
                        if start <= now < end:
                            return tariff
        except Exception as e:
            _LOGGER.error(f"Error parsing tariff data: {e}")
        
        return None

    def _get_next_hour_tariff(self):
        """Get the tariff for the next hour."""
        if not self.coordinator.data:
            return None
        
        next_hour = datetime.now() + timedelta(hours=1)
        
        try:
            prices = self.coordinator.data.get("prices", [])
            for day_data in prices:
                if day_data.get("date") == next_hour.strftime("%Y-%m-%d"):
                    electricity = day_data.get("electricity", {})
                    tariffs = electricity.get("tariffs", [])
                    for tariff in tariffs:
                        start = datetime.fromisoformat(tariff["startDateTime"])
                        end = datetime.fromisoformat(tariff["endDateTime"])
                        if start <= next_hour < end:
                            return tariff
        except Exception as e:
            _LOGGER.error(f"Error parsing tariff data: {e}")
        
        return None

    def _get_today_tariffs(self):
        """Get all tariffs for today."""
        if not self.coordinator.data:
            return []
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        try:
            prices = self.coordinator.data.get("prices", [])
            for day_data in prices:
                if day_data.get("date") == today:
                    electricity = day_data.get("electricity", {})
                    return electricity.get("tariffs", [])
        except Exception as e:
            _LOGGER.error(f"Error parsing tariff data: {e}")
        
        return []


class EssentCurrentPriceSensor(EssentPriceSensorBase):
    """Sensor for current electricity price."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Current Price"
        self._attr_unique_id = f"{entry.entry_id}_current_price"

    @property
    def native_value(self):
        """Return the current price."""
        tariff = self._get_current_hour_tariff()
        if tariff:
            return round(tariff.get("totalAmount", 0), 5)
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        tariff = self._get_current_hour_tariff()
        if not tariff:
            return {}
        
        return {
            "total_amount_ex": tariff.get("totalAmountEx"),
            "total_amount_vat": tariff.get("totalAmountVat"),
            "start_time": tariff.get("startDateTime"),
            "end_time": tariff.get("endDateTime"),
            "groups": tariff.get("groups", []),
        }


class EssentNextHourPriceSensor(EssentPriceSensorBase):
    """Sensor for next hour electricity price."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Next Hour Price"
        self._attr_unique_id = f"{entry.entry_id}_next_hour_price"

    @property
    def native_value(self):
        """Return the next hour price."""
        tariff = self._get_next_hour_tariff()
        if tariff:
            return round(tariff.get("totalAmount", 0), 5)
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        tariff = self._get_next_hour_tariff()
        if not tariff:
            return {}
        
        return {
            "start_time": tariff.get("startDateTime"),
            "end_time": tariff.get("endDateTime"),
        }


class EssentTodayAveragePriceSensor(EssentPriceSensorBase):
    """Sensor for today's average electricity price."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Today Average Price"
        self._attr_unique_id = f"{entry.entry_id}_today_average_price"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Return today's average price."""
        tariffs = self._get_today_tariffs()
        if not tariffs:
            return None
        
        total = sum(t.get("totalAmount", 0) for t in tariffs)
        return round(total / len(tariffs), 5) if tariffs else None


class EssentTodayMinPriceSensor(EssentPriceSensorBase):
    """Sensor for today's minimum electricity price."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Today Minimum Price"
        self._attr_unique_id = f"{entry.entry_id}_today_min_price"

    @property
    def native_value(self):
        """Return today's minimum price."""
        tariffs = self._get_today_tariffs()
        if not tariffs:
            return None
        
        min_tariff = min(tariffs, key=lambda t: t.get("totalAmount", float('inf')))
        return round(min_tariff.get("totalAmount", 0), 5)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        tariffs = self._get_today_tariffs()
        if not tariffs:
            return {}
        
        min_tariff = min(tariffs, key=lambda t: t.get("totalAmount", float('inf')))
        return {
            "start_time": min_tariff.get("startDateTime"),
            "end_time": min_tariff.get("endDateTime"),
        }


class EssentTodayMaxPriceSensor(EssentPriceSensorBase):
    """Sensor for today's maximum electricity price."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry):
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_name = "Today Maximum Price"
        self._attr_unique_id = f"{entry.entry_id}_today_max_price"

    @property
    def native_value(self):
        """Return today's maximum price."""
        tariffs = self._get_today_tariffs()
        if not tariffs:
            return None
        
        max_tariff = max(tariffs, key=lambda t: t.get("totalAmount", 0))
        return round(max_tariff.get("totalAmount", 0), 5)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        tariffs = self._get_today_tariffs()
        if not tariffs:
            return {}
        
        max_tariff = max(tariffs, key=lambda t: t.get("totalAmount", 0))
        return {
            "start_time": max_tariff.get("startDateTime"),
            "end_time": max_tariff.get("endDateTime"),
        }
