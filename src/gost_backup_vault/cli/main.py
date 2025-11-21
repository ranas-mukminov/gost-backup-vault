import typer
from pathlib import Path
from .commands import init_repo, backup, restore, check, policy_wizard, metrics_server

app = typer.Typer(help="gost-backup-vault: Encrypted backups with GOST support")

app.add_typer(init_repo.app, name="init")
app.add_typer(backup.app, name="backup")
app.add_typer(restore.app, name="restore")
app.add_typer(check.app, name="check")
app.add_typer(policy_wizard.app, name="policy-wizard")
app.add_typer(metrics_server.app, name="metrics-server")

if __name__ == "__main__":
    app()
