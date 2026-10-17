\set ON_ERROR_STOP on

BEGIN;

\copy analytics."DimDate" FROM '/home/tony/analytics/northstar/data/DimDate.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimLocation" FROM '/home/tony/analytics/northstar/data/DimLocation.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimCustomer" FROM '/home/tony/analytics/northstar/data/DimCustomer.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimProduct" FROM '/home/tony/analytics/northstar/data/DimProduct.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimService" FROM '/home/tony/analytics/northstar/data/DimService.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimEmployee" FROM '/home/tony/analytics/northstar/data/DimEmployee.csv' WITH (FORMAT csv, HEADER true, NULL '')
\copy analytics."DimExpenseCategory" FROM '/home/tony/analytics/northstar/data/DimExpenseCategory.csv' WITH (FORMAT csv, HEADER true, NULL '')

COMMIT;
