from prometheus_client import Gauge, Counter, Histogram, Summary

# Metrics definitions
BACKUP_LAST_SUCCESS_TIMESTAMP = Gauge(
    'gost_backup_last_success_timestamp',
    'Timestamp of the last successful backup',
    ['job', 'node']
)

BACKUP_LAST_STATUS = Gauge(
    'gost_backup_last_status',
    'Status of the last backup (1 for success, 0 for failure)',
    ['job', 'node']
)

BACKUP_DURATION_SECONDS = Histogram(
    'gost_backup_duration_seconds',
    'Duration of backup in seconds',
    ['job', 'backend']
)

BACKUP_SIZE_BYTES = Gauge(
    'gost_backup_size_bytes',
    'Size of the last backup in bytes',
    ['job', 'backend']
)

BACKUP_FAILURES_TOTAL = Counter(
    'gost_backup_failures_total',
    'Total number of backup failures',
    ['job', 'reason']
)
