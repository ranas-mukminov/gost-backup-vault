from gost_backup_vault.domain.models import BackupResult
from gost_backup_vault.metrics import registry
from gost_backup_vault.metrics.mapping import MetricsMapper


def _reset_metrics():
    registry.BACKUP_LAST_SUCCESS_TIMESTAMP.clear()
    registry.BACKUP_LAST_STATUS.clear()
    registry.BACKUP_DURATION_SECONDS.clear()
    registry.BACKUP_SIZE_BYTES.clear()
    registry.BACKUP_FAILURES_TOTAL.clear()


def test_metrics_update_success():
    _reset_metrics()
    result = BackupResult(
        job_name="job1",
        success=True,
        duration_seconds=1.2,
        size_bytes=2048,
        snapshot_id="snap1",
    )

    MetricsMapper.update_metrics(result, node_id="node1", backend_type="restic")

    status_value = registry.BACKUP_LAST_STATUS.labels(job="job1", node="node1")._value.get()
    size_value = registry.BACKUP_SIZE_BYTES.labels(job="job1", backend="restic")._value.get()

    assert status_value == 1
    assert size_value == 2048


def test_metrics_update_failure_increments_counter():
    _reset_metrics()
    result = BackupResult(
        job_name="job2",
        success=False,
        duration_seconds=0.5,
        size_bytes=0,
        error_message="crypto error",
    )

    MetricsMapper.update_metrics(result, node_id="node2", backend_type="restic")

    counter_value = registry.BACKUP_FAILURES_TOTAL.labels(job="job2", reason="error")._value.get()
    assert counter_value == 1
