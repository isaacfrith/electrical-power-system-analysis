from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "config" / "base.yaml"


@dataclass(frozen=True)
class FeederConfig:
    n_houses: int
    backbone_length_m: float
    segment_length_m: float
    service_length_m: float
    backbone_line_type: str
    service_line_type: str
    trafo_type: str
    source_vm_pu: float
    lv_vn_kv: float


@dataclass(frozen=True)
class LoadsConfig:
    evening_kw: float
    midday_kw: float
    power_factor: float


@dataclass(frozen=True)
class SolarConfig:
    inverter_kva: float
    penetration_levels: list[float]
    runs_per_level: int


@dataclass(frozen=True)
class InverterConfig:
    mode: str  # unity | volt_var | volt_watt | vv_vw


@dataclass(frozen=True)
class Config:
    run_name: str
    seed: int
    feeder: FeederConfig
    loads: LoadsConfig
    solar: SolarConfig
    inverter: InverterConfig


def load_config(path: str | Path = DEFAULT_CONFIG) -> Config:
    """Read YAML with yaml.safe_load and build the dataclasses."""
    with open(path) as f:
        raw = yaml.safe_load(f)

    return Config(
        run_name=raw["run_name"],
        seed=raw["seed"],
        feeder=FeederConfig(**raw["feeder"]),
        loads=LoadsConfig(**raw["loads"]),
        solar=SolarConfig(**raw["solar"]),
        inverter=InverterConfig(**raw["inverter"]),
    )
