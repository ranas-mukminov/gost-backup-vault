import pytest
import shutil
import subprocess
from pathlib import Path
from gost_backup_vault.runner.executor import Executor
from gost_backup_vault.domain.models import BackupConfig, NodeConfig, BackendConfig, CryptoProfile, BackupJob
from gost_backup_vault.domain.enums import BackupBackendType, GostCipher

@pytest.mark.skipif(shutil.which("restic") is None, reason="restic not installed")
def test_restic_integration_flow(tmp_path):
    repo_path = tmp_path / "repo"
    data_path = tmp_path / "data"
    data_path.mkdir()
    (data_path / "file.txt").write_text("secret data")
    
    config = BackupConfig(
        node=NodeConfig(id="test-node"),
        backend=BackendConfig(type=BackupBackendType.RESTIC, repo=str(repo_path)),
        crypto_profile=CryptoProfile(name="test", gost_cipher=GostCipher.NONE),
        jobs=[
            BackupJob(name="test-job", paths=[str(data_path)], schedule="daily")
        ]
    )
    
    executor = Executor(config)
    
    # Init
    executor.backend.init_repo(config.jobs[0])
    assert repo_path.exists()
    
    # Backup
    result = executor.run_job("test-job")
    assert result.success
    assert result.size_bytes > 0
    
    # Check
    executor.backend.check(config.jobs[0])
