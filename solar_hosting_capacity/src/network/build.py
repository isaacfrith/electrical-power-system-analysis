import pandapower as pp 
import math
from types import SimpleNamespace
from dataclasses import dataclass

@dataclass
class Feeder:
    net: pp.pandapowerNet
    house_buses: list[int]        # pandapower bus index of each house, in order along the street
    dist_m: dict[int, float] 

def builder_feeder(cfg) -> Feeder:
    net = pp.create_empty_network()

    #HV bus + external grid
    hv_bus = pp.create_bus(net, vn_kv=20.0, name="HV")
    pp.create_ext_grid(net, bus=hv_bus, vm_pu=cfg.feeder.source_vm_pu)

    lv_bus = pp.create_bus(net, vn_kv=cfg.feeder.lv_vn_kv, name="LV street start")
    pp.create_transformer(net, hv_bus, lv_bus, std_type=cfg.feeder.trafo_type)

    n_segments = int(cfg.feeder.backbone_length_m / cfg.feeder.segment_length_m)
    prev_bus = lv_bus
    distance_m = 0.0 
    backbone_buses = []
    dist_m = {}

    for i in range(n_segments):
        new_bus = pp.create_bus(net, vn_kv=cfg.feeder.lv_vn_kv, name=f"BB {i+1}")
        pp.create_line(net, from_bus=prev_bus, to_bus = new_bus, length_km=cfg.feeder.segment_length_m / 1000, std_type=cfg.feeder.backbone_line_type)

        distance_m += cfg.feeder.segment_length_m
        dist_m[new_bus] = distance_m
        backbone_buses.append(new_bus)
        prev_bus = new_bus



    #house loop
    house_buses = []
    for i in range(cfg.feeder.n_houses):
        bb_bus = backbone_buses[int(i * len(backbone_buses) / cfg.feeder.n_houses)]
        house_bus = pp.create_bus(net, vn_kv=cfg.feeder.lv_vn_kv, name=f"House {i + 1}")
        pp.create_line(net, from_bus=bb_bus, to_bus=house_bus, length_km=cfg.feeder.service_length_m/1000, std_type=cfg.feeder.service_line_type)

        dist_m[house_bus] = dist_m[bb_bus] + cfg.feeder.service_length_m
        house_buses.append(house_bus)

    return Feeder(net=net, house_buses=house_buses, dist_m=dist_m)

if __name__ == "__main__":
    cfg = SimpleNamespace(feeder=SimpleNamespace(
    source_vm_pu=1.03, lv_vn_kv=0.398, trafo_type="0.4 MVA 20/0.4 kV",
    segment_length_m=20, backbone_length_m=400,
    backbone_line_type="NAYY 4x150 SE",
    n_houses=30, service_length_m=20, service_line_type="NAYY 4x50 SE",
    ))

    feeder = builder_feeder(cfg)
    net = feeder.net
    print(len(net.bus), len(net.line))
    print(net.line.tail(5)[["from_bus", "to_bus", "length_km", "std_type"]])
    print({b: feeder.dist_m[b] for b in feeder.house_buses[:5]})

    pp.runpp(net)
    print(net.res_bus.vm_pu.describe())


def add_house_loads(feeder: Feeder, kw: float, pf: float) -> list[int]:
    """Create one load per house bus. Return the load indices.
    hint: pp.create_load(net, bus, p_mw=..., q_mvar=...)
    Use kw_to_mw and q_from_pf from constants. TODO"""
    