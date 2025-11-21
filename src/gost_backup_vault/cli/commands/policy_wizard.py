import typer
import yaml
from ...policy.generator import PolicyGenerator

app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(output: str = typer.Option("gost-backup.yaml", help="Output config file")):
    """Interactive policy generator."""
    typer.echo("Welcome to GOST Backup Vault Policy Wizard")
    
    node_id = typer.prompt("Node ID")
    backend = typer.prompt("Backend type", default="restic", show_default=True)
    repo = typer.prompt("Repository path")
    cipher = typer.prompt("GOST Cipher (magma/kuznyechik)", default="magma")
    paths = typer.prompt("Paths to backup (comma separated)").split(",")
    
    config = PolicyGenerator.generate_policy(
        node_id=node_id,
        backend_type=backend,
        repo_path=repo,
        gost_cipher=cipher,
        job_paths=[p.strip() for p in paths]
    )
    
    with open(output, 'w') as f:
        # Pydantic v2 dump
        f.write(yaml.dump(config.model_dump(), sort_keys=False))
        
    typer.echo(f"Config written to {output}")
