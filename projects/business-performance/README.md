# Project 002 — Northstar Business Performance Analytics

**Analytics Lab Portfolio Project**

A synthetic business intelligence project designed to evaluate the financial and operational performance of a fictional retail and technology services company.

**Data-generation phase: Complete**  
**Database integration: Planned**  
**Power BI development: Planned**

## 1. Project Overview

Northstar Home & Tech operates three locations offering retail products and technical services.

Its retail business includes computers, accessories, networking equipment, and smart-home products. Its services include repairs, installations, troubleshooting, technical support, and device setup.

This project develops an integrated analytical dataset to investigate profitability, operational efficiency, inventory management, and opportunities for business improvement.

All company data is synthetic.

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
| Power BI | Business intelligence dashboards | Planned |
| DAX | Analytical measures and KPIs | Planned |

See [Database Infrastructure](docs/database_infrastructure.md)
for PostgreSQL deployment, data loading, validation, and security details.

### Development Environment

**Mac — Data Engineering**

Python-based data generation, validation, and analytical development.

**Ichabod — Database Infrastructure**

Ubuntu server designated for PostgreSQL and future data pipelines.

**Nomad — Business Intelligence**

Windows workstation designated for Power BI Desktop, data modeling, and dashboard development.

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
│   └── data_dictionary.md
├── powerbi/
└── scripts/
    └── generate_facts.py
```

Additional supporting scripts and project files may exist within these directories.

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

- Dimension generation.
- Fact-table generation.
- Referential integrity validation.
- Financial reconciliation.
- Inventory simulation.
- Independent CSV audits.

### Phase 2 — Database Integration

**Planned**

- Deploy PostgreSQL on Ichabod.
- Design relational database schemas.
- Load and validate Northstar datasets.
- Develop SQL analytical queries.
- Establish repeatable data-loading workflows.

### Phase 3 — Business Intelligence

**Planned**

- Build the Power BI semantic model on Nomad.
- Define DAX measures.
- Create revenue and profitability dashboards.
- Analyze service productivity.
- Develop operating expense visualizations.
- Create inventory performance dashboards.

### Phase 4 — Portfolio Presentation

**Planned**

- Document business findings.
- Publish dashboard screenshots.
- Explain analytical methodology.
- Identify operational improvement opportunities.
- Prepare a portfolio case study.

## 12. Project Purpose

Northstar Business Performance Analytics demonstrates the development of an analytical solution that connects transactional, operational, workforce, and financial information.

The project is intended to showcase practical data engineering, data validation, analytical modeling, SQL, and business intelligence skills.

**Project status: Synthetic data generation complete; database and dashboard development pending.**