from prometheus_client import start_http_server
import time

class MetricsServer:
    def __init__(self, port: int = 9105):
        self.port = port

    def start(self):
        start_http_server(self.port)
        print(f"Metrics server started on port {self.port}")
        while True:
            time.sleep(1)
