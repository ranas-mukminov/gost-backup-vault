# gost-backup-vault 🔐

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

![CI](https://github.com/ranas-mukminov/gost-backup-vault/workflows/CI/badge.svg) ![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg) ![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

## Overview

**gost-backup-vault** is a Python 3.10+ CLI wrapper around `restic`, `borg`, and `tar` that adds an optional GOST (Magma, Kuznyechik) encryption layer, YAML-based backup policies, and Prometheus metrics for Linux backup workflows. It targets Linux system administrators, DevOps engineers, and security teams that require predictable, auditable, and policy-driven backup solutions with support for Russian cryptographic standards. The tool validates backup policies, executes backup jobs, and exposes observability metrics for integration with cron/systemd timers and monitoring stacks like Prometheus and Grafana.

## Key Features

- **Single CLI entrypoint** (`gost-backup`) with subcommands: `init`, `backup`, `restore` (prototype), `check`, `metrics-server`, `policy-wizard`
- **YAML-based policies** validated by Pydantic schema with comprehensive policy checks (unique job names, valid schedules, path existence)
- **Multiple backup backends**: restic, borg, or tar archives with optional extra arguments and pass-through support
- **Optional GOST crypto layer**: Magma/Kuznyechik encryption via pluggable crypto providers or pass-through mode for externally handled encryption
- **Prometheus metrics exporter** exposing `gost_backup_*` metrics (job status, duration, backup size, failure counters) on configurable port
- **Interactive policy wizard** for quick configuration generation with step-by-step CLI prompts
- **Cron and systemd timer friendly**: CLI-first design with clear exit codes for scheduler integration
- **Production-grade Python codebase**: fully typed, tested with pytest, linted with Ruff/Mypy, CI/CD workflows for quality assurance

## Architecture / Components

The tool follows a modular pipeline architecture:

```
[YAML config] → [ConfigLoader + PolicyValidator] → [Executor]
                    ├→ [Backend: restic | borg | tar] → [Repository/Storage]
                    ├→ [Crypto Provider: GOST wrapper or pass-through]
                    └→ [MetricsMapper] → [/metrics endpoint for Prometheus/Grafana]
```

**Components**:

- **ConfigLoader**: Parses YAML configuration and validates against Pydantic schema
- **PolicyValidator**: Checks for unique job names, valid schedules, path accessibility, retention policies
- **Executor**: Orchestrates backup workflow with selected backend and crypto provider
- **Backends**: Pluggable adapters for `restic`, `borg`, or `tar` with customizable arguments
- **Crypto Provider**: Abstraction layer for GOST encryption (Magma/Kuznyechik) or transparent pass-through
- **MetricsMapper**: Updates Prometheus gauges/counters; metrics server publishes `/metrics` endpoint via `prometheus_client`

**Storage**: Depends on selected backend — restic/borg repository (`file://`, `s3://`, `rclone:`) or tar archive directory.

## Requirements

- **Operating system**: Linux host (POSIX-compliant; uses `fcntl`), tested on Ubuntu 22.04/24.04 in CI
- **Python**: Python 3.10+ with pip and venv support
- **Backend binaries** (depending on chosen backend):
  - `restic` (tested with 0.16+)
  - `borgbackup` (tested with 1.2+)
  - `tar` (GNU tar, usually pre-installed)
- **Permissions**: Access to backup source paths (often requires `root` or `sudo`) and writable repository/storage destination
- **Optional crypto tooling**: GOST-capable OpenSSL or external crypto provider plugin for production GOST encryption
- **Network**:
  - Outbound access to remote repositories if using cloud/remote backends (S3, SFTP, rclone)
  - Inbound access to metrics port (default 9105) if exposing metrics to Prometheus

### Notes / Assumptions

- Repository credentials (`RESTIC_PASSWORD`, `RESTIC_PASSWORD_FILE`, `BORG_PASSPHRASE`) must be provided via environment variables or external secret stores
- Backup scheduling is handled by external schedulers (cron, systemd timers, Kubernetes CronJobs); `schedule` field in YAML is metadata for documentation
- Replace sample placeholders in examples (`<YOUR_SERVER_IP>`, `<YOUR_STORAGE_PATH>`, `<YOUR_DOMAIN>`) with your actual values
- The bundled crypto provider is a software stub for development; use a production-grade GOST provider plugin with certified toolchains for compliance

## Quick Start (TL;DR)

**1. Clone and install**:

```bash
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
```

**2. Create a minimal policy file**:

```bash
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
```

**3. Export backend credentials** (example for restic):

```bash
export RESTIC_PASSWORD=<SET_STRONG_PASSWORD>
```

**4. Initialize repository and run backup job**:

```bash
gost-backup init --config gost-backup.yaml
gost-backup backup --config gost-backup.yaml --job etc-and-home
```

**5. Expose metrics** (optional):

```bash
gost-backup metrics-server --config gost-backup.yaml --listen 0.0.0.0:9105
# Scrape metrics: curl http://<YOUR_SERVER_IP>:9105/metrics
```

## Installation

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y restic borgbackup tar python3-venv python3-pip
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv /opt/gost-backup-venv
source /opt/gost-backup-venv/bin/activate
pip install -U pip
pip install .
```

### RHEL / Rocky / Alma Linux

```bash
sudo dnf install -y restic borgbackup tar python3-pip python3-virtualenv
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv /opt/gost-backup-venv
source /opt/gost-backup-venv/bin/activate
pip install -U pip
pip install .
```

### From Source (Editable for Development)

```bash
git clone https://github.com/ranas-mukminov/gost-backup-vault.git
cd gost-backup-vault
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]   # installs lint/test tooling (pytest, ruff, mypy)
```

## Configuration

Main configuration is YAML-based (schema defined in `src/gost_backup_vault/config/schema.yaml`). Key sections:

```yaml
node:
  id: node-1              # Logical node identifier
  os: debian-12           # Optional OS metadata

backend:
  type: restic            # restic | borg | tar
  repo: /var/backups/restic-repo
  extra_args: ["--host", "node-1"]  # Optional backend-specific flags

crypto_profile:
  name: gost-magma
  gost_cipher: magma      # magma | kuznyechik | none
  mode: wrap_key          # wrap_key | full_encrypt
  provider: local_software

jobs:
  - name: etc-and-home
    paths: ["/etc", "/home"]
    exclude: ["/home/*/.cache"]
    schedule: "daily@02:00"          # Metadata for your scheduler
    retention:
      type: tiered
      daily: 7
      weekly: 4
      monthly: 6
```

**Environment variables**:

- **Restic**: `RESTIC_PASSWORD` or `RESTIC_PASSWORD_FILE`, repository URLs (local path, `s3://`, `rclone://`) as needed
- **Borg**: `BORG_PASSPHRASE` or `BORG_PASSCOMMAND`
- **Tar**: Only requires a writable destination directory

**Generate config interactively**:

```bash
gost-backup policy-wizard --output gost-backup.yaml
```

## Usage & Common Tasks

**Validate config without side effects**:

```bash
gost-backup check --config gost-backup.yaml --dry-run
```

**Run a specific backup job**:

```bash
gost-backup backup --config gost-backup.yaml --job etc-and-home
```

**Initialize backend repository** (idempotent):

```bash
gost-backup init --config gost-backup.yaml
```

**Start Prometheus metrics exporter**:

```bash
gost-backup metrics-server --config gost-backup.yaml --listen 0.0.0.0:9105
```

**Generate a new policy**:

```bash
gost-backup policy-wizard --output my-policy.yaml
```

### Systemd Timer Integration

Example systemd service and timer (replace `<CONFIG_PATH>` and `<SECRET>`):

```ini
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
```

Enable and start timer:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gost-backup.timer
```

**Note**: Restore command is currently a prototype; verify restoration manually using backend-native tools (`restic restore`, `borg extract`, `tar xf`) as needed.

## Update / Upgrade

Pull latest code and reinstall:

```bash
cd gost-backup-vault
git pull
pip install -U .
```

Re-run validation after upgrade:

```bash
gost-backup check --config gost-backup.yaml --dry-run
```

Restart systemd timers/services if applicable:

```bash
sudo systemctl restart gost-backup.timer
```

## Logs, Monitoring, Troubleshooting

**Logs**:

- CLI logs to stdout/stderr; check exit codes for success/failure
- If run via systemd: `journalctl -u gost-backup.service -f`
- Backend-specific logs via `restic` or `borg` verbose flags in `extra_args`

**Metrics**:

```bash
curl http://localhost:9105/metrics
```

Metrics include `gost_backup_job_status`, `gost_backup_duration_seconds`, `gost_backup_size_bytes`, `gost_backup_failures_total`.

**Common Issues**:

| Issue | Solution |
|-------|----------|
| Missing backend binary | Ensure `restic`, `borg`, or `tar` is in `PATH` |
| Repository not initialized or password mismatch | Run `gost-backup init` and verify `RESTIC_PASSWORD`/`BORG_PASSPHRASE` |
| Permission denied on source paths | Run as `root` or grant read access to service account |
| Port in use for metrics | Change `--listen` address/port (e.g., `--listen 0.0.0.0:9106`) |
| Policy validation errors | Run `gost-backup check --dry-run` and fix YAML syntax/logic |

## Security Notes

- **Strong passwords**: Use strong, randomly generated passwords for repositories and rotate them periodically
- **Secret management**: Store passwords outside config files (environment variables, secret managers, systemd credentials)
- **Access control**: Restrict metrics and repository access via firewall rules, VPN, or reverse proxy authentication
- **File permissions**: Set strict permissions on config files (`chmod 600 gost-backup.yaml`)
- **Service accounts**: Run backup jobs with dedicated service accounts using least privilege principle
- **Crypto providers**: Validate and audit any external crypto provider plugins before production use
- **Do not expose** backup repositories or plaintext configs to the public Internet

## Project Structure

```
src/gost_backup_vault/     # CLI, backends, crypto provider loader, policy/metrics code
  ├── cli/                 # Typer commands (backup, restore, init, check, metrics-server, policy-wizard)
  ├── backends/            # restic, borg, tar backend implementations
  ├── crypto/              # Crypto provider abstraction and local stub
  ├── config/              # YAML schema and config loader
  ├── policy/              # Policy validator and generator
  ├── metrics/             # Prometheus metrics mapper and server
  ├── domain/              # Domain models (Job, BackupResult, etc.)
  └── runner/              # Execution orchestrator
scripts/                   # lint, test, perf, security scan helpers
tests/                     # unit and integration tests (pytest)
.github/workflows/         # CI (lint, test) and security scans (bandit, safety)
pyproject.toml             # packaging and tooling configuration
LICENSE                    # Apache-2.0 license
LEGAL.md                   # Legal disclaimers and compliance notes
```

## Roadmap / Plans

- **Full restore workflows**: Snapshot listing, selective restore, cross-backend restore
- **Retention enforcement**: Automated prune/forget operations per backend with policy-driven rules
- **Remote storage helpers**: Pre-configured templates for SSH, S3, Rclone backends with credential management
- **Certified GOST providers**: Integration with certified GOST crypto toolchains (hardware HSM, commercial СКЗИ)
- **Packaging**: Debian/RPM packages, Docker images, official systemd units
- **Rich metrics and dashboards**: Pre-built Grafana dashboards, alerting rules, anomaly detection

## Contributing

- Open issues or feature requests via [GitHub Issues](https://github.com/ranas-mukminov/gost-backup-vault/issues)
- Fork the repository and submit PRs; keep changes small, focused, and well-documented
- **Run quality checks before submitting**:

  ```bash
  bash scripts/lint.sh
  bash scripts/test.sh
  ```

- **Code style**: Follow existing conventions — type hints everywhere, Ruff/Mypy clean, YAML with consistent indentation
- **Tests**: Add unit/integration tests for new features; maintain test coverage

## License

Apache License 2.0. See [LICENSE](LICENSE).

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)

For production-grade setup, infrastructure audits, GOST compliance consulting, and ongoing support, visit [https://run-as-daemon.ru](https://run-as-daemon.ru) (Russian) or contact the author via [GitHub profile](https://github.com/ranas-mukminov).

Commercial services include:

- Production deployment and hardening
- Custom crypto provider integration (HSM, certified СКЗИ)
- Backup policy design and compliance audits
- Monitoring stack integration (Prometheus/Grafana)
- DevOps/SRE consulting for backup workflows
