""" Tests for TeamTracker """

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.teamtracker.const import DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.entity_registry import async_get
from homeassistant.setup import async_setup_component
from tests.const import CONFIG_DATA
from unittest.mock import patch

@pytest.fixture(autouse=False)
def expected_lingering_timers() -> bool:
    """  Temporary ability to bypass test failures due to lingering timers.
    Parametrize to True to bypass the pytest failure.
    @pytest.mark.parametrize("expected_lingering_timers", [True])
    This should be removed when all lingering timers have been cleaned up.
    """
    return False

    
#@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_setup_entry(
    hass,
):
    """ test setup """

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="team_tracker",
        data=CONFIG_DATA,
    )

    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_entity_ids(SENSOR_DOMAIN)) == 1
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert await entry.async_unload(hass)
    await hass.async_block_till_done()


#@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_unload_entry(hass):
    """ test unload """

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="team_tracker",
        data=CONFIG_DATA,
    )

    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_entity_ids(SENSOR_DOMAIN)) == 1
    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert await hass.config_entries.async_unload(entries[0].entry_id)
    await hass.async_block_till_done()
    assert len(hass.states.async_entity_ids(SENSOR_DOMAIN)) == 1
    assert len(hass.states.async_entity_ids(DOMAIN)) == 0

    assert await hass.config_entries.async_remove(entries[0].entry_id)
    await hass.async_block_till_done()
    assert len(hass.states.async_entity_ids(SENSOR_DOMAIN)) == 0

    assert await entry.async_unload(hass)
    await hass.async_block_till_done()


async def test_import(hass):
    """Test importing a config."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="team_tracker",
        data=CONFIG_DATA,
    )

    await async_setup_component(hass, "persistent_notification", {})
    with patch(
        "custom_components.teamtracker.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:

        ent_reg = async_get(hass)
        ent_entry = ent_reg.async_get_or_create(
            "sensor", DOMAIN, unique_id="replaceable_unique_id", config_entry=entry
        )
        entity_id = ent_entry.entity_id
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.unique_id is None
        assert ent_reg.async_get(entity_id).unique_id == entry.entry_id
