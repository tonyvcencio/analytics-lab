# Module 001 — Daily Aging & Reconciliation Monitor

**Project:** 003 — Operations Automation  
**Company:** Meridian Property Services (fictional)  
**Primary Platform:** Microsoft Excel / VBA  
**Development Workstation:** Hopper  
**Status:** Specification — v0.1  
**Target:** November 2026

## 1. Purpose

Automate the daily reconciliation of outstanding maintenance work orders across two operational systems and generate a unified aging report.

The report must include every unique work order appearing in either system's daily open-work-order export.

## 2. Business Environment

Meridian Property Services uses two systems:

- **Property Management System (External):** Originates maintenance requests and supplies records to the internal maintenance system.
- **Maintenance Operations System (Internal):** Receives work orders from the external system and manages their operational processing.

Each system independently maintains its open-work-order population.

Resolved work orders disappear from the following day's open-work-order export.

Differences between the two exports may indicate synchronization delays, unresolved work, or operational discrepancies requiring investigation.

## 3. Input Files

The module processes two daily Excel exports.

### Source A — External_Open_WorkOrders.xlsx

Required fields:

| Column | Description |
|---|---|
| WorkOrderID | Unique work order identifier |
| CreatedDate | Original request creation date |
| PropertyID | Property identifier |
| RequestType | Maintenance category |
| Priority | Work order priority |
| DueDate | Target completion date |

### Source B — Internal_Open_WorkOrders.xlsx

Required fields:

| Column | Description |
|---|---|
| WorkOrderID | Shared work order identifier |
| CreatedDate | Original creation date inherited from Source A |
| AssignedTo | Responsible technician or coordinator |
| Region | Operational region |
| DueDate | Target completion date |

The MVP assumes that both sources use the same WorkOrderID and inherit the same original creation date.

## 4. Reconciliation Rules

All comparisons use WorkOrderID as the unique matching key.

| External | Internal | Result |
|---|---|---|
| Present | Present | Matched |
| Present | Absent | External Only |
| Absent | Present | Internal Only |
| Absent | Absent | Excluded |

The consolidated active backlog is the union of unique WorkOrderIDs across both exports.

A work order must not be excluded simply because it is missing from one source.

A missing record does not independently establish that the work order was resolved.

## 5. Aging Calculation

Aging is measured in calendar days:

**AgeDays = MAX(0, ReportDate - CreatedDate)**

The report date must be explicitly defined for each run.

For testing, use a fixed report date. Production runs will use the selected reporting date.

### Aging Buckets

| Days | Category |
|---|---|
| 0–2 | Fresh |
| 3–5 | Developing |
| 6–10 | Aging |
| 11–20 | High Aging |
| 21+ | Critical Aging |

These are fictional business thresholds and will eventually be configurable.

## 6. Exception Handling

The tool must identify:

- Work orders present in only one source.
- Duplicate WorkOrderIDs within a source.
- Missing or invalid creation dates.
- Creation dates later than the report date.
- Conflicting creation dates between sources.
- Missing required columns.
- Empty or unreadable source files.

Invalid records must be reported rather than silently discarded.

If a valid creation date cannot be established, the work order remains in the reconciliation output with an aging calculation exception.

## 7. Processing Workflow

1. Select the reporting date.
2. Import the external open-work-order export.
3. Import the internal open-work-order export.
4. Validate file structure and required fields.
5. Match WorkOrderIDs bidirectionally.
6. Consolidate unique open work orders.
7. Classify records as Matched, External Only, or Internal Only.
8. Calculate aging where valid dates are available.
9. Identify reconciliation and data-quality exceptions.
10. Generate the daily report.

## 8. Report Outputs

The Excel report will contain:

### Summary

- Total unique open work orders
- Matched work orders
- External-only work orders
- Internal-only work orders
- Work orders by aging bucket
- Total data-quality exceptions

### Aging Detail

One row per unique WorkOrderID, including source presence, reconciliation classification, creation date, age, and aging category.

### Exceptions

Records requiring review, including unmatched IDs, duplicates, missing dates, and invalid source data.

## 9. Validation Requirements

The MVP must pass tests confirming:

- Records appearing in both exports are counted once.
- Records appearing in only one export are included.
- Records absent from both exports are excluded.
- Duplicate IDs do not inflate the consolidated backlog.
- Aging calculations match independently verified expected results.
- Missing dates do not cause records to disappear.
- Empty exports are handled correctly.
- Repeated processing of identical inputs produces identical results.

## 10. Initial Implementation

The first implementation will use Microsoft Excel and VBA on Hopper.

COUNTIF-based presence checks will serve as the conceptual starting point, with VBA handling bidirectional reconciliation, deduplication, validation, and report generation.

Power Query and Python implementations may be developed later for comparison and additional functionality.

## 11. Data Protection

All records, work-order identifiers, dates, and business scenarios will be synthetic.

No employer-owned data, code, proprietary procedures, or internal reporting files will be incorporated.

## 12. MVP Completion Criteria

The module is complete when two synthetic daily exports can be processed into one accurate, reproducible aging report with validated reconciliation results and documented exceptions.