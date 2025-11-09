import yaml
from pathlib import Path

def load_specs(path="dq_config/specs"):
    """Loads all YAML spec files under `path`."""
    specs = []
    base = Path(path)
    for file in base.glob("*.yaml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
            specs.append(data)
    return specs
