import subprocess
import json
import time
from typing import List
from ..domain.models import BackupJob, BackupResult, BackendConfig
from .base import BackupBackend, BackendInitResult, CheckResult, BackupSnapshot, RestoreSpec, RestoreResult

class ResticBackend(BackupBackend):
    def __init__(self, config: BackendConfig):
        self.config = config
        self.repo = config.repo
        self.password_file = None # Should be handled securely

    def _run_command(self, args: List[str]) -> subprocess.CompletedProcess[str]:
        cmd = ["restic", "-r", self.repo] + args
        # In a real implementation, handle environment variables for passwords securely
        return subprocess.run(cmd, capture_output=True, text=True)

    def init_repo(self, job: BackupJob) -> BackendInitResult:
        res = self._run_command(["init"])
        if res.returncode != 0:
            raise RuntimeError(f"Restic init failed: {res.stderr}")
        return BackendInitResult() # Placeholder

    def backup(self, job: BackupJob) -> BackupResult:
        start_time = time.time()
        cmd = ["backup"] + job.paths
        if job.exclude:
            for excl in job.exclude:
                cmd.extend(["--exclude", excl])
        
        res = self._run_command(cmd + ["--json"])
        duration = time.time() - start_time
        
        if res.returncode != 0:
             return BackupResult(
                job_name=job.name,
                success=False,
                duration_seconds=duration,
                size_bytes=0,
                error_message=res.stderr
            )

        # Parse JSON output from restic to get size and snapshot ID
        # This is a simplified parsing logic
        try:
            output_lines = res.stdout.strip().split('\n')
            summary_line = output_lines[-1]
            summary = json.loads(summary_line)
            size_bytes = summary.get("data_added", 0)
            snapshot_id = summary.get("snapshot_id", "unknown")
        except Exception:
            size_bytes = 0
            snapshot_id = "unknown"

        return BackupResult(
            job_name=job.name,
            success=True,
            duration_seconds=duration,
            size_bytes=size_bytes,
            snapshot_id=snapshot_id
        )

    def restore(self, job: BackupJob, restore_spec: RestoreSpec) -> RestoreResult:
        # Placeholder implementation
        return RestoreResult()

    def check(self, job: BackupJob) -> CheckResult:
        res = self._run_command(["check"])
        if res.returncode != 0:
             raise RuntimeError(f"Restic check failed: {res.stderr}")
        return CheckResult()

    def list_backups(self, job: BackupJob) -> List[BackupSnapshot]:
        return []
