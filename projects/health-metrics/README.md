# Health Metrics Analytics

## Project Overview

Health Metrics Analytics is a cross-platform data engineering and analytics
project developed within the Analytics Lab.

The project collects system-health observations from laboratory computers,
stores them in structured formats, and supports the analysis of operational
performance over time.

The initial deployment operates on Ichabod, an Ubuntu Server, with development
and analytical workloads performed on the Mac M4 Pro.

## Project Objectives

1. Collect system-health metrics using Python and psutil.
2. Store observations in JSONL and PostgreSQL.
3. Automate data collection and ingestion using systemd.
4. Analyze observations using DuckDB and SQL.
5. Visualize performance trends using Jupyter and Matplotlib.
6. Extend collection and analysis to additional laboratory machines.

## Laboratory Infrastructure

- **Mac M4 Pro:** Primary development and analytics workstation.
- **Ichabod:** Ubuntu Server responsible for collection, ingestion, and storage.
- **Nomad:** Windows analytics workstation and cross-platform validation environment.

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

The ingestion timer uses the calendar schedule:

`OnCalendar=*-*-* *:02/5:00`

Both services run under the nonadministrative `tony` Linux account.

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

### Mac M4 Pro

The Mac serves as the primary development and analytical environment.

Analytical responsibilities:

- Connect securely to PostgreSQL through an SSH tunnel.
- Retrieve observations from Ichabod.
- Perform analytical processing using DuckDB and SQL.
- Analyze datasets using pandas and Jupyter.
- Visualize system performance using Matplotlib.

### Nomad

Nomad provides a secondary development environment.

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

**Version:** 0.3
**Current Phase:** Initial Analytics and Visualization Complete
**Last Updated:** October 14, 2026

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
- Connected the Mac analytics environment to Ichabod using Psycopg.
- Retrieved PostgreSQL observations into pandas.
- Created the first Jupyter exploratory analysis notebook.
- Visualized CPU, memory, and disk utilization over time.
- Calculated descriptive statistics for system-health metrics.
- Verified that the initial 577 observations contained no missing values.
- Published the analytics notebook to GitHub.

### Next Milestones

1. Validate timestamp ordering, sampling intervals, and duplicate records.
2. Implement ingestion monitoring and automated data-quality checks.
3. Establish PostgreSQL backup and recovery procedures.
4. Optimize ingestion to process new observations incrementally.
5. Extend system-health collection to Nomad.
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

Established secure, read-only PostgreSQL access from the Mac,
developed the first Jupyter notebook, and visualized system-health
trends using pandas and Matplotlib.

Additional analytical validation and reporting improvements remain planned.

### Phase 5 — Monitoring and Expansion
**Status: Planned**

Implement data-quality monitoring, improve ingestion efficiency,
expand system metrics, and extend collection across laboratory machines.