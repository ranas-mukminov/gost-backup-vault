import pytest

from gost_backup_vault.domain.enums import BackupBackendType, GostCipher, RetentionPolicyType
from gost_backup_vault.domain.models import (
    BackendConfig,
    BackupConfig,
    BackupJob,
    CryptoProfile,
    NodeConfig,
    RetentionPolicy,
)
from gost_backup_vault.policy.validator import PolicyValidator


def _minimal_config(job_overrides: dict | None = None) -> BackupConfig:
    job = BackupJob(
        name="job1",
        paths=["/data"],
        schedule="daily",
        retention=RetentionPolicy(type=RetentionPolicyType.SIMPLE, keep_last=1),
    )
    if job_overrides:
        for key, value in job_overrides.items():
            setattr(job, key, value)

    return BackupConfig(
        node=NodeConfig(id="node1"),
        backend=BackendConfig(type=BackupBackendType.RESTIC, repo="/tmp/repo"),
        crypto_profile=CryptoProfile(name="cp", gost_cipher=GostCipher.NONE),
        jobs=[job],
    )


def test_validator_allows_valid_config():
    config = _minimal_config()
    assert PolicyValidator.validate(config) == []


def test_validator_detects_duplicate_jobs():
    config = _minimal_config()
    duplicate = config.jobs[0].model_copy()
    config.jobs.append(duplicate)

    errors = PolicyValidator.validate(config)

    assert any("Duplicate job name" in err for err in errors)


def test_validator_detects_missing_paths():
    config = _minimal_config({"paths": []})

    errors = PolicyValidator.validate(config)

    assert any("has no paths" in err for err in errors)


def test_validator_detects_missing_schedule():
    config = _minimal_config({"schedule": ""})

    errors = PolicyValidator.validate(config)

    assert any("missing schedule" in err for err in errors)


def test_validator_requires_jobs():
    config = _minimal_config()
    config.jobs = []

    errors = PolicyValidator.validate(config)

    assert "No backup jobs defined" in errors
