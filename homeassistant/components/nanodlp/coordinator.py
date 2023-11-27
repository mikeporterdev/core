"""The data update coordinator for NanoDLP."""
import asyncio
from datetime import timedelta
import logging

from pynanodlpapi import NanoDlpClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class NanodlpCoordinator(DataUpdateCoordinator):
    """Class to manage fetching NanoDLP data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        nanodlp: NanoDlpClient,
        config_entry: ConfigEntry,
        interval: int,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"nanodlp-{config_entry.entry_id}",
            update_interval=timedelta(seconds=interval),
        )
        self.config_entry = config_entry
        self._nanodlp = nanodlp
        self._printer_offline = False
        self.data = {"printer": None, "job": None, "last_read_time": None}

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.
        async with asyncio.timeout(10):
            printer = await self._nanodlp.get_status()
            _LOGGER.info(printer)
            return {"printer": printer}
