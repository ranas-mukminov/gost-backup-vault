import subprocess
import time
import os
from typing import List
from ..domain.models import BackupJob, BackupResult, BackendConfig
from .base import BackupBackend, BackendInitResult, CheckResult, BackupSnapshot, RestoreSpec, RestoreResult

class TarBackend(BackupBackend):
    def __init__(self, config: BackendConfig):
        self.config = config
        self.repo = config.repo # For tar, this is the destination directory

    def init_repo(self, job: BackupJob) -> BackendInitResult:
        if not os.path.exists(self.repo):
            os.makedirs(self.repo)
        return BackendInitResult()

    def backup(self, job: BackupJob) -> BackupResult:
        start_time = time.time()
        archive_name = f"{job.name}-{int(time.time())}.tar"
        archive_path = os.path.join(self.repo, archive_name)
        
        cmd = ["tar", "-cf", archive_path] + job.paths
        if job.exclude:
            for excl in job.exclude:
                cmd.extend(["--exclude", excl])

        res = subprocess.run(cmd, capture_output=True, text=True)
        duration = time.time() - start_time

        if res.returncode != 0:
             return BackupResult(
                job_name=job.name,
                success=False,
                duration_seconds=duration,
                size_bytes=0,
                error_message=res.stderr
            )
        
        size_bytes = os.path.getsize(archive_path)

        return BackupResult(
            job_name=job.name,
            success=True,
            duration_seconds=duration,
            size_bytes=size_bytes,
            snapshot_id=archive_name
        )

    def restore(self, job: BackupJob, restore_spec: RestoreSpec) -> RestoreResult:
        return RestoreResult()

    def check(self, job: BackupJob) -> CheckResult:
        return CheckResult()

    def list_backups(self, job: BackupJob) -> List[BackupSnapshot]:
        return []
