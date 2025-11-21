from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import ValidationError

from ..domain.models import BackupConfig
from ..policy.validator import PolicyValidator

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
            config = BackupConfig(**data)
        except ValidationError as e:
            raise ValueError(f"Config validation error: {e}")

        errors = PolicyValidator.validate(config)
        if errors:
            raise ValueError(f"Config policy validation errors: {errors}")

        return config

    @staticmethod
    def validate(config: BackupConfig) -> List[str]:
        """
        Validate a parsed BackupConfig and return a list of error messages.
        """
        return PolicyValidator.validate(config)
