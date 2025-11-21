from typing import List, Dict
from ..domain.models import BackupConfig, NodeConfig, BackendConfig, CryptoProfile, BackupJob, RetentionPolicy
from ..domain.enums import BackupBackendType, GostCipher, RetentionPolicyType

class PolicyGenerator:
    @staticmethod
    def generate_policy(
        node_id: str,
        backend_type: str,
        repo_path: str,
        gost_cipher: str,
        job_paths: List[str]
    ) -> BackupConfig:
        
        node = NodeConfig(id=node_id)
        
        backend = BackendConfig(
            type=BackupBackendType(backend_type),
            repo=repo_path
        )
        
        crypto = CryptoProfile(
            name=f"gost_{gost_cipher}_default",
            gost_cipher=GostCipher(gost_cipher)
        )
        
        job = BackupJob(
            name="default_job",
            paths=job_paths,
            schedule="daily@02:00",
            retention=RetentionPolicy(
                type=RetentionPolicyType.TIERED,
                daily=7,
                weekly=4,
                monthly=6
            )
        )
        
        return BackupConfig(
            node=node,
            backend=backend,
            crypto_profile=crypto,
            jobs=[job]
        )
