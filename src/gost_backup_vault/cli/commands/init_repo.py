import typer
from pathlib import Path
from ...config.loader import ConfigLoader
from ...runner.executor import Executor
from ...policy.validator import PolicyValidator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(config: Path = typer.Option(..., exists=True, help="Path to config file")):
    """Initialize the backup repository."""
    cfg = ConfigLoader.load_from_file(config)
    errors = PolicyValidator.validate(cfg)
    if errors:
        typer.echo(f"Config validation errors: {errors}")
        raise typer.Exit(code=1)

    executor = Executor(cfg)
    
    # In a real scenario, we might want to init specific jobs or just the repo
    # For now, we just pick the first job to get the backend context
    if not cfg.jobs:
        typer.echo("No jobs defined in config.")
        raise typer.Exit(code=1)
        
    # This is a simplification. The backend init might need to be more granular.
    try:
        executor.backend.init_repo(cfg.jobs[0])
        typer.echo("Repository initialized successfully.")
    except Exception as e:
        typer.echo(f"Initialization failed: {e}")
        raise typer.Exit(code=1)
