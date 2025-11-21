from dataclasses import dataclass
from typing import List, Protocol
from ..domain.models import BackupJob, BackupResult


@dataclass
class BackendInitResult:
    initialized: bool = True
    message: str | None = None


@dataclass
class CheckResult:
    ok: bool = True
    message: str | None = None


@dataclass
class BackupSnapshot:
    snapshot_id: str
    created_at: float | None = None


@dataclass
class RestoreSpec:
    snapshot_id: str = "latest"
    target_path: str | None = None


@dataclass
class RestoreResult:
    success: bool = True
    message: str | None = None


class BackupBackend(Protocol):
    def init_repo(self, job: BackupJob) -> BackendInitResult: ...
    def backup(self, job: BackupJob) -> BackupResult: ...
    def restore(self, job: BackupJob, restore_spec: RestoreSpec) -> RestoreResult: ...
    def check(self, job: BackupJob) -> CheckResult: ...
    def list_backups(self, job: BackupJob) -> List[BackupSnapshot]: ...
