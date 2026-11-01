# Health Metrics Analytics

## Project Overview

Health Metrics Analytics is a cross-platform data engineering and analytics
project developed within the Analytics Lab.

The project collects system-health observations from laboratory computers,
stores them in structured formats, and supports the analysis of operational
performance over time.

The initial deployment operates on Ichabod, an Ubuntu Server, with development
and analytical workloads performed on Carroll's M4 Pro.

## Project Objectives

1. Collect system-health metrics using Python and psutil.
2. Store observations in JSONL and PostgreSQL.
3. Automate data collection and ingestion using systemd.
4. Analyze observations using DuckDB and SQL.
5. Visualize performance trends using Jupyter and Matplotlib.
6. Extend collection and analysis to additional laboratory machines.

## Laboratory Infrastructure

- **Carroll (M4 Pro):** Primary development and analytics workstation.
- **Ichabod:** Ubuntu Server responsible for collection, ingestion, and storage.
- **Hopper:** Windows analytics workstation and cross-platform validation environment.

## Data Architecture

The project uses a distributed collection and analysis architecture.

### Ichabod

Ichabod hosts the operational data pipeline.

Responsibilities:

- Collects system-health observations using Python and psutil.
- Stores raw observations locally in JSONL format.
- Executes collection automatically using a systemd timer.
- Hosts PostgreSQL 16 as the operational database.
- Ingests JSONL observations into PostgreSQL using Psycopg.
- Executes database ingestion automatically using a separate systemd timer.
- Prevents duplicate database records using a unique constraint and
  PostgreSQL's `ON CONFLICT DO NOTHING`.

### Automated Data Pipeline

The initial production workflow is:

```text
Ichabod
   |
   v
Python + psutil
   |
   v
System Health Collector
   |
   | systemd timer (~5 minutes)
   v
observations.jsonl
   |
   v
PostgreSQL Ingestion
   |
   | systemd timer (every 5 minutes)
   v
PostgreSQL 16
   |
   v
health_metrics
   |
   v
public.system_observations
```

Collection and ingestion operate independently.

If database ingestion fails, the collector continues writing observations
to JSONL. Subsequent successful ingestion runs can recover observations
that were not previously inserted.

The ingestion process currently rereads the JSONL file during each execution.
Incremental ingestion is a planned optimization.

### Automated Services

| Service | Timer | Frequency | Purpose |
|---|---|---|---|
| health-metrics.service | health-metrics.timer | Approximately 5 minutes | Collect system observations |
| health-metrics-ingest.service | health-metrics-ingest.timer | Every 5 minutes | Ingest observations into PostgreSQL |
| health-metrics-backup.service | health-metrics-backup.timer | Daily at 03:30 UTC | Create and rotate PostgreSQL backups |

The ingestion timer uses the calendar schedule:

`OnCalendar=*-*-* *:02/5:00`

The collection and ingestion services run under the nonadministrative
`tony` Linux account.

The PostgreSQL backup service runs under the `postgres` operating-system
account. Its script and systemd configurations are owned by root.

### PostgreSQL Configuration

- PostgreSQL version: 16
- Database: `health_metrics`
- Primary table: `public.system_observations`
- Application role: `health_collector`
- Network binding: Localhost (`127.0.0.1`)
- Authentication: PostgreSQL password authentication using `.pgpass`
- Duplicate prevention: Unique constraint on hostname and UTC timestamp

The application role has restricted database privileges.

Database credentials are stored outside the Git repository.

### Carroll (M4 Pro)

Carroll serves as the primary development and analytical environment.

Analytical responsibilities:

- Connect securely to PostgreSQL through an SSH tunnel.
- Retrieve observations from Ichabod.
- Perform analytical processing using DuckDB and SQL.
- Analyze datasets using pandas and Jupyter.
- Visualize system performance using Matplotlib.

### Hopper

Hopper provides a secondary development environment.

Responsibilities:

- Cross-platform validation.
- Reproducibility testing.
- Future Windows system-health collection.
- Secondary analytical workloads.

### Version Control

GitHub stores:

- Python source code.
- PostgreSQL schema definitions.
- Systemd service and timer configurations.
- Project documentation.
- Dependency declarations.

Generated observations, operational databases, virtual environments,
and authentication credentials are excluded from version control.

## PostgreSQL Backup and Recovery

Health Metrics uses automated PostgreSQL backups to provide local
database recovery capability.

### Backup Architecture

Backups are created on Ichabod using PostgreSQL's `pg_dump` utility.

Configuration:

| Setting | Value |
|---|---|
| Database | `health_metrics` |
| Backup format | PostgreSQL custom archive |
| Compression | PostgreSQL custom-format compression |
| Backup directory | `/var/backups/health-metrics/` |
| Schedule | Daily at 03:30 UTC |
| Retention | Seven days for automated backups |
| Execution account | `postgres` |
| Scheduling | systemd service and timer |

The backup directory uses permissions `700`, and backup archives
use permissions `600`.

Database backups and credentials are excluded from Git.

### Backup Automation

The backup script is maintained at:

`backup/backup_health_metrics.sh`

The script:

1. Creates a timestamped PostgreSQL archive.
2. Writes the archive to a temporary file.
3. Validates the archive catalog using `pg_restore --list`.
4. Checks for an existing destination filename.
5. Moves the validated archive to its final filename.
6. Deletes automated archives older than seven days.
7. Reports execution results through the systemd journal.

Backup rotation runs only after a new archive is successfully created
and validated.

The original manually created archive,
`health_metrics_initial.dump`, is excluded from automated retention.

### Backup Service

The systemd configurations are maintained in:

`deployment/systemd/health-metrics-backup.service`

`deployment/systemd/health-metrics-backup.timer`

The timer uses:

`OnCalendar=*-*-* 03:30:00 UTC`

`Persistent=true`

The persistent timer allows systemd to execute a missed scheduled
backup when the timer becomes active again.

### Monitoring Backups

Check the timer:

```bash
systemctl status health-metrics-backup.timer

## Initial Metrics

The current collector records:

- UTC timestamp
- Hostname
- CPU utilization percentage
- Memory used (MB)
- Memory available (MB)
- Root filesystem utilization percentage
- System uptime (seconds)

### Planned Metrics

- CPU temperature, when available
- Disk read/write activity
- Network activity
- Additional system-health indicators

## Exploratory Data Analysis

The first analytical notebook examines system-health observations
collected from Ichabod.

The analysis includes:

- CPU utilization trends.
- Memory utilization trends.
- Disk utilization trends.
- Descriptive statistics.
- Missing-value analysis.

The initial dataset contained 577 observations with no missing values
in the seven analyzed columns.

The analysis identified low sampled CPU utilization, changes in memory
consumption, and a gradual increase in disk utilization.

These findings are preliminary because the observation period is short
and CPU measurements represent periodic samples rather than continuous
utilization.

**Notebook:** [System Health Exploration](notebooks/01_system_health_exploration.ipynb)

The notebook contains saved analytical outputs. Reexecuting its
database queries requires authorized access to Ichabod.

## Project Status

**Version:** 0.4
**Current Phase:** Automated Backup and Recovery Complete
**Last Updated:** October 18, 2026

### Completed

- Created the Python system-health collector.
- Implemented JSONL observation storage.
- Validated collection on macOS and Ubuntu Server.
- Deployed the collector to Ichabod.
- Configured automated collection using systemd.
- Verified successful unattended collection.
- Installed PostgreSQL 16 on Ichabod.
- Created the `health_metrics` database.
- Designed and implemented the `system_observations` schema.
- Configured restricted application database access.
- Implemented JSONL-to-PostgreSQL ingestion using Psycopg.
- Implemented duplicate prevention and idempotent ingestion.
- Verified automated PostgreSQL ingestion and queried 577 observations during initial analysis.
- Created a dedicated PostgreSQL ingestion systemd service.
- Configured automated ingestion using a systemd timer.
- Verified successful unattended PostgreSQL ingestion.
- Confirmed independent operation of collection and ingestion.
- Created a dedicated read-only PostgreSQL analytics role.
- Established secure remote PostgreSQL access using an SSH tunnel.
- Connected Carroll's analytics environment to Ichabod using Psycopg.
- Retrieved PostgreSQL observations into pandas.
- Created the first Jupyter exploratory analysis notebook.
- Visualized CPU, memory, and disk utilization over time.
- Calculated descriptive statistics for system-health metrics.
- Verified that the initial 577 observations contained no missing values.
- Published the analytics notebook to GitHub.
- Implemented PostgreSQL custom-format database backups.
- Validated backup restoration into a separate recovery database.
- Verified recovery of 1,381 historical observations.
- Created a dedicated PostgreSQL backup script.
- Implemented timestamped archives and temporary-file handling.
- Configured restricted backup directory and file permissions.
- Implemented seven-day automated backup retention.
- Tested retention using disposable backup files.
- Created a dedicated systemd backup service and timer.
- Verified successful backup execution through systemd.
- Enabled daily PostgreSQL backups at 03:30 UTC.

### Next Milestones

1. Validate timestamp ordering, sampling intervals, and duplicate records.
2. Implement ingestion monitoring and automated data-quality checks.
3. Establish off-machine PostgreSQL backup replication.
4. Optimize ingestion to process new observations incrementally.
5. Extend system-health collection to Hopper.
6. Expand the collected metrics and analytical capabilities.
7. Evaluate Power BI integration for operational monitoring.

## Development Roadmap

### Phase 1 — Data Collection
**Status: Complete**

Establish a portable Python collector and persistent JSONL storage.

### Phase 2 — Operational Database
**Status: Complete**

Deploy PostgreSQL, implement the database schema, and establish
reliable ingestion with duplicate prevention.

### Phase 3 — Pipeline Automation
**Status: Complete**

Automate both collection and PostgreSQL ingestion using independent
systemd services and timers.

### Phase 4 — Analytics and Visualization
**Status: Initial implementation complete**

Established secure, read-only PostgreSQL access from Carroll,
developed the first Jupyter notebook, and visualized system-health
trends using pandas and Matplotlib.

Additional analytical validation and reporting improvements remain planned.

### Phase 5 — Backup and Recovery
**Status: Complete — Local Backup Automation**

Implemented PostgreSQL custom-format backups, validated database
restoration, configured seven-day retention, and deployed a daily
systemd backup service and timer.

Off-machine backup replication and automated recovery testing
remain future improvements.

### Phase 6 — Monitoring and Expansion
**Status: Planned**

Implement data-quality monitoring, improve ingestion efficiency,
expand system metrics, and extend collection across laboratory machines.