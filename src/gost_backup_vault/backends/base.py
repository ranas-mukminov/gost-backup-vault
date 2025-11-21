from typing import Protocol, List
from ..domain.models import BackupJob, BackupResult

class BackendInitResult(Protocol):
    pass

class CheckResult(Protocol):
    pass

class BackupSnapshot(Protocol):
    pass

class RestoreSpec(Protocol):
    pass

class RestoreResult(Protocol):
    pass

class BackupBackend(Protocol):
    def init_repo(self, job: BackupJob) -> BackendInitResult: ...
    def backup(self, job: BackupJob) -> BackupResult: ...
    def restore(self, job: BackupJob, restore_spec: RestoreSpec) -> RestoreResult: ...
    def check(self, job: BackupJob) -> CheckResult: ...
    def list_backups(self, job: BackupJob) -> List[BackupSnapshot]: ...
