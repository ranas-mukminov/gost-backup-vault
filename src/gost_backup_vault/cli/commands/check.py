import typer
from pathlib import Path
from ...config.loader import ConfigLoader
from ...runner.executor import Executor
from ...policy.validator import PolicyValidator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    config: Path = typer.Option(..., exists=True, help="Path to config file"),
    dry_run: bool = typer.Option(False, help="Simulate check")
):
    """Check repository integrity."""
    cfg = ConfigLoader.load_from_file(config)
    errors = PolicyValidator.validate(cfg)
    if errors:
        typer.echo(f"Config validation errors: {errors}")
        raise typer.Exit(code=1)

    executor = Executor(cfg)
    
    if dry_run:
        typer.echo("Dry run: would check repository integrity")
        return

    try:
        # We need a job context to check the repo usually
        if not cfg.jobs:
             typer.echo("No jobs defined.")
             return

        executor.backend.check(cfg.jobs[0])
        typer.echo("Repository check successful.")
    except Exception as e:
        typer.echo(f"Check failed: {e}")
        raise typer.Exit(code=1)
