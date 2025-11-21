import logging
import time

from prometheus_client import start_http_server

logger = logging.getLogger(__name__)

class MetricsServer:
    def __init__(self, port: int = 9105, host: str = "0.0.0.0"):
        self.port = port
        self.host = host

    def start(self):
        start_http_server(self.port, addr=self.host)
        logger.info("Metrics server started on %s:%s", self.host, self.port)
        while True:
            time.sleep(1)
