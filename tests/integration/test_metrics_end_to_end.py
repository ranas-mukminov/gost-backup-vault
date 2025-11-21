import pytest
import requests
import time
import threading
from gost_backup_vault.metrics.exporter import MetricsServer
from gost_backup_vault.metrics.mapping import MetricsMapper
from gost_backup_vault.domain.models import BackupResult

def test_metrics_end_to_end():
    # Start server in thread
    server = MetricsServer(port=9106)
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    
    # Give it a moment to start
    time.sleep(1)
    
    # Update metrics
    result = BackupResult(
        job_name="test-job",
        success=True,
        duration_seconds=1.5,
        size_bytes=1024,
        snapshot_id="abc"
    )
    MetricsMapper.update_metrics(result, "node1", "restic")
    
    # Scrape
    response = requests.get("http://localhost:9106/metrics")
    assert response.status_code == 200
    content = response.text
    
    assert 'gost_backup_last_status{job="test-job",node="node1"} 1.0' in content
    assert 'gost_backup_size_bytes{backend="restic",job="test-job"} 1024.0' in content
