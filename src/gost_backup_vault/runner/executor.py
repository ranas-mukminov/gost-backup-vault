import time
from typing import List
from ..domain.models import BackupConfig, BackupResult, BackupJob
from ..backends.base import BackupBackend
from ..backends.restic_backend import ResticBackend
from ..backends.borg_backend import BorgBackend
from ..backends.tar_backend import TarBackend
from ..domain.enums import BackupBackendType

class Executor:
    def __init__(self, config: BackupConfig):
        self.config = config
        self.backend = self._init_backend()

    def _init_backend(self) -> BackupBackend:
        if self.config.backend.type == BackupBackendType.RESTIC:
            return ResticBackend(self.config.backend)
        elif self.config.backend.type == BackupBackendType.BORG:
            return BorgBackend(self.config.backend)
        elif self.config.backend.type == BackupBackendType.TAR:
            return TarBackend(self.config.backend)
        else:
            raise ValueError(f"Unsupported backend: {self.config.backend.type}")

    def run_job(self, job_name: str) -> BackupResult:
        job = next((j for j in self.config.jobs if j.name == job_name), None)
        if not job:
            raise ValueError(f"Job not found: {job_name}")

        # In a real implementation, we would check schedule here or in a higher level scheduler
        
        # Init repo if needed (idempotent usually)
        try:
             self.backend.init_repo(job)
        except Exception as e:
             # Log warning but continue, maybe it's already initialized
             pass

        return self.backend.backup(job)

    def run_all(self) -> List[BackupResult]:
        results = []
        for job in self.config.jobs:
            results.append(self.run_job(job.name))
        return results
