"""The decora_wifi component."""

from dataclasses import dataclass

from decora_wifi import DecoraWiFiSession

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN

PLATFORMS = [Platform.LIGHT]


@dataclass
class DecoraComponentData:
    """Decora Component Data Class."""

    session: DecoraWiFiSession


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up config entry."""

    hass.data.setdefault(DOMAIN, {})

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    session = DecoraWiFiSession()
    user = await hass.async_add_executor_job(lambda: session.login(username, password))
    if not user:
        raise ConfigEntryAuthFailed("invalid authentication")

    hass.data[DOMAIN][entry.entry_id] = DecoraComponentData(session)

    # Forward the setup to the sensor platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data.pop(DOMAIN)
    return unload_ok
