import pandapower as pp
import pytest

from solar_hosting_capacity.config import load_config
from solar_hosting_capacity.network.build import add_house_loads, builder_feeder

CFG = load_config("config/base.yaml")

@pytest.fixture
def cfg():
    return load_config()


@pytest.fixture
def feeder(cfg):
    return builder_feeder(cfg)


def test_feeder_size(cfg, feeder):
    """HV + LV street start + one bus per backbone segment + one per house."""
    n_segments = int(cfg.feeder.backbone_length_m / cfg.feeder.segment_length_m)
    assert len(feeder.net.bus) == 2 + n_segments + cfg.feeder.n_houses
    assert len(feeder.net.line) == n_segments + cfg.feeder.n_houses
    assert len(feeder.house_buses) == cfg.feeder.n_houses


def test_house_distances_increase(cfg, feeder):
    dists = [feeder.dist_m[b] for b in feeder.house_buses]
    assert dists == sorted(dists)
    assert dists[0] == cfg.feeder.segment_length_m + cfg.feeder.service_length_m
    assert dists[-1] <= cfg.feeder.backbone_length_m + cfg.feeder.service_length_m


def test_no_load_no_drop(feeder):
    """With no loads and no solar, every house bus should sit at (almost exactly)
    the street-start voltage."""
    net = feeder.net
    pp.runpp(net)
    lv_start = net.bus.index[net.bus.name == "LV street start"][0]
    v_start = net.res_bus.vm_pu.at[lv_start]
    house_v = net.res_bus.vm_pu.loc[feeder.house_buses]
    assert house_v.sub(v_start).abs().max() < 1e-4

def test_no_load_voltages_equal():
    feeder = builder_feeder(CFG)
    pp.runpp(feeder.net)
    v = feeder.net.res_bus.loc[feeder.house_buses, "vm_pu"]
    assert v.max() - v.min() < 1e-5      # pick a tiny tolerance

def test_load_drops_voltage_along_street():
    feeder = builder_feeder(CFG)
    add_house_loads(feeder, kw=1.8, pf=0.95)
    pp.runpp(feeder.net)
    v = feeder.net.res_bus.loc[feeder.house_buses, "vm_pu"]
    first, last = feeder.house_buses[0], feeder.house_buses[-1]
    assert v[first] > v[last]             # which house should be higher?
