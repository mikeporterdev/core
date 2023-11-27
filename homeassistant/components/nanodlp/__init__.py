"""The NanoDLP integration."""
from __future__ import annotations

import aiohttp
from pynanodlpapi import NanoDlpClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import NanodlpCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

PRINTER_ENDPOINT = "status"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NanoDLP from a config entry."""

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data.setdefault(DOMAIN, {})
    connector = aiohttp.TCPConnector(
        force_close=True,
    )
    session = aiohttp.ClientSession(connector=connector)
    client = NanoDlpClient(host=entry.data["host"], session=session)
    coordinator = NanodlpCoordinator(hass, client, entry, 5)
    hass.data[DOMAIN][entry.entry_id] = {"client": client, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
