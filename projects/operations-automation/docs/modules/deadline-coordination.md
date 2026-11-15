
# Meridian Deadline Coordination

**Project:** 003 — Operations Automation
**Module:** 2 — Deadline Coordination
**Release:** v1.0
**Status:** Release candidate

## Overview

Meridian Deadline Coordination is an Excel/VBA reporting
solution for monitoring operational deadlines across two
independent work-order systems.

The application reconciles external and internal records,
identifies conflicting or missing deadlines, classifies
urgency, and generates a prioritized action queue.

The solution uses synthetic property-services data and
demonstrates operational reporting, data validation,
exception management, and workflow automation.

## Architecture

- Python generates reproducible synthetic CSV datasets.
- Excel/VBA imports and validates both source exports.
- Reconciliation creates one record per unique work order.
- Deadline calculations determine urgency.
- Action Queue prioritizes records requiring attention.
- Exceptions identifies reconciliation discrepancies.
- Summary provides operational metrics and one-click refresh.

## Business Rules

### DC-001 — Deadline Reconciliation

Use the earliest valid deadline from the external and
internal sources as the monitoring deadline.

Flag conflicting dates without modifying source values.

### DC-002 — Active Work Orders

Include the union of work orders appearing in either
source export.

A missing record from one source does not establish closure.

### DC-003 — Deadline Classification

Classify deadlines relative to the reporting date:

| Classification | Days Remaining |
|---|---|
| Overdue | Less than 0 |
| Due Today | 0 |
| Immediate | 1–2 |
| Approaching | 3–5 |
| On Track | 6 or more |
| Undetermined | No valid deadline |

The warning window is five calendar days.

### DC-004 — Action Queue Eligibility

Include work orders that are overdue, due within five
calendar days, or have a reconciliation exception.

Exclude nonexception work orders outside the warning window.

Each work order appears only once.

### DC-005 — Queue Prioritization

Sort Action Queue records by:

1. Queue urgency priority, ascending.
2. Monitoring deadline, earliest first.
3. Exception flags, flagged records first.
4. WorkOrderID, ascending.

## Workbook Worksheets

| Worksheet | Purpose |
|---|---|
| Summary | Dashboard and refresh button |
| External_Data | Validated external source records |
| Internal_Data | Validated internal source records |
| Deadline_Detail | Reconciled work-order detail |
| Action_Queue | Prioritized operational follow-up |
| Exceptions | Records requiring reconciliation review |

## Requirements

- Windows with desktop Microsoft Excel supporting VBA macros.
- Python 3 with the dependencies used by the analytics-lab repository.
- Local copy of the analytics-lab repository.
- Macros enabled for the trusted workbook.

## Generate Synthetic Data

From the repository root:

```powershell
.\.venv\Scripts\python.exe `
    projects\operations-automation\scripts\deadline-coordination\generate_deadlines.py `
    --report-date 2026-11-06
```

The generator creates:

- External_Deadlines.csv
- Internal_Deadlines.csv
- Expected_Deadlines.csv

These files are stored under:

`projects/operations-automation/data/deadline-coordination/`

Generated data is excluded from Git.

## Run the Workbook

Open:

`projects/operations-automation/excel/deadline-coordination/Meridian_Deadline_Coordination.xlsm`

1. Confirm Summary!B3 contains the intended reporting date.
2. Click **Refresh Deadline Report**.
3. Review Summary for operational totals.
4. Use Action_Queue for prioritized follow-up.
5. Use Exceptions to investigate discrepancies.

The workbook expects the repository directory structure
to remain intact because CSV imports use relative paths.

The reporting date is controlled by Summary!B3 and is
not automatically changed by the CSV generator.

## Validation Reference

Using reporting date 2026-11-06:

| Metric | Expected |
|---|---:|
| External records | 17 |
| Internal records | 18 |
| Unique active work orders | 20 |
| Overdue | 4 |
| Due Today | 2 |
| Immediate | 2 |
| Approaching | 5 |
| On Track | 4 |
| Undetermined | 3 |
| Deadline conflicts | 3 |
| Unmatched records | 5 |
| Missing deadlines | 3 |
| Action Queue | 18 |
| Exceptions | 8 |

## Validation and Recovery

The importer validates:

- Source-file existence.
- Expected CSV headers.
- Duplicate and blank WorkOrderIDs.
- ISO-formatted deadline values.
- Required LastUpdated dates.
- CSV field counts and quotation syntax.

Before modifying source data, the refresh controller
creates a workbook backup and captures worksheet snapshots.

If a refresh fails after modifications begin, the controller
attempts to restore the previous worksheet contents.

Recovery tests included changed-data imports, forced
failures, extra-row restoration, and dashboard integrity
checks.

The Last Refresh timestamp updates only after successful
completion.

## Known Limitations

- CSV input expects five fields per source record.
- Embedded line breaks inside quoted CSV fields are
  unsupported.
- The current workbook is designed for the documented
  repository structure.
- The reference reporting date is fixed for demonstration;
  users must update it when changing the reporting period.
- The solution uses synthetic data and does not connect
  directly to live property-management systems.

## Release Notes

Version 1.0 includes source reconciliation, deadline
classification, exception reporting, prioritized action
queues, input validation, automated recovery, and a
one-click Excel dashboard.
