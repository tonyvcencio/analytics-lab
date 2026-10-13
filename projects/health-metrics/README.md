# Health Metrics Analytics

## Project Overview

Health Metrics Analytics is a cross platform data engineering and analytics project developed within the Analytics Lab.

The project collects system-health observations from laboratory
computers and analyzes operational performance over time.

## Project Objectives

1. Collect system-health metrics using Python.
2. Store observations in JSONL and PostgreSQL.
3. Automate data collection on Ichabod using systemd.
4. Analyze observations using DuckDB and SQL.
5. Visualize performance trends using Jupyter and Matplotlib.
6. Extend collection and analysis to additional machines.

## Laboratory Infrastructure

- Mac M4 Pro: Primary development and analytics workstation.
- Ichabod: Ubuntu Server metrics collection and storage.
- Nomad: Windows analytics and cross-platform validation.

## Data Architecture

The project uses a distributed collection and analysis architecture.

### Ichabod
- Collects system-health observations using Python and psutil.
- Stores observations locally in JSONL format.
- Executes collection automatically using a systemd timer.
- Will host PostgreSQL as the primary operational database.

### Mac M4 Pro
- Serves as the primary development environment.
- Retrieves observations from Ichabod.
- Uses DuckDB and SQL for analytical processing.
- Uses pandas, Jupyter, and Matplotlib for analysis and visualization.

### Nomad
- Provides a secondary development environment.
- Supports cross-platform validation and reproducibility testing.

### Version Control
- GitHub stores source code, configuration, and documentation.
- Generated observations and operational databases are excluded.

## Initial Metrics

- UTC timestamp
- Hostname
- CPU utilization
- Memory utilization
- Root filesystem utilization
- CPU temperature, when available
- System uptime

## Project Status

Version: 0.1

### Completed
- Created the Python system-health collector.
- Implemented JSONL observation storage.
- Validated collection on macOS and Ubuntu Server.
- Deployed the collector to Ichabod.
- Configured automated collection using systemd.
- Verified successful unattended collection.

### Next Milestones
- Deploy PostgreSQL on Ichabod.
- Design the initial database schema.
- Implement validated PostgreSQL ingestion.
- Query collected observations using DuckDB.
- Build the first Jupyter analytics notebook.
- Add automated data-quality checks.