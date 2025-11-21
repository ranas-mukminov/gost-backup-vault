import yaml
from pathlib import Path
from typing import Any, Dict
from pydantic import ValidationError
from ..domain.models import BackupConfig

class ConfigLoader:
    @staticmethod
    def load_from_file(path: Path) -> BackupConfig:
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML: {e}")
        
        try:
            return BackupConfig(**data)
        except ValidationError as e:
            raise ValueError(f"Config validation error: {e}")

    @staticmethod
    def validate(config: BackupConfig) -> bool:
        # Add custom validation logic here if needed beyond Pydantic
        return True
