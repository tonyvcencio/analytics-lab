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
| Carroll | macOS workstation for Python engineering and data preparation |
| Ichabod | Ubuntu Server hosting PostgreSQL |
| Hopper | Windows workstation for Power BI Desktop, DAX, and reporting |

PostgreSQL is configured for local and authorized private-network connectivity.

Database access is controlled through PostgreSQL authentication and client-access rules.

Carroll uses the `northstar_app` role for authorized data engineering operations.

Hopper uses the `northstar_reader` role for Power BI reporting and database validation.

The reporting role has SELECT permissions on analytical tables and does not have INSERT, UPDATE, or DELETE permissions.

The Power BI report uses an imported analytical model. Previously imported report data can be explored without a live PostgreSQL query connection; refreshing from the original source requires authorized database connectivity and credentials.

The development database is not intended to serve as a publicly accessible reporting endpoint.

## Security

- Dedicated database and application roles.
- Dedicated read-only reporting role.
- SCRAM-SHA-256 password authentication.
- Database access restricted to designated LAN clients.
- PostgreSQL is not intentionally exposed to the public internet.
- Database passwords and authentication secrets are excluded
  from source control.
- Ubuntu UFW rules are configured to restrict inbound access.

The current firewall activation state and complete remote-access rules have not been independently reverified during the v1.0 release review.

## Next Steps

The PostgreSQL warehouse and Power BI integration are complete for Northstar v1.0.

Future infrastructure improvements may include:

1. Implement a repeatable staging-to-analytics ETL workflow.
2. Expand automated database and data-quality testing.
3. Verify and document firewall and access-control settings.
4. Evaluate scheduled report refresh and deployment options.
5. Review database backup and restoration procedures periodically.
6. Evaluate deployment alternatives for public portfolio demonstrations without exposing the development database.

These enhancements are outside the Northstar v1.0 release scope.

## Project Status

| Component | Status |
|---|---|
| Synthetic data generation | Complete |
| PostgreSQL database creation | Complete |
| Initial data loading | Complete |
| Financial reconciliation | Complete |
| Read-only reporting access | Verified |
| Power BI Desktop integration | Complete |
| Analytical model and DAX | Complete for v1.0 |
| Six business dashboards | Complete |
| Report filtering and functional QA | Complete for documented scope |
| Repeatable staging-to-analytics ETL | Future enhancement |
| Public report embedding | Future enhancement |
| Final infrastructure security recheck | Outstanding |

## Project Status

- Synthetic data generation: Complete.
- PostgreSQL database creation: Complete.
- Initial data loading: Complete.
- Financial reconciliation: Complete.
- Local reporting-role authentication: Verified.
- Remote PostgreSQL connectivity: Pending verification.
- Power BI integration: Pending.