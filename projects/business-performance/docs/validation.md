
# Northstar Business Performance Analytics
## Data and Report Validation — v1.0

**Project:** 002 — Northstar Business Performance Analytics
**Dataset:** Synthetic retail and technology services operations
**Reporting period:** January 1, 2025–December 31, 2026
**Status:** Core validation completed; release review pending

## 1. Validation Approach

Northstar uses three complementary validation methods:

1. Python-generated data integrity and business-rule checks.
2. Independent PostgreSQL aggregation and reconciliation queries.
3. Power BI measure comparisons, slicer tests, and visual interaction testing.

Validation is based on selected reporting periods, dimensions, and documented business rules. It does not constitute an exhaustive audit of every possible filter combination.

## 2. Dataset Integrity

The analytical warehouse contains seven dimension tables and six fact tables.

| Area | Verified result |
|---|---:|
| Dimension records | 8,926 |
| Fact records | 98,071 |
| Total records | 106,997 |
| Reporting periods | 24 months |
| Business locations | 3 |
| Retail products | 120 |
| Completed service jobs | 8,944 |

The generated datasets passed implemented checks for primary-key uniqueness, foreign-key integrity, required fields, financial consistency, labor allocation, and inventory movement.

PostgreSQL loading was validated against the original CSV record counts.

## 3. Financial Reconciliation

All amounts represent the complete 2025–2026 reporting period unless otherwise stated.

| Measure | Validated amount |
|---|---:|
| Retail net revenue | $18,872,278.94 |
| Retail cost of goods sold | $15,180,838.79 |
| Retail gross profit | $3,691,440.15 |
| Completed service revenue | $1,004,778.85 |
| Service parts cost | $100,673.95 |
| Allocated direct service labor | $509,155.15 |
| Service gross profit | $394,949.75 |
| Consolidated revenue | $19,877,057.79 |
| Consolidated gross profit | $4,086,389.90 |
| Non-direct labor | $2,364,547.00 |
| Non-payroll operating expenses | $1,005,670.94 |
| Estimated operating result | $716,171.96 |

The estimated operating result subtracts non-direct labor and non-payroll operating expenses from consolidated gross profit.

Direct service labor is already reflected in service gross profit and is not subtracted a second time.

## 4. Payroll and Workforce Reconciliation

| Measure | Validated result |
|---|---:|
| Fully loaded labor | $2,873,702.15 |
| Direct service labor | $509,155.15 |
| Non-direct labor | $2,364,547.00 |
| Payroll reconciliation difference | $0.00 |
| Billable labor hours | 13,289.68 |
| Technician available hours | 32,288.00 |
| Technician utilization | 41.16% |

Technician utilization was independently evaluated using billable hours divided by available hours for employees classified as service technicians or senior service technicians.

Location-level utilization results:

| Location | Utilization |
|---|---:|
| Northstar East | 46.18% |
| Northstar Central | 37.82% |
| Northstar West | 35.93% |

The monthly utilization calculation was also tested against PostgreSQL results covering all 24 reporting periods.

## 5. Service Operations

The dataset contains 8,944 completed service jobs.

Job-level labor allocation supports service-category profitability calculations.

Category-level validation confirmed that allocated labor follows the corresponding completed service jobs rather than repeating company-wide direct labor costs across every service category.

A filtered test for Northstar East in 2025 produced:

| Measure | Result |
|---|---:|
| Completed service jobs | 2,001 |
| Completed service revenue | $222,357.30 |
| Service parts cost | $21,401.88 |
| Allocated labor | $111,103.36 |
| Service gross profit | $89,852.06 |
| Service gross margin | 40.41% |

These figures matched the independent PostgreSQL reconciliation for the same filter context.

## 6. Operating Expenses

Non-payroll operating expenses total $1,005,670.94 across 537 records.

The nine expense categories were independently aggregated in PostgreSQL. Monthly expenses were also reviewed for all 24 reporting periods.

Location reconciliation:

| Location | Operating expenses |
|---|---:|
| Northstar Central | $406,472.97 |
| Northstar West | $317,791.17 |
| Northstar East | $281,406.80 |
| **Total** | **$1,005,670.94** |

## 7. Inventory Snapshot Validation

Inventory is recorded as 24 month-end snapshots across 120 products and three locations.

Inventory balances are point-in-time measures and must not be summed across multiple snapshot dates.

### December 2025 Closing Inventory

| Measure | Validated result |
|---|---:|
| Inventory value | $2,017,323.98 |
| Units on hand | 14,533 |
| Units reserved | 293 |
| Units available | 14,240 |

The December 2025 inventory value was also reconciled by all four product categories.

### December 2026 Closing Inventory

| Measure | Validated result |
|---|---:|
| Inventory value | $2,004,290.88 |
| Units on hand | 14,549 |
| Units reserved | 274 |
| Units available | 14,275 |

December 2026 inventory values and quantities were independently reconciled by all three business locations.

### Reorder and Aging Indicators

The December 2026 snapshot contains 360 product-location positions.

- Positions below reorder point: 0.
- Positions exactly at reorder point: 1.
- Positions with 90 or more days since last sale: 0.
- Maximum recorded days since last sale: 29.
- Average recorded days since last sale: 2.94.

These results reflect the synthetic inventory-generation rules. They should not be interpreted as evidence of real-world inventory optimization.

## 8. Power BI Functional Validation

The six business-facing pages were reviewed:

- Executive Overview
- Retail Sales Performance
- Service Operations
- Labor & Workforce
- Operating Expenses
- Inventory Performance

Year and Location slicers were tested individually and synchronized across the business-facing pages.

Selected chart interactions and filtered KPI results were reviewed for consistency.

Inventory measures return the latest available month-end snapshot for the selected reporting period, while financial and labor measures generally aggregate activity across that period.

## 9. Known Limitations

- All records represent a fictional company and synthetic operations.
- The inventory simulation uses immediate replenishment when required, limiting observable shortages.
- The recorded days-since-last-sale distribution does not produce positions aged 30 or more days at the December 2026 snapshot.
- Scheduled hours and available productive hours are equivalent in the current synthetic labor model.
- Technician utilization should not be interpreted as overall employee productivity.
- Service reporting focuses on completed-job profitability; additional job-status analysis remains outside v1.0.
- Validation covers documented checks and selected filter contexts, not every possible reporting scenario.
- The solution is a portfolio demonstration, not a production accounting or inventory system.

## 10. Validation Conclusion

Northstar's core financial, workforce, expense, and inventory measures have been reconciled against the analytical warehouse for the documented reporting contexts.

The six Power BI business pages have also passed the documented functional and presentation reviews.

No material discrepancies remain identified within the tested scope. Additional tests may be added in future releases.
