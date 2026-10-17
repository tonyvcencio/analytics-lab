-- Project 002 — Northstar Business Performance Analytics
-- Initial fact-table import

\set ON_ERROR_STOP on

BEGIN;

-- Retail transactions
\copy analytics."FactSales" FROM '/home/tony/analytics/northstar/data/FactSales.csv' WITH (FORMAT csv, HEADER true, NULL '')

-- Service operations
\copy analytics."FactServiceJobs" FROM '/home/tony/analytics/northstar/data/FactServiceJobs.csv' WITH (FORMAT csv, HEADER true, NULL '')

-- Employee labor and payroll
\copy analytics."FactLabor" FROM '/home/tony/analytics/northstar/data/FactLabor.csv' WITH (FORMAT csv, HEADER true, NULL '')

-- Job-level labor allocations
\copy analytics."FactJobLaborAllocation" FROM '/home/tony/analytics/northstar/data/FactJobLaborAllocation.csv' WITH (FORMAT csv, HEADER true, NULL '')

-- Operating expenses
\copy analytics."FactExpenses" FROM '/home/tony/analytics/northstar/data/FactExpenses.csv' WITH (FORMAT csv, HEADER true, NULL '')

-- Monthly inventory snapshots
\copy analytics."FactInventorySnapshot" FROM '/home/tony/analytics/northstar/data/FactInventorySnapshot.csv' WITH (FORMAT csv, HEADER true, NULL '')

COMMIT;
