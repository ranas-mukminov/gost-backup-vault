from gost_backup_vault.policy.generator import PolicyGenerator
from gost_backup_vault.domain.enums import BackupBackendType, GostCipher

def test_generate_policy():
    config = PolicyGenerator.generate_policy(
        node_id="node1",
        backend_type="restic",
        repo_path="/tmp/repo",
        gost_cipher="magma",
        job_paths=["/etc", "/home"]
    )
    
    assert config.node.id == "node1"
    assert config.backend.type == BackupBackendType.RESTIC
    assert config.crypto_profile.gost_cipher == GostCipher.MAGMA
    assert len(config.jobs) == 1
    assert config.jobs[0].paths == ["/etc", "/home"]
