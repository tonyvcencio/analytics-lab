# Module 001 — Meridian Daily Aging & Reconciliation Monitor

**Project:** 003 — Operations Automation  
**Company:** Meridian Property Services (fictional)  
**Primary Platform:** Microsoft Excel / VBA  
**Development Workstation:** Hopper (Windows)
**Status:** Completed - v1.0
**Validation Period:** October 31–November 2, 2026

## 1. Purpose

Automate the daily reconciliation of outstanding maintenance work orders across two operational systems and produce a consolidated aging and exception report.

The monitor identifies discrepancies between the two systems, calculates work-order aging, flags overdue requests, and presents operational metrics through an Excel dashboard.

## 2. Business Environment

Meridian Property Services operates two fictional systems:

- **Property Management System (External):** Originates maintenance requests and maintains its open-work-order population.
- **Maintenance Operations System (Internal):** Tracks assigned maintenance work and independently maintains its open-work-order population.

A work order may appear in either or both systems. Differences may indicate synchronization delays, incomplete processing, or other conditions requiring investigation.

The monitor consolidates all unique work orders appearing in at least one daily export.

## 3. Input Files

The application uses two CSV files located in:

`data/daily-exports/`

### External_Open.csv

Required columns, in order:

| Column | Description |
|---|---|
| WorkOrderID | Unique work-order identifier |
| CreatedDate | Original creation date |
| PropertyID | Property identifier |
| RequestType | Maintenance category |
| Priority | Work-order priority |
| DueDate | Target completion date |

### Internal_Open.csv

Required columns, in order:

| Column | Description |
|---|---|
| WorkOrderID | Shared work-order identifier |
| CreatedDate | Original creation date |
| AssignedTo | Assigned technician or coordinator |
| Region | Operational region |
| DueDate | Target completion date |

Both files must use the required column names and ordering.

The workbook expects the repository's existing relative directory structure.

## 4. Reconciliation Rules

WorkOrderID is the unique matching key.

| External | Internal | Classification |
|---|---|---|
| Present | Present | Matched |
| Present | Absent | External Only |
| Absent | Present | Internal Only |
| Absent | Absent | Excluded |

The active backlog is the union of work orders appearing in either source.

A missing record in one system does not automatically establish that the work order has been resolved.

## 5. Aging and Overdue Calculations

The reporting date is selected in `Summary!K2`.

**AgeDays = ReportDate − CreatedDate**, measured in calendar days.

| Age in days | Classification |
|---|---|
| 0–2 | Fresh |
| 3–5 | Developing |
| 6–10 | Aging |
| 11–20 | High Aging |
| 21+ | Critical Aging |

A work order is overdue when:

**DueDate < ReportDate**

Orders due on the reporting date are not yet classified as overdue.

These aging thresholds are fictional business rules and are fixed in the current VBA implementation.

## 6. Input Validation and Exception Handling

Before replacing the workbook's imported source data, the application validates both CSV files.

Implemented validation includes:

- Required file existence
- Required column names and ordering
- Missing WorkOrderIDs
- Duplicate WorkOrderIDs within a source
- Invalid creation dates
- Creation dates later than the reporting date
- Invalid due dates

Validation failures stop the reporting workflow and display an error message.

The application distinguishes between two types of issues:

**Input validation errors:** Prevent the report from proceeding.

**Reconciliation exceptions:** Valid work orders appearing in only one system. These remain in the active backlog and are listed on the Exceptions worksheet for review.

Cross-source field consistency checks and additional empty-file handling remain areas for future validation or enhancement.

## 7. Daily Processing Workflow

1. Place the two required CSV files in `data/daily-exports/`.
2. Open `Meridian_Aging_Monitor.xlsm` in Microsoft Excel.
3. Enter the reporting date in `Summary!K2`.
4. Save the workbook.
5. Select **Run Daily Report**.
6. The workbook creates a pre-refresh backup.
7. Both source files undergo validation.
8. Valid source records are imported.
9. Work orders are reconciled and consolidated.
10. Aging and overdue classifications are calculated.
11. Reconciliation exceptions are generated.
12. The Summary dashboard and chart are refreshed.
13. Review the results and save the completed workbook.

The reporting workflow displays a completion message with processing time.

## 8. Report Outputs

### Summary

Displays:

- Active backlog
- Matched records
- Source discrepancies
- External-only records
- Internal-only records
- Overdue work orders
- Critical aging
- Work orders by aging category
- Aging distribution chart

### Aging_Detail

Contains the consolidated active work-order population, source presence indicators, reconciliation classification, creation date, age, aging category, due date, and overdue status.

### Exceptions

Contains work orders found in only one source, including their classification, dates, aging information, overdue status, and review status.

### External_Data and Internal_Data

Contain the imported source records used for the current report.

## 9. Validation Results

The monitor was tested against synthetic daily snapshots for three consecutive dates.

| Metric | Oct 31 | Nov 1 | Nov 2 |
|---|---:|---:|---:|
| Active backlog | 470 | 479 | 475 |
| Matched records | 441 | 450 | 444 |
| Source discrepancies | 29 | 29 | 31 |

The November 2 results were independently checked using Python.

| Metric | Verified count |
|---|---:|
| Fresh | 93 |
| Developing | 85 |
| Aging | 86 |
| High Aging | 103 |
| Critical Aging | 108 |
| Overdue | 199 |

All six independently checked aging and overdue calculations matched the Excel results.

The November 2 Excel refresh completed in **8.02 seconds** on Hopper.

Additional negative tests confirmed that the application rejects malformed headers, duplicate identifiers, invalid creation dates, and blank identifiers.

## 10. Backup and Recovery

Before each report refresh, the workbook creates:

`excel/Meridian_PreRefresh_Backup.xlsm`

The backup contains a copy of the workbook's state immediately before processing.

A recovery test confirmed that the backup could be opened and that the previous reporting dashboard remained readable.

**Important limitations:**

- The backup is overwritten on each report run.
- Recovery is manual; the application does not automatically roll back a failed refresh.
- The backup captures the workbook's current state, including any reporting-date changes made before refresh.
- The operator should save the workbook after a successful report.
- The backup file is excluded from Git version control.

To recover, close the working workbook, preserve the backup by copying it to a separate filename, inspect that copy, and restore it only after confirming it contains the required information.

## 11. Data Protection and Known Limitations

All data is synthetic. No confidential employer information, proprietary source code, or production records are used.

Current limitations include:

- Fixed CSV schemas and relative folder structure
- Fixed aging thresholds
- Manual initiation of the reporting workflow
- Manual backup recovery
- No automatic report history or scheduled execution
- Cross-source field conflicts are not yet independently validated
- Empty-file handling requires additional testing

The current release is a local Excel/VBA reporting solution, not a hosted or multi-user application.

## 12. Completion Criteria and Future Development

The v1.0 release candidate satisfies the principal functional requirements for daily reconciliation, consolidated aging, overdue monitoring, exception reporting, and dashboard generation.

Final release preparation includes documentation review, repository verification, and packaging.

Future enhancements may include configurable thresholds, additional data-quality checks, scheduled execution, historical reporting, and integration with other Operations Automation modules.

The broader Project 003 remains in development.