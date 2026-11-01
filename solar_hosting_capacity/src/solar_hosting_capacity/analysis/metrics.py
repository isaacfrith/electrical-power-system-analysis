import pandas as pd
import pandapower as pp

from solar_hosting_capacity.constants import pu_to_volts


def run_pf(net) -> None:
    """Run pp.runpp(net) and raise a clear error if it doesn't converge."""
    pp.runpp(net)
    if not net.converged:
        raise RuntimeError("Power flow did not converge")


def voltage_profile(feeder) -> pd.DataFrame:
    """Columns: bus, dist_m, volts. One row per house bus, sorted by distance.
    Assumes a power flow has already run (results in net.res_bus.vm_pu)."""
    buses = feeder.house_buses
    profile = pd.DataFrame({
        "bus": buses,
        "dist_m": [feeder.dist_m[b] for b in buses],
        "volts": pu_to_volts(feeder.net.res_bus.loc[buses, "vm_pu"]).to_numpy(),
    })
    return profile.sort_values("dist_m", ignore_index=True)
