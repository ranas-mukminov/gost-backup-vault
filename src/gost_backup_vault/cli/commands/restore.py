import typer
from pathlib import Path
from ...config.loader import ConfigLoader
from ...runner.executor import Executor
from ...policy.validator import PolicyValidator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    config: Path = typer.Option(..., exists=True, help="Path to config file"),
    job: str = typer.Option(..., help="Name of the job to restore from"),
    snapshot: str = typer.Option("latest", help="Snapshot ID to restore"),
    target: Path = typer.Option(..., help="Target directory for restore")
):
    """Restore from a backup."""
    cfg = ConfigLoader.load_from_file(config)
    errors = PolicyValidator.validate(cfg)
    if errors:
        typer.echo(f"Config validation errors: {errors}")
        raise typer.Exit(code=1)

    executor = Executor(cfg)
    
    typer.echo(f"Restoring job '{job}' snapshot '{snapshot}' to '{target}'...")
    # Implement restore logic in executor/backend
    # executor.restore(job, snapshot, target)
    typer.echo("Restore not fully implemented in this prototype.")
