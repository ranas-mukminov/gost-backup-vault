import time
from ..domain.models import BackupResult
from .registry import (
    BACKUP_LAST_SUCCESS_TIMESTAMP,
    BACKUP_LAST_STATUS,
    BACKUP_DURATION_SECONDS,
    BACKUP_SIZE_BYTES,
    BACKUP_FAILURES_TOTAL
)

class MetricsMapper:
    @staticmethod
    def update_metrics(result: BackupResult, node_id: str, backend_type: str):
        if result.success:
            BACKUP_LAST_SUCCESS_TIMESTAMP.labels(job=result.job_name, node=node_id).set(time.time())
            BACKUP_LAST_STATUS.labels(job=result.job_name, node=node_id).set(1)
            BACKUP_SIZE_BYTES.labels(job=result.job_name, backend=backend_type).set(result.size_bytes)
        else:
            BACKUP_LAST_STATUS.labels(job=result.job_name, node=node_id).set(0)
            BACKUP_FAILURES_TOTAL.labels(job=result.job_name, reason="error").inc()
            if result.error_message and "crypto" in result.error_message.lower():
                 BACKUP_FAILURES_TOTAL.labels(job=result.job_name, reason="crypto_error").inc()

        BACKUP_DURATION_SECONDS.labels(job=result.job_name, backend=backend_type).observe(result.duration_seconds)
