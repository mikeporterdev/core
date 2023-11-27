"""Support for monitoring NanoDLP Sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NanodlpCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the available NanoDLP binary sensors."""
    coordinator: NanodlpCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]
    device_id = config_entry.unique_id

    async_add_entities(
        [
            NanoDlpCurrentLayerSensor(coordinator, device_id),
            NanoDlpPrintingSensor(coordinator, device_id),
        ]
    )


class NanoDlpSensorBase(CoordinatorEntity[NanodlpCoordinator], SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self,
        coordinator: NanodlpCoordinator,
        sensor_type: str,
        device_id: str | None,
    ) -> None:
        """Initialize a new OctoPrint sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_name = f"NanoDlp {sensor_type}"
        self._attr_unique_id = f"{sensor_type}-{device_id}"


class NanoDlpCurrentLayerSensor(NanoDlpSensorBase):
    """Representation of a Sensor."""

    _attr_icon = "mdi:printer-3d"

    def __init__(self, coordinator: NanodlpCoordinator, device_id: str | None) -> None:
        """Initialize a new OctoPrint sensor."""
        super().__init__(coordinator, "Current Layer", device_id)

    @property
    def native_value(self):
        """Return sensor state."""
        printer = self.coordinator.data["printer"]

        _LOGGER.info(printer)
        if not printer:
            return None

        return printer.layer_id

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data["printer"]


class NanoDlpPrintingSensor(NanoDlpSensorBase):
    """Representation of a Sensor."""

    _attr_icon = "mdi:printer-3d"

    def __init__(self, coordinator: NanodlpCoordinator, device_id: str | None) -> None:
        """Initialize a new OctoPrint sensor."""
        super().__init__(coordinator, "Printing", device_id)

    @property
    def native_value(self):
        """Return sensor state."""
        printer = self.coordinator.data["printer"]

        _LOGGER.info(printer)
        if not printer:
            return None

        return printer.printing

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data["printer"]
