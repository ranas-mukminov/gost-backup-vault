import pytest
from unittest.mock import MagicMock, patch
from gost_backup_vault.backends.restic_backend import ResticBackend
from gost_backup_vault.domain.models import BackendConfig, BackupJob
from gost_backup_vault.domain.enums import BackupBackendType

@patch("subprocess.run")
def test_restic_backup_success(mock_run):
    config = BackendConfig(type=BackupBackendType.RESTIC, repo="/tmp/repo")
    backend = ResticBackend(config)
    
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout='{"data_added": 1024, "snapshot_id": "abc1234"}'
    )
    
    job = BackupJob(name="test", paths=["/data"], schedule="daily")
    result = backend.backup(job)
    
    assert result.success
    assert result.size_bytes == 1024
    assert result.snapshot_id == "abc1234"

@patch("subprocess.run")
def test_restic_backup_failure(mock_run):
    config = BackendConfig(type=BackupBackendType.RESTIC, repo="/tmp/repo")
    backend = ResticBackend(config)
    
    mock_run.return_value = MagicMock(
        returncode=1,
        stderr="Error connecting to repo"
    )
    
    job = BackupJob(name="test", paths=["/data"], schedule="daily")
    result = backend.backup(job)
    
    assert not result.success
    assert "Error connecting to repo" in result.error_message
