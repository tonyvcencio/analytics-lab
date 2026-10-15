# Analytics Lab

A multi-system analytics environment for developing and demonstrating
practical solutions in data engineering, business intelligence,
automation, and data visualization.

The laboratory combines Windows, macOS, and Linux systems to build
end-to-end analytical workflows using Python, SQL, PostgreSQL,
Power BI, and Git.

## Systems

### Nomad

Windows analytics workstation focused on:

- Power BI
- Excel
- Python
- SQL
- Git
- PowerShell
- Remote Linux administration

### Mac

macOS analytics and development workstation focused on:

- Python
- Unix Tooling
- Git
- Development workflows
- Infrastructure preparation

### Ichabod

Headless Ubuntu Linux server supporting:

- PostgreSQL databases
- Automated Python workloads
- Scheduled data collection and ingestion
- Remote analytics and administration
- Future containerized services

### Gimperihno

Secondary non-critical storage for testing and expendable workloads.

## Architecture

Nomad and Mac serve as development and administration clients.

Ichabod provides Linux-based server services and remote compute/storage capabilities.

GitHub acts as the shared version-control layer across the environment.

## Featured Projects

### 001 — Health Metrics Analytics

**Status:** Initial analytics implementation complete (v0.3)

An automated system-health monitoring and analytics pipeline
built using Python, PostgreSQL, Linux systemd, pandas,
Jupyter, and Matplotlib.

The project demonstrates:

- Automated data collection and ingestion
- Relational database design
- Secure remote database access
- Exploratory data analysis
- Operational performance visualization
- Cross-platform development

[Explore Health Metrics Analytics](projects/health-metrics/README.md)

[View the Jupyter Notebook](projects/health-metrics/notebooks/01_system_health_exploration.ipynb)

### 002 — Small Business Performance Analytics

**Status:** Planned

A business intelligence project focused on sales, profitability,
customer behavior, and operational performance.

Planned technologies include Python, PostgreSQL, SQL, and Power BI.
