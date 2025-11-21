import typer
from pathlib import Path
from ...metrics.exporter import MetricsServer

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    config: Path = typer.Option(..., exists=True, help="Path to config file"),
    listen: str = typer.Option("0.0.0.0:9105", help="Address to listen on")
):
    """Start Prometheus metrics server."""
    host, port = listen.split(":")
    server = MetricsServer(port=int(port))
    server.start()
