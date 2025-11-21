import typer
from pathlib import Path
from ...config.loader import ConfigLoader
from ...runner.executor import Executor
from ...metrics.mapping import MetricsMapper
from ...policy.validator import PolicyValidator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(
    config: Path = typer.Option(..., exists=True, help="Path to config file"),
    job: str = typer.Option(..., help="Name of the backup job to run"),
    dry_run: bool = typer.Option(False, help="Simulate backup without writing data")
):
    """Run a backup job."""
    cfg = ConfigLoader.load_from_file(config)
    errors = PolicyValidator.validate(cfg)
    if errors:
        typer.echo(f"Config validation errors: {errors}")
        raise typer.Exit(code=1)

    executor = Executor(cfg)
    
    if dry_run:
        typer.echo(f"Dry run: would backup job '{job}'")
        return

    try:
        result = executor.run_job(job)
        MetricsMapper.update_metrics(result, cfg.node.id, cfg.backend.type.value)
        
        if result.success:
            typer.echo(f"Backup successful: {result.snapshot_id}, size: {result.size_bytes} bytes")
        else:
            typer.echo(f"Backup failed: {result.error_message}")
            raise typer.Exit(code=1)
            
    except Exception as e:
        typer.echo(f"Backup execution error: {e}")
        raise typer.Exit(code=1)
