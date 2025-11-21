import typer
from pathlib import Path
from ...metrics.exporter import MetricsServer
from ...config.loader import ConfigLoader
from ...policy.validator import PolicyValidator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    config: Path = typer.Option(..., exists=True, help="Path to config file"),
    listen: str = typer.Option("0.0.0.0:9105", help="Address to listen on")
):
    """Start Prometheus metrics server."""
    # We still load and validate the config to ensure the file is present and correct,
    # even though metrics serving itself is stateless in this prototype.
    cfg = ConfigLoader.load_from_file(config)
    errors = PolicyValidator.validate(cfg)
    if errors:
        typer.echo(f"Config validation errors: {errors}")
        raise typer.Exit(code=1)

    host, port = listen.split(":")
    server = MetricsServer(port=int(port), host=host)
    server.start()
