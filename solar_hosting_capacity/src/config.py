from dataclasses import dataclass

@dataclass(frozen=True)
class FeederConfig:
    n_houses: int
    backbone_length_m: float
    # TODO: remaining feeder fields

@dataclass(frozen=True)
class Config:
    run_name: str
    seed: int
    feeder: FeederConfig
    # TODO: loads, solar, inverter

def load_config(path: str) -> Config:
    """Read YAML with yaml.safe_load and build the dataclasses. TODO"""