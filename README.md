gost-backup-vault 🔐
🇬🇧 English | 🇷🇺 @README.ru.md

CILicense: Apache-2.0Python 3.10+

Overview
gost-backup-vault is a Python 3.10+ CLI wrapper around restic, borg, and tar that adds an optional GOST (Magma, Kuznyechik) encryption layer, YAML-based policies, and Prometheus metrics for Linux backup jobs. It targets Linux admins, DevOps, and security teams that need predictable, auditable backups with Russian cryptography profiles. The tool validates policies, runs backups, and exposes metrics so you can plug it into cron/systemd timers and observability stacks.

Key features
Single CLI entrypoint gost-backup with init, backup, restore (prototype), check, metrics-server, policy-wizard.
YAML policies validated by Pydantic schema plus policy checks (unique job names, schedules, paths).
Multiple backends: restic, borg, or tar archives with optional extra args.
Optional GOST crypto layer (Magma/Kuznyechik) via pluggable providers; pass-through mode when crypto is handled externally.
Prometheus exporter exposing gost_backup_* metrics (status, duration, size, failures).
Interactive policy wizard for quick config generation.
Fits cron/systemd timers; everything is CLI-first with clear exit codes.
Typed Python code with tests, linting, and CI workflows.
Architecture / Components
Typer-based CLI → Config loader → Policy validator → Executor → Backend (restic | borg | tar).
Crypto provider (default local_software stub) can wrap streams for GOST encryption or pass-through.
Metrics mapper updates Prometheus gauges/counters; metrics server publishes /metrics via prometheus_client.
Storage target depends on backend: restic/borg repository or a tar archive directory.
ASCII view:

[YAML config] -> [ConfigLoader + PolicyValidator] -> [Executor]
                    |-> [Backend: restic | borg | tar] -> [Repo/Storage]
                    |-> [Crypto provider]
                    |-> [MetricsMapper] -> [/metrics for Prometheus/Grafana]
Requirements
Linux host (POSIX; uses fcntl), tested in CI on Ubuntu-latest.
Python 3.10+ with pip/venv.
Backend binaries in PATH depending on choice: restic, borg, tar.
Access to backup sources (often requires root/sudo) and writable repository/storage path.
Optional crypto tooling if you use real GOST encryption (e.g., GOST-capable OpenSSL or external provider).
Network: outbound access to remote repositories if used; inbound access to port 9105 (metrics) as needed.
Notes / Assumptions
Repository credentials (e.g., RESTIC_PASSWORD, RESTIC_PASSWORD_FILE, BORG_PASSPHRASE) are provided via environment variables or external secret stores.
Scheduling is handled by your scheduler (cron/systemd/k8s); schedule in YAML is descriptive metadata.
Replace sample paths/domains with your own (<YOUR_SERVER_IP>, <YOUR_STORAGE_PATH>).
The bundled crypto provider is a software stub; use a production-grade provider plugin for real GOST compliance.
Quick start (TL;DR)
Clone and install:
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
Create a minimal policy file:
cat <<'EOF' > gost-backup.yaml
node:
  id: node-1
  os: debian-12
backend:
  type: restic
  repo: /var/backups/restic-repo
  extra_args: []
crypto_profile:
  name: gost-magma
  gost_cipher: magma
  mode: wrap_key
  provider: local_software
jobs:
  - name: etc-and-home
    paths:
      - /etc
      - /home
    exclude:
      - /home/*/.cache
    schedule: "daily@02:00"
    retention:
      type: tiered
      daily: 7
      weekly: 4
      monthly: 6
EOF
Export backend secrets (example for restic):
export RESTIC_PASSWORD=<SET_STRONG_PASSWORD>
Initialize repository and run a job:
gost-backup init --config gost-backup.yaml
gost-backup backup --config gost-backup.yaml --job etc-and-home
Expose metrics:
gost-backup metrics-server --config gost-backup.yaml --listen 0.0.0.0:9105
# Scrape: curl http://<YOUR_SERVER_IP>:9105/metrics
Installation
Ubuntu / Debian
sudo apt update
sudo apt install -y restic borgbackup tar python3-venv python3-pip
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv /opt/gost-backup-venv
source /opt/gost-backup-venv/bin/activate
pip install -U pip
pip install .
RHEL / Rocky / Alma
sudo dnf install -y restic borgbackup tar python3-pip python3-virtualenv
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv /opt/gost-backup-venv
source /opt/gost-backup-venv/bin/activate
pip install -U pip
pip install .
From source (editable for development)
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]   # installs lint/test tooling
Configuration
Main config is YAML (schema in src/gost_backup_vault/config/schema.yaml). Key fields:

node:
  id: node-1              # logical node ID
  os: debian-12           # optional
backend:
  type: restic            # restic | borg | tar
  repo: /var/backups/restic-repo
  extra_args: ["--host", "node-1"]  # optional backend flags
crypto_profile:
  name: gost-magma
  gost_cipher: magma      # magma | kuznyechik | none
  mode: wrap_key          # wrap_key | full_encrypt
  provider: local_software
jobs:
  - name: etc-and-home
    paths: ["/etc", "/home"]
    exclude: ["/home/*/.cache"]
    schedule: "daily@02:00"          # metadata for your scheduler
    retention:
      type: tiered
      daily: 7
      weekly: 4
      monthly: 6
Environment variables:

Restic: RESTIC_PASSWORD or RESTIC_PASSWORD_FILE, repository URLs (local path, s3:, rclone:) as needed.
Borg: BORG_PASSPHRASE or BORG_PASSCOMMAND.
Tar: only needs a writable destination directory.
Use gost-backup policy-wizard --output gost-backup.yaml for an interactive generator.

Usage & common tasks
Validate config without side effects:
gost-backup check --config gost-backup.yaml --dry-run
Run a specific job:
gost-backup backup --config gost-backup.yaml --job etc-and-home
Initialize backend repository (idempotent):
gost-backup init --config gost-backup.yaml
Start metrics exporter:
gost-backup metrics-server --config gost-backup.yaml --listen 0.0.0.0:9105
Generate a new policy:
gost-backup policy-wizard --output my-policy.yaml
Example systemd timer (replace <CONFIG_PATH>):
# /etc/systemd/system/gost-backup.service
[Unit]
Description=gost-backup-vault job
[Service]
Type=oneshot
Environment=RESTIC_PASSWORD=<SECRET>
ExecStart=/opt/gost-backup-venv/bin/gost-backup backup --config <CONFIG_PATH> --job etc-and-home

# /etc/systemd/system/gost-backup.timer
[Unit]
Description=Run gost-backup-vault daily
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
[Install]
WantedBy=timers.target
sudo systemctl daemon-reload
sudo systemctl enable --now gost-backup.timer
Restore command is stubbed in this prototype; verify manually with backend tools where needed.
Update / upgrade
Pull latest code and reinstall:
git pull
pip install -U .
Re-run validation:
gost-backup check --config gost-backup.yaml --dry-run
Restart timers/services after upgrades if used.
Logs, monitoring, troubleshooting
CLI logs to stdout/stderr; check exit codes.
If run via systemd: journalctl -u gost-backup.service -f.
Metrics: curl http://localhost:9105/metrics and inspect gost_backup_*.
Common issues:
Missing backend binary: ensure restic/borg/tar in PATH.
Repo not initialized or password mismatch: run gost-backup init and verify RESTIC_PASSWORD/BORG_PASSPHRASE.
Permission denied on source paths: run as root or grant read access.
Port in use for metrics: change --listen address/port.
Security notes
Use strong, rotated passwords and store them outside the config file.
Restrict metrics and repository access via firewall/VPN/reverse proxy.
Do not expose backup repositories or plaintext configs to the Internet; set strict filesystem permissions (e.g., 600 for configs).
Prefer dedicated service accounts with least privilege for running backups.
Validate any external crypto provider you load; audit binaries in your path.
Project structure
src/gost_backup_vault/     # CLI, backends, crypto provider loader, policy/metrics code
scripts/                   # lint, test, perf, security helpers
tests/                     # unit and integration tests
.github/workflows/         # CI and security scans
pyproject.toml             # packaging and tooling configuration
LICENSE                    # Apache-2.0 license
Roadmap / Plans
Full restore workflows and snapshot listing across backends.
Retention enforcement (prune/forget) per backend.
Remote storage helpers (SSH/S3/Rclone) and secrets handling.
Additional crypto provider plugins with certified GOST toolchains.
Packaging (deb/rpm), optional Docker/systemd units, and richer metrics/dashboards.
Contributing
Open issues or feature requests via GitHub.
Fork and submit PRs; keep changes small and documented.
Run quality checks before submitting:
bash scripts/lint.sh
bash scripts/test.sh
Follow existing style: type hints, Ruff/Mypy clean, YAML with consistent indentation.
License
Apache License 2.0. See LICENSE.

Author and commercial support
Author: Ranas Mukminov.
For production-grade setup, audits, and support, visit https://run-as-daemon.ru or reach out via the GitHub profile.
