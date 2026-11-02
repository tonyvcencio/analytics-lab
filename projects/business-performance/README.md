# Project 002 — Northstar Business Performance Analytics

**Analytics Lab Portfolio Project**

A synthetic business intelligence project designed to evaluate the financial and operational performance of a fictional retail and technology services company.

**Data Generation: Complete**
**Database Integration: Deployed and Validated**
**Power BI Development: Complete — Six Dashboards**
**Project Status: v1.0 Complete**

## 1. Project Overview

Northstar Home & Tech operates three locations offering retail products and technical services.

Its retail business includes computers, accessories, networking equipment, and smart-home products. Its services include repairs, installations, troubleshooting, technical support, and device setup.

This project develops an integrated analytical dataset to investigate profitability, operational efficiency, inventory management, and opportunities for business improvement.

All company data is synthetic.

### Explore the Project

**Live Portfolio Case Study**

[Explore Northstar Business Performance Analytics](https://tonyvcencio.github.io/analytics-lab/northstar/)

View the completed business case study, including key findings,
management recommendations, and screenshots of all six Power BI
dashboards.

- [Executive Overview Dashboard](outputs/screenshots/executive_overview.png)
- [Retail Sales Performance](outputs/screenshots/retail_sales.png)
- [Service Operations](outputs/screenshots/service_operations.png)
- [Labor & Workforce](outputs/screenshots/labor_workforce.png)
- [Operating Expenses](outputs/screenshots/operating_expenses.png)
- [Inventory Performance](outputs/screenshots/inventory_performance.png)

### Supporting Documentation

- [Data Dictionary](docs/data_dictionary.md)
- [Database Infrastructure](docs/database_infrastructure.md)
- [Data and Report Validation](docs/validation.md)
- [Business Case Study](docs/business_case_study.md)

The dashboards use a fully synthetic dataset representing a fictional retail and technology services business. Screenshots illustrate the completed Power BI report; they are not an interactive web deployment.

## 2. Business Objectives

The analytical solution is designed to answer questions such as:

- Which locations, products, and services generate the highest profits?
- How do revenue and operating expenses change over time?
- How efficiently are service technicians utilized?
- How do direct and non-direct labor costs affect profitability?
- Which products require inventory replenishment?
- How much working capital is tied up in inventory?
- Where can Northstar improve operating efficiency?

## 3. Technology Stack

| Technology | Purpose | Status |
|---|---|---|
| Python | Synthetic data generation and validation | Implemented |
| pandas | Data transformation and aggregation | Implemented |
| NumPy | Synthetic data simulation | Implemented |
| Git and GitHub | Version control and documentation | Implemented |
| PostgreSQL | Relational analytical database | Implemented |
| Power BI | Interactive financial and operational reporting | Implemented |
| DAX | Financial, workforce, service, and inventory measures | Implemented and Validated |

See [Database Infrastructure](docs/database_infrastructure.md)
for PostgreSQL deployment, data loading, validation, and security details.


### Development Environment

**Carroll — Data Engineering**

Mac M4 Pro workstation used for Python-based synthetic data generation, validation, and analytical development.

**Ichabod — Database Infrastructure**

Ubuntu Server hosting PostgreSQL and the Northstar analytical warehouse.

**Hopper — Business Intelligence**

Windows workstation used for Power BI Desktop, DAX development, report validation, and dashboard presentation.

The `analytics-lab` repository is maintained across the development environments using Git and GitHub.


## 4. Dataset Overview

The dataset covers January 1, 2025, through December 31, 2026.

### Dimension Tables

| Table | Records | Purpose |
|---|---:|---|
| DimDate | 744 | Reporting calendar |
| DimLocation | 3 | Business locations |
| DimCustomer | 8,000 | Synthetic customers |
| DimProduct | 120 | Retail product catalog |
| DimService | 20 | Technical service catalog |
| DimEmployee | 30 | Employee information |
| DimExpenseCategory | 9 | Operating expense classifications |

### Fact Tables

| Table | Records | Columns | Purpose |
|---|---:|---:|---|
| FactSales | 59,060 | 14 | Retail sales and returns |
| FactServiceJobs | 10,366 | 17 | Service requests and revenue |
| FactLabor | 10,524 | 18 | Employee work hours and payroll |
| FactJobLaborAllocation | 8,944 | 7 | Job-level direct labor allocation |
| FactExpenses | 537 | 10 | Non-payroll operating expenses |
| FactInventorySnapshot | 8,640 | 12 | Monthly inventory positions |
| **Total fact records** | **98,071** | | |

The dataset contains seven dimension tables and six fact tables.

See [Data Dictionary](docs/data_dictionary.md) for detailed field definitions.

## 5. Analytical Design

Northstar uses a dimensional analytical structure.

Fact tables describe business activities and financial measures, while dimension tables provide the descriptive attributes used for filtering and reporting.

Key analytical relationships include:

- Sales to products, customers, dates, and locations.
- Service jobs to services, customers, technicians, dates, and locations.
- Labor records to employees, dates, and locations.
- Job labor allocations to completed service jobs and labor records.
- Operating expenses to dates, locations, and expense categories.
- Inventory snapshots to dates, locations, and products.

`FactJobLaborAllocation` connects completed service jobs to the labor records responsible for their fulfillment.

Labor costs are recorded in `FactLabor`; job-level allocations provide analytical detail without creating additional payroll expense.


### Power BI Semantic Model

The Power BI semantic model uses all 13 analytical tables from the Northstar PostgreSQL warehouse.

The model supports six interactive business dashboards covering financial performance, retail sales, service operations, labor, operating expenses, and inventory management.

Key implementation details include:

- Dimension-to-fact relationships supporting Year, Location, Product, Service, and other reporting dimensions.
- Synchronized Year and Location slicers across all six business-facing report pages.
- DAX measures for retail revenue, cost of goods sold, gross profit, and gross margin.
- Completed-service revenue, parts costs, and directly allocated service labor.
- Consolidated profitability measures that avoid double-counting direct service labor.
- Fully loaded payroll, non-direct labor, labor hours, and technician utilization.
- Non-payroll operating expenses, total operating costs, and estimated operating results.
- Snapshot-aware inventory measures that report the latest available month-end position within the selected reporting period.

#### Service Labor Allocation

Direct service labor originates in `FactLabor`, while `FactJobLaborAllocation` provides job-level allocation details.

Service-category profitability uses DAX filter propagation through matching service job keys to associate allocated labor with completed service jobs and their categories.

This prevents company-wide direct labor costs from being incorrectly repeated across individual service categories.

#### Inventory Snapshot Methodology

`FactInventorySnapshot` contains monthly inventory balances for each product-location combination.

Inventory valuation and quantity measures use the latest available snapshot within the selected reporting period rather than summing inventory balances across historical months.

With all reporting years selected, the measures return the December 2026 closing inventory position.

Selecting 2025 returns the December 2025 closing position instead.

#### Model Validation

The analytical model has undergone independent PostgreSQL reconciliation and Power BI filter testing.

Validated areas include retail and service financial results, payroll allocation, operating expenses, inventory balances, location-level reporting, and synchronized slicer behavior.

Detailed reconciliation evidence is available in the
[Data and Report Validation](docs/validation.md) documentation.

## 6. Data Generation

Synthetic records are generated using Python.

The generation process incorporates business rules and relationships intended to create internally consistent operational data.

### Retail Sales

The dataset contains:

- 59,060 sales and return records.
- 37,728 unique transactions.
- 56,332 sale lines.
- 2,728 return lines.

Returns use negative quantities and financial values.

Net retail revenue across the reporting period is $18,872,278.94.

### Service Operations

The dataset contains:

- 10,366 service requests.
- 8,944 completed jobs.
- 807 cancelled jobs.
- 541 no-shows.
- 74 scheduled jobs.

Technician assignments respect staggered five-day work schedules and daily service capacity.

Completed service hours total 13,289.68.

Net completed service revenue totals $1,004,778.85.

### Labor and Payroll

The labor model includes employee work calendars, paid hours, billable hours, payroll costs, and direct service labor allocations.

| Measure | Validated result |
|---|---:|
| Paid labor hours | 80,292.00 |
| Billable service hours | 13,289.68 |
| Technician utilization | 41.2% |
| Fully loaded payroll | $2,873,702.15 |
| Direct service labor | $509,155.15 |
| Non-direct labor | $2,364,547.00 |

Direct service labor costs reconcile to job-level labor allocations.

### Operating Expenses

`FactExpenses` includes nine operating expense categories.

The expense model generates:

- Location-specific recurring expenses.
- Shared expenses allocated across locations.
- Variable and periodic operating costs.
- Merchant processing fees based on retail and service revenue.

Total generated non-payroll operating expenses are $1,005,670.94.

Payroll, retail cost of goods sold, and service parts costs are excluded to avoid duplication.

### Inventory

Inventory is modeled across:

- 120 products.
- 3 locations.
- 24 monthly reporting periods.
- 8,640 month-end snapshots.

Inventory movements incorporate signed retail sales and returns, opening stock, and simulated replenishments.

| Measure | Validated result |
|---|---:|
| Opening inventory | 17,342 units |
| Replenishments | 58,386 units |
| Net units sold | 61,179 units |
| Closing inventory | 14,549 units |
| Closing inventory value | $2,004,290.88 |

Opening balances are maintained internally rather than exported as December 2024 snapshots.

## 7. Data Validation

The generation process includes checks for:

- Primary-key uniqueness.
- Foreign-key integrity.
- Required fields.
- Transaction and status consistency.
- Technician scheduling capacity.
- Labor-hour reconciliation.
- Payroll and direct labor allocation.
- Operating expense classifications.
- Shared expense allocation completeness.
- Inventory movement reconciliation.
- Inventory valuation.
- Monthly snapshot completeness.

All six fact tables have passed their implemented validations.

Independent audits of the exported labor, expense, and inventory CSV files have also passed.

### Financial Reconciliation

Fully loaded payroll:

$2,873,702.15

Direct service labor:

$509,155.15

Non-direct labor:

$2,364,547.00

**Payroll reconciliation difference: $0.00**

### Inventory Reconciliation

Opening inventory + replenishments − net units sold = closing inventory

17,342 + 58,386 − 61,179 = 14,549

**Inventory quantity reconciliation difference: 0 units**

### Database and Power BI Validation

All 13 analytical tables were successfully imported into the `northstar_analytics` PostgreSQL database on Ichabod.

Database validation confirmed:

- All 106,997 records were loaded successfully.
- PostgreSQL table counts match the original synthetic CSV datasets.
- Eight financial and operational reconciliation totals match the Python-generated results.
- The `northstar_reader` reporting account successfully retrieves data using read-only permissions.

Power BI validation confirmed:

- All seven dimension tables and six fact tables are incorporated into the analytical model.
- Consolidated revenue of $19,877,057.79 and consolidated gross profit of $4,086,389.90 reconcile to independently verified results.
- The estimated operating result of $716,171.96 reconciles after accounting for non-direct labor and non-payroll expenses.
- Fully loaded labor of $2,873,702.15 reconciles to direct service labor of $509,155.15 plus non-direct labor of $2,364,547.00.
- Completed-service revenue of $1,004,778.85 and service gross profit of $394,949.75 have been validated.
- Operating expenses totaling $1,005,670.94 have been reconciled by category, month, and location.
- December 2026 closing inventory value is $2,004,290.88, representing 14,549 units on hand.
- December 2025 closing inventory value is $2,017,323.98, representing 14,533 units on hand.
- Inventory value by product category and location has been independently reconciled against PostgreSQL for tested reporting periods.
- Year and Location slicers are synchronized across all six business-facing dashboards.
- Report filtering, navigation, and visual interactions have passed functional testing.

Inventory metrics use closing month-end snapshots rather than summing inventory balances across reporting periods.

The completed [Data and Report Validation](docs/validation.md)
document records reconciliation results, testing, and limitations.

## 8. Repository Structure

```text
business-performance/
├── README.md
├── data/
│   ├── DimDate.csv
│   ├── DimLocation.csv
│   ├── DimCustomer.csv
│   ├── DimProduct.csv
│   ├── DimService.csv
│   ├── DimEmployee.csv
│   ├── DimExpenseCategory.csv
│   ├── FactSales.csv
│   ├── FactServiceJobs.csv
│   ├── FactLabor.csv
│   ├── FactJobLaborAllocation.csv
│   ├── FactExpenses.csv
│   └── FactInventorySnapshot.csv
├── docs/
│   ├── business_case_study.md
│   ├── data_dictionary.md
│   ├── database_infrastructure.md
│   └── validation.md
├── outputs/
│   └── screenshots/
│       ├── executive_overview.png
│       ├── retail_sales.png
│       ├── service_operations.png
│       ├── labor_workforce.png
│       ├── operating_expenses.png
│       └── inventory_performance.png
├── powerbi/
│   └── Northstar_Business_Performance.pbix
├── scripts/
│   ├── generate_dimensions.py
│   └── generate_facts.py
└── sql/
    ├── 01_create_tables.sql
    ├── 02_load_dimensions.sql
    └── 03_load_facts.sql
```

## 9. Running the Data Generator

From the `analytics-lab` repository root, activate or use the project's configured Python environment.

The fact-table generator can be executed with:

```bash
.venv/bin/python projects/business-performance/scripts/generate_facts.py
```

The generator reads the existing dimension CSV files and generates the six fact tables.

Python dependencies must be installed in the active environment before execution.

## 10. Modeling Assumptions and Limitations

Northstar is a fictional company. Its transactions, customers, employees, financial results, and inventory are synthetic.

Important modeling assumptions include:

- Technician schedules follow recurring five-day work patterns.
- The current labor model uses scheduled paid hours without overtime.
- Payroll includes a modeled employer burden.
- Technician utilization measures billable service hours relative to paid technician hours.
- Nonbillable hours are not necessarily unproductive hours.
- Merchant processing fees use a simplified 2.5% revenue-based rate.
- Shared operating expenses use predetermined location allocation percentages.
- Inventory replenishment is immediate when required by the simulation.
- Inventory snapshots represent month-end positions rather than every inventory movement.
- Inventory reservations are simulated.
- Inventory valuation uses product acquisition costs.

The immediate-replenishment assumption produces unusually high inventory availability. It should not be interpreted as evidence of real-world supply-chain performance.

These assumptions can be expanded in future versions.

## 11. Project Roadmap

### Phase 1 — Synthetic Dataset

**Complete**

- [x] Generate seven dimension tables and six fact tables.
- [x] Validate referential integrity and business rules.
- [x] Reconcile financial, labor, expense, and inventory calculations.
- [x] Complete independent CSV audits.

### Phase 2 — Database Integration

**Complete for v1.0**

- [x] Deploy and configure PostgreSQL.
- [x] Create and populate the Northstar analytical warehouse.
- [x] Validate all 106,997 loaded records.
- [x] Configure read-only reporting access.
- [x] Execute independent SQL reconciliation queries.

### Phase 3 — Business Intelligence

**Complete for v1.0**

- [x] Connect Power BI Desktop to PostgreSQL.
- [x] Import all 13 analytical tables.
- [x] Configure semantic model relationships.
- [x] Develop financial and operational DAX measures.
- [x] Build all six business-facing dashboards.
- [x] Implement synchronized Year and Location slicers.
- [x] Validate calculations, filtering, and visual interactions.
- [x] Complete dashboard presentation review.

### Phase 4 — Portfolio Release

**Complete — v1.0 Published**

- [x] Complete core warehouse and Power BI development.
- [x] Complete independent financial and inventory QA.
- [x] Finalize the Northstar README.
- [x] Prepare validation documentation.
- [x] Capture six clean dashboard screenshots.
- [x] Complete the business case study.
- [x] Review repository contents for sensitive information.
- [x] Commit and publish the v1.0 deliverables.
- [x] Publish the Northstar portfolio case study website.
- [x] Add Northstar to the LinkedIn Projects section.

**Published Portfolio:**
[Northstar Business Performance Analytics](https://tonyvcencio.github.io/analytics-lab/northstar/)

### Future Enhancements (Outside v1.0)

- Optional additional service-status reporting.
- Expanded inventory turnover and aging analysis.
- Automated reporting refresh workflows.
- Interactive Northstar demonstration on the future Atlas Realm Consulting website.

## 12. Project Purpose

Northstar Business Performance Analytics demonstrates the development of an analytical solution that connects transactional, operational, workforce, and financial information.

The project is intended to showcase practical data engineering, data validation, analytical modeling, SQL, and business intelligence skills.

**Project Status: v1.0 Complete and Published**

Northstar Business Performance Analytics has completed data
engineering, PostgreSQL deployment, Power BI development,
independent validation, technical documentation, and portfolio
publication.

The completed project is publicly accessible through its
dedicated GitHub Pages case study website. Future enhancements
will be managed separately from the completed v1.0 release.
