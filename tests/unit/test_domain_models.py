import pytest
from pydantic import ValidationError
from gost_backup_vault.domain.models import BackupJob, RetentionPolicy, CryptoProfile
from gost_backup_vault.domain.enums import GostCipher, RetentionPolicyType

def test_backup_job_model():
    job = BackupJob(
        name="test",
        paths=["/etc"],
        schedule="daily"
    )
    assert job.name == "test"
    assert job.paths == ["/etc"]

def test_crypto_profile_validation():
    with pytest.raises(ValidationError):
        CryptoProfile(name="test", gost_cipher="invalid_cipher")

    profile = CryptoProfile(name="test", gost_cipher=GostCipher.MAGMA)
    assert profile.gost_cipher == GostCipher.MAGMA
