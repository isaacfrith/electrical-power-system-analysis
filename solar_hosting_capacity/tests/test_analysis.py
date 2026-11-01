import pandapower as pp
import pytest

from solar_hosting_capacity.analysis.metrics import voltage_profile
from solar_hosting_capacity.config import load_config
from solar_hosting_capacity.network.build import builder_feeder


@pytest.fixture
def cfg():
    return load_config()


@pytest.fixture
def feeder(cfg):
    return builder_feeder(cfg)


def test_voltage_profile_one_row_per_house_sorted(cfg, feeder):
    pp.runpp(feeder.net)
    profile = voltage_profile(feeder)
    assert list(profile.columns) == ["bus", "dist_m", "volts"]
    assert len(profile) == cfg.feeder.n_houses
    assert set(profile.bus) == set(feeder.house_buses)
    assert profile.dist_m.is_monotonic_increasing


def test_no_load_no_solar_flat_profile(feeder):
    pp.runpp(feeder.net)
    volts = voltage_profile(feeder).volts
    assert volts.max() - volts.min() < 1e-3
