# Project 003 — Operations Automation

**Analytics Lab | Atlas Realm Consulting**

**Status:** In Development  
**Primary Workstation:** Hopper (Windows)  
**Current Technologies:** Excel, VBA, Python, PowerShell
**Planned Technologies:** Power Query, SQL, Power BI

## Overview

Operations Automation is a modular reporting and workflow automation project designed to help organizations reduce manual administrative work, monitor operational deadlines, identify reporting discrepancies, and improve data quality.

The project uses fictional business scenarios and synthetic datasets to demonstrate practical automation solutions that can be adapted to different industries.

Development is Microsoft-first, with Excel serving as the initial reporting and automation platform.

## Business Objectives

- Reduce repetitive manual reporting tasks.
- Improve visibility into aging workloads and overdue items.
- Identify deadline conflicts and operational exceptions.
- Validate documentation and communication activity.
- Improve reporting consistency and reliability.
- Demonstrate accessible automation solutions for small and midsize organizations.

## Planned Modules

| Module | Purpose | Status |
|---|---|---|
| Aging & Backlog Monitor (Meridian) | Daily reconciliation, aging, overdue monitoring, and exception reporting | Completed - v1.0 |
| Deadline Coordination | Reconcile deadlines and identify SLA risks | Planned |
| Documentation Quality Audit | Identify incomplete or inconsistent activity notes | Planned |
| Communication Tracker | Monitor required updates and follow-ups | Planned |
| Duplicate Detection | Flag duplicate or inconsistent records | Planned |
| Assignment Support | Assist workload distribution | Planned |

## Development Environment

### Hopper — Primary Development
- Microsoft Excel and VBA
- Power Query
- Power BI Desktop
- PowerShell
- Windows-based validation

### Carroll — Supporting Development
- Python
- Synthetic data generation
- Advanced transformations and testing

### Ichabod — Optional Infrastructure
- PostgreSQL
- Scheduled processing
- Logging and monitoring

## Repository Structure

```text
operations-automation/
├── data/       # Synthetic datasets
├── docs/       # Charter and technical documentation
├── excel/      # Excel workbooks and VBA modules
├── outputs/    # Generated reports
├── powerbi/    # Power BI reports
├── scripts/    # Automation utilities
├── sql/        # Database queries
└── tests/      # Validation and regression tests
```

## Development Roadmap

1. Project initialization and repository setup.
2. Aging Monitor MVP.
3. Deadline Coordination module.
4. Documentation and communication validation.
5. Integration testing and portfolio demonstration.
6. Evaluation of reusable commercial offerings.

## Data and Intellectual Property

All project datasets will be synthetic. Business rules, automation logic, and reporting tools will be independently developed.

No confidential employer information, proprietary code, internal documents, or production data will be used.

## Meridian Aging Monitor — Quick Start

### Requirements

- Windows with Microsoft Excel (desktop version with VBA support)
- Python 3 with pandas installed
- PowerShell or another command-line terminal

### Generate Synthetic Data

From the `analytics-lab` repository root:

```powershell
python -m pip install pandas
python projects/operations-automation/scripts/generate_workorders.py --report-date 2026-11-02
```

The generator creates the required CSV files in:

`projects/operations-automation/data/daily-exports/`

Required reporting inputs:

- `External_Open.csv`
- `Internal_Open.csv`

The generator also creates `Expected_Reconciliation.csv` for independent validation. This file is not imported by the Excel application.

### Run the Excel Report

1. Open `projects/operations-automation/excel/Meridian_Aging_Monitor.xlsm` in Microsoft Excel.
2. Enable macros if permitted and the workbook is trusted.
3. Enter the reporting date in `Summary!K2` (November 2, 2026, for the example dataset).
4. Save the workbook.
5. Click **Run Daily Report**.
6. Review the Summary, Aging_Detail, and Exceptions worksheets.
7. Save the workbook after a successful refresh.

For the November 2 test dataset, the expected results are **475 active work orders, 31 source discrepancies, and 199 overdue work orders**.

### Recovery

Before each refresh, Meridian creates `Meridian_PreRefresh_Backup.xlsm` in the `excel` directory.

The backup is overwritten on subsequent runs. Recovery is manual, so preserve a separate copy before attempting restoration.

For detailed business rules, validation results, and limitations, see [Aging Monitor Technical Documentation](docs/modules/aging-monitor.md).

## Documentation

See [Project Charter](docs/project-charter.md) for the formal project objectives, scope, deliverables, and success criteria.

## Project Status

Project 003 remains in active development.

The first module, **Meridian Daily Aging & Reconciliation Monitor**, has completed v1.0 validation and is ready for release.

The Excel/VBA application has completed three-day functional testing using synthetic operational datasets. Reconciliation results were validated across October 31–November 2, 2026, and November 2 aging and overdue calculations were independently verified using Python.

The module includes CSV validation, a consolidated aging report, reconciliation exceptions, an Excel dashboard, and a pre-refresh recovery backup.

See [Meridian Aging Monitor Documentation](docs/modules/aging-monitor.md) for operating instructions, validation results, and known limitations.

Future modules will address deadline coordination, documentation quality, communication tracking, duplicate detection, and assignment support.