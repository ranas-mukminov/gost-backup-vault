import pytest
import yaml
from pathlib import Path
from gost_backup_vault.config.loader import ConfigLoader
from gost_backup_vault.domain.models import BackupConfig

def test_load_valid_config(tmp_path):
    config_data = {
        "node": {"id": "test-node"},
        "backend": {"type": "restic", "repo": "/tmp/repo"},
        "crypto_profile": {"name": "test-crypto", "gost_cipher": "magma"},
        "jobs": [
            {
                "name": "test-job",
                "paths": ["/tmp/data"],
                "schedule": "daily"
            }
        ]
    }
    
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
        
    config = ConfigLoader.load_from_file(config_file)
    assert isinstance(config, BackupConfig)
    assert config.node.id == "test-node"
    assert config.jobs[0].name == "test-job"

def test_load_invalid_config(tmp_path):
    config_file = tmp_path / "invalid.yaml"
    with open(config_file, "w") as f:
        f.write("invalid: yaml: content")
        
    with pytest.raises(ValueError):
        ConfigLoader.load_from_file(config_file)
