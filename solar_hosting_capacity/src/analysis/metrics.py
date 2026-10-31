def run_pf(net) -> None:
    """Run pp.runpp(net) and raise a clear error if it doesn't converge
    (hint: check net.converged). TODO"""

def voltage_profile(feeder) -> "pd.DataFrame":
    """Columns: bus, dist_m, v_volts. One row per house bus, sorted by distance.
    Results live in net.res_bus.vm_pu after a run. TODO"""