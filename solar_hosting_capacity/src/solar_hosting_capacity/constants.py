# src/solar_hosting_capacity/constants.py
import math 

V_NOM = 230.0
V_MIN, V_MAX = 216.0, 253.0              # AS 61000.3.100 steady-state limits
V_MIN_OUTER, V_MAX_OUTER = 207.0, 260.0  # outer band

def kw_to_mw(kw: float) -> float:
    """pandapower works in MW. TODO"""
    return kw / 1000

def pu_to_volts(vm_pu, base_v: float = V_NOM):
    """Works on floats, numpy arrays and pandas Series alike. TODO"""
    return vm_pu * base_v

def q_from_pf(p: float, pf: float) -> float:
    """Reactive power for a given real power and power factor.
    Hint: Q = P × tan(arccos(pf)). TODO"""
    return p * math.tan(math.acos(pf))