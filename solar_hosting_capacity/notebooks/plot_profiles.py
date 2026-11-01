from pathlib import Path

import matplotlib.pyplot as plt
import pandapower as pp

from solar_hosting_capacity.analysis.metrics import voltage_profile
from solar_hosting_capacity.analysis.plots import add_limits, plot_profile
from solar_hosting_capacity.config import load_config
from solar_hosting_capacity.network.build import add_house_loads, add_solar, builder_feeder

cfg = load_config("config/base.yaml")


def run_scenario(load_kw: float, solar_kw: float):
    """Build a fresh feeder, apply loads (and solar if any), run the power flow."""
    feeder = builder_feeder(cfg)
    add_house_loads(feeder, kw=load_kw, pf=cfg.loads.power_factor)
    if solar_kw > 0:
        add_solar(feeder, feeder.house_buses, kw=solar_kw, kva=cfg.solar.inverter_kva)
    pp.runpp(feeder.net)
    return voltage_profile(feeder)


scenarios = {
    "No load": (0.0, 0.0),
    "Evening peak": (cfg.loads.evening_kw, 0.0),
    "Sunny midday, all solar": (cfg.loads.midday_kw, 5.0),
}

fig, ax = plt.subplots(figsize=(9, 5))
for label, (load_kw, solar_kw) in scenarios.items():
    profile = run_scenario(load_kw, solar_kw)
    print(f"{label:<25} min {profile.volts.min():6.2f} V   max {profile.volts.max():6.2f} V")
    plot_profile(profile, ax, label)

add_limits(ax)
ax.set_xlabel("Distance from transformer (m)")
ax.set_ylabel("Voltage (V)")
ax.set_ylim(210, 260)
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title(f"House voltage profiles (source = {cfg.feeder.source_vm_pu} pu)")

out = Path("figures")
out.mkdir(exist_ok=True)
fig.savefig(out / "profiles.png", dpi=150, bbox_inches="tight")
plt.show()
