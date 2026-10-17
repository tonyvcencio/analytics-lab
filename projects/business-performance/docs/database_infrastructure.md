# Project 002 — Northstar Database Infrastructure

## Overview

Northstar Business Performance Analytics uses PostgreSQL 16
hosted on Ichabod, an Ubuntu Server 24.04 LTS machine.

The database stores the synthetic analytical datasets generated
during Project 002's data-engineering phase.

## Infrastructure

| Component | Configuration |
|---|---|
| Database server | Ichabod |
| Operating system | Ubuntu Server 24.04.5 LTS |
| PostgreSQL version | 16.15 |
| PostgreSQL cluster | 16/main |
| Database | northstar_analytics |
| Database port | 5432 |
| Application role | northstar_app |
| Reporting role | northstar_reader |

The database is separate from Project 001's health_metrics database.

## Database Architecture

Two PostgreSQL schemas have been created:

- staging: Reserved for future ETL and staging workflows.
- analytics: Contains validated analytical tables.

### Analytics Tables

Seven dimensions:

- DimDate
- DimLocation
- DimCustomer
- DimProduct
- DimService
- DimEmployee
- DimExpenseCategory

Six facts:

- FactSales
- FactServiceJobs
- FactLabor
- FactJobLaborAllocation
- FactExpenses
- FactInventorySnapshot

**Total: 13 tables and 106,997 records.**

## Data Loading

The initial database load uses PostgreSQL's native CSV import
functionality.

SQL scripts are maintained in:

`projects/business-performance/sql/`

| Script | Purpose |
|---|---|
| 01_create_tables.sql | Create relational tables |
| 02_load_dimensions.sql | Import dimension CSVs |
| 03_load_facts.sql | Import fact CSVs |

Dimension tables are loaded before fact tables to satisfy
foreign-key dependencies.

The initial import loads directly into the analytics schema.
A repeatable staging-to-analytics ETL process is planned.

## Data Validation

PostgreSQL record counts were independently verified against
the original CSV datasets.

All eight financial reconciliation metrics matched the
Python-generated results.

| Metric | Validated total |
|---|---:|
| Retail net revenue | $18,872,278.94 |
| Service net revenue | $1,004,778.85 |
| Fully loaded payroll | $2,873,702.15 |
| Direct service labor | $509,155.15 |
| Non-direct labor | $2,364,547.00 |
| Allocated job labor | $509,155.15 |
| Operating expenses | $1,005,670.94 |
| Closing inventory value | $2,004,290.88 |

Financial reconciliation difference: $0.00.

## Network Architecture

Northstar's development environment uses three machines:

| Machine | Responsibility |
|---|---|
| Mac | Python engineering and data preparation |
| Ichabod | PostgreSQL database hosting |
| Nomad | Power BI Desktop and reporting |

PostgreSQL listens on localhost and Ichabod's designated
private LAN address.

Remote database access is restricted by PostgreSQL
authentication rules.

The Mac uses northstar_app for data engineering.

Nomad uses northstar_reader for reporting.

The reporting role has SELECT permissions on analytical
tables and does not have INSERT, UPDATE, or DELETE permissions.

## Security

- Dedicated database and application roles.
- Dedicated read-only reporting role.
- SCRAM-SHA-256 password authentication.
- Database access restricted to designated LAN clients.
- PostgreSQL is not intentionally exposed to the public internet.
- Database passwords and authentication secrets are excluded
  from source control.
- Ubuntu UFW rules are configured to restrict inbound access.

Firewall activation and remote connectivity require
final verification.

## Next Steps

1. Verify UFW is active and SSH remains accessible.
2. Test PostgreSQL connectivity from the Mac.
3. Test PostgreSQL connectivity from Nomad.
4. Connect Power BI Desktop using northstar_reader.
5. Configure the Power BI semantic model.
6. Develop database validation and analytical SQL queries.
7. Build reproducible staging-to-analytics ETL workflows.

## Project Status

- Synthetic data generation: Complete.
- PostgreSQL database creation: Complete.
- Initial data loading: Complete.
- Financial reconciliation: Complete.
- Local reporting-role authentication: Verified.
- Remote PostgreSQL connectivity: Pending verification.
- Power BI integration: Pending.