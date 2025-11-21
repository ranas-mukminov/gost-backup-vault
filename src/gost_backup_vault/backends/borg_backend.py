import json
import logging
import subprocess
import time
from typing import List

from ..domain.models import BackendConfig, BackupJob, BackupResult
from .base import (
    BackupBackend,
    BackupSnapshot,
    BackendInitResult,
    CheckResult,
    RestoreResult,
    RestoreSpec,
)

logger = logging.getLogger(__name__)

class BorgBackend(BackupBackend):
    def __init__(self, config: BackendConfig):
        self.config = config
        self.repo = config.repo

    def _run_command(self, args: List[str]) -> subprocess.CompletedProcess[str]:
        cmd = ["borg"] + args
        # Environment variables for passphrase should be handled here
        return subprocess.run(cmd, capture_output=True, text=True)

    def init_repo(self, job: BackupJob) -> BackendInitResult:
        # Borg requires encryption mode during init
        res = self._run_command(["init", "--encryption=repokey", self.repo])
        if res.returncode != 0:
            logger.error("Borg init failed: %s", res.stderr)
            raise RuntimeError(f"Borg init failed: {res.stderr}")
        return BackendInitResult()

    def backup(self, job: BackupJob) -> BackupResult:
        start_time = time.time()
        archive_name = f"{self.repo}::{job.name}-{int(time.time())}"
        cmd = ["create", "--json", archive_name] + job.paths
        
        if job.exclude:
            for excl in job.exclude:
                cmd.extend(["--exclude", excl])

        res = self._run_command(cmd)
        duration = time.time() - start_time

        if res.returncode != 0:
            logger.error("Borg backup failed for job %s: %s", job.name, res.stderr)
            return BackupResult(
                job_name=job.name,
                success=False,
                duration_seconds=duration,
                size_bytes=0,
                error_message=res.stderr,
            )
        
        # Parse JSON output
        try:
            data = json.loads(res.stdout)
            archive = data.get("archive", {})
            size_bytes = archive.get("stats", {}).get("deduplicated_size", 0)
            snapshot_id = archive.get("name", archive_name)
        except Exception as exc:  # pragma: no cover - defensive parsing
            logger.warning("Failed to parse borg output for job %s: %s", job.name, exc)
            size_bytes = 0
            snapshot_id = archive_name

        return BackupResult(
            job_name=job.name,
            success=True,
            duration_seconds=duration,
            size_bytes=size_bytes,
            snapshot_id=snapshot_id,
        )

    def restore(self, job: BackupJob, restore_spec: RestoreSpec) -> RestoreResult:
        return RestoreResult()

    def check(self, job: BackupJob) -> CheckResult:
        res = self._run_command(["check", self.repo])
        if res.returncode != 0:
            logger.error("Borg check failed: %s", res.stderr)
            raise RuntimeError(f"Borg check failed: {res.stderr}")
        return CheckResult()

    def list_backups(self, job: BackupJob) -> List[BackupSnapshot]:
        return []
