import logging
from typing import List

from ..backends.base import BackupBackend
from ..backends.borg_backend import BorgBackend
from ..backends.restic_backend import ResticBackend
from ..backends.tar_backend import TarBackend
from ..domain.enums import BackupBackendType
from ..domain.models import BackupConfig, BackupJob, BackupResult

logger = logging.getLogger(__name__)

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
        except Exception as exc:
            logger.warning("Backend init failed for job %s: %s", job.name, exc)
            raise

        return self.backend.backup(job)

    def run_all(self) -> List[BackupResult]:
        results = []
        for job in self.config.jobs:
            results.append(self.run_job(job.name))
        return results
