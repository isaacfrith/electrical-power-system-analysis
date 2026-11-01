import pandas as pd
import pandapower as pp
from solar_hosting_capacity.config import load_config
from solar_hosting_capacity.constants import V_NOM
from solar_hosting_capacity.network.build import builder_feeder, add_house_loads

cfg = load_config("config/base.yaml")
feeder = builder_feeder(cfg)
net = feeder.net
add_house_loads(feeder, kw=1.8, pf=0.95)
pp.runpp(net)

profile = pd.DataFrame({
    "bus": feeder.house_buses,
    "dist_m": [feeder.dist_m[b] for b in feeder.house_buses],
    "volts": net.res_bus.loc[feeder.house_buses, "vm_pu"].values * V_NOM,
})
print(profile.to_string(index=False))
print("Street start:", round(net.res_bus.at[1, "vm_pu"] * V_NOM, 2), "V")
print("Total load:", round(net.res_load.p_mw.sum() * 1000, 1), "kW")
print("Transformer loading:", round(net.res_trafo.loading_percent.iloc[0], 1), "%")