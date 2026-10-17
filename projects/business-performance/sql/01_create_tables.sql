-- Project 002 — Northstar Business Performance Analytics
-- PostgreSQL 16
-- Schema migration: 01_create_tables.sql

BEGIN;

-- ============================================================
-- DIMENSIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics."DimDate" (
    "DateKey" INTEGER PRIMARY KEY,
    "FullDate" DATE NOT NULL UNIQUE,
    "Year" INTEGER NOT NULL,
    "Quarter" INTEGER NOT NULL,
    "MonthNumber" INTEGER NOT NULL,
    "MonthName" TEXT NOT NULL,
    "YearMonth" TEXT NOT NULL,
    "DayOfWeek" INTEGER NOT NULL,
    "IsWeekend" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics."DimLocation" (
    "LocationKey" INTEGER PRIMARY KEY,
    "LocationName" TEXT NOT NULL,
    "Region" TEXT NOT NULL,
    "OpeningDate" DATE NOT NULL,
    "SquareFootage" INTEGER NOT NULL,
    "LocationType" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics."DimCustomer" (
    "CustomerKey" INTEGER PRIMARY KEY,
    "CustomerType" TEXT NOT NULL,
    "AcquisitionChannel" TEXT NOT NULL,
    "SignupDate" DATE NOT NULL,
    "HomeLocationKey" INTEGER NOT NULL
        REFERENCES analytics."DimLocation"("LocationKey")
);

CREATE TABLE IF NOT EXISTS analytics."DimProduct" (
    "ProductKey" INTEGER PRIMARY KEY,
    "SKU" TEXT NOT NULL UNIQUE,
    "ProductName" TEXT NOT NULL,
    "Category" TEXT NOT NULL,
    "Subcategory" TEXT NOT NULL,
    "Brand" TEXT NOT NULL,
    "StandardRetailPrice" NUMERIC(12,2) NOT NULL,
    "StandardUnitCost" NUMERIC(12,2) NOT NULL,
    "ReorderPoint" INTEGER NOT NULL,
    "IsActive" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics."DimService" (
    "ServiceKey" INTEGER PRIMARY KEY,
    "ServiceCode" TEXT NOT NULL UNIQUE,
    "ServiceName" TEXT NOT NULL,
    "ServiceCategory" TEXT NOT NULL,
    "StandardRate" NUMERIC(12,2) NOT NULL,
    "EstimatedDurationHours" NUMERIC(8,2) NOT NULL,
    "RequiresAppointment" BOOLEAN NOT NULL,
    "IsActive" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics."DimEmployee" (
    "EmployeeKey" INTEGER PRIMARY KEY,
    "EmployeeCode" TEXT NOT NULL UNIQUE,
    "JobRole" TEXT NOT NULL,
    "Department" TEXT NOT NULL,
    "HomeLocationKey" INTEGER NOT NULL
        REFERENCES analytics."DimLocation"("LocationKey"),
    "HireDate" DATE NOT NULL,
    "TerminationDate" DATE,
    "EmploymentType" TEXT NOT NULL,
    "StandardHourlyRate" NUMERIC(12,2) NOT NULL,
    "IsActive" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics."DimExpenseCategory" (
    "ExpenseCategoryKey" INTEGER PRIMARY KEY,
    "ExpenseCategory" TEXT NOT NULL UNIQUE,
    "ExpenseGroup" TEXT NOT NULL,
    "CostBehavior" TEXT NOT NULL,
    "Description" TEXT NOT NULL
);

-- ============================================================
-- FACT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics."FactSales" (
    "SalesLineKey" INTEGER PRIMARY KEY,
    "TransactionID" TEXT NOT NULL,
    "OriginalSalesLineKey" INTEGER,
    "DateKey" INTEGER NOT NULL REFERENCES analytics."DimDate"("DateKey"),
    "LocationKey" INTEGER NOT NULL REFERENCES analytics."DimLocation"("LocationKey"),
    "CustomerKey" INTEGER NOT NULL REFERENCES analytics."DimCustomer"("CustomerKey"),
    "ProductKey" INTEGER NOT NULL REFERENCES analytics."DimProduct"("ProductKey"),
    "TransactionType" TEXT NOT NULL,
    "Quantity" INTEGER NOT NULL,
    "UnitListPrice" NUMERIC(12,2) NOT NULL,
    "DiscountAmount" NUMERIC(12,2) NOT NULL,
    "NetRevenue" NUMERIC(14,2) NOT NULL,
    "UnitCost" NUMERIC(12,2) NOT NULL,
    "TotalCOGS" NUMERIC(14,2) NOT NULL,
    CONSTRAINT fk_original_sales_line
        FOREIGN KEY ("OriginalSalesLineKey")
        REFERENCES analytics."FactSales"("SalesLineKey")
);

CREATE TABLE IF NOT EXISTS analytics."FactServiceJobs" (
    "ServiceJobKey" INTEGER PRIMARY KEY,
    "JobReference" TEXT NOT NULL UNIQUE,
    "CustomerKey" INTEGER NOT NULL REFERENCES analytics."DimCustomer"("CustomerKey"),
    "LocationKey" INTEGER NOT NULL REFERENCES analytics."DimLocation"("LocationKey"),
    "ServiceKey" INTEGER NOT NULL REFERENCES analytics."DimService"("ServiceKey"),
    "EmployeeKey" INTEGER NOT NULL REFERENCES analytics."DimEmployee"("EmployeeKey"),
    "ScheduledDateKey" INTEGER NOT NULL REFERENCES analytics."DimDate"("DateKey"),
    "CompletedDateKey" INTEGER REFERENCES analytics."DimDate"("DateKey"),
    "JobStatus" TEXT NOT NULL,
    "ScheduledHours" NUMERIC(8,2) NOT NULL,
    "ActualServiceHours" NUMERIC(8,2) NOT NULL,
    "StandardServiceFee" NUMERIC(12,2) NOT NULL,
    "DiscountAmount" NUMERIC(12,2) NOT NULL,
    "ServiceRevenue" NUMERIC(14,2) NOT NULL,
    "PartsCost" NUMERIC(12,2) NOT NULL,
    "CancellationReason" TEXT,
    "RelatedTransactionID" TEXT
);

CREATE TABLE IF NOT EXISTS analytics."FactLabor" (
    "LaborKey" INTEGER PRIMARY KEY,
    "DateKey" INTEGER NOT NULL REFERENCES analytics."DimDate"("DateKey"),
    "EmployeeKey" INTEGER NOT NULL REFERENCES analytics."DimEmployee"("EmployeeKey"),
    "LocationKey" INTEGER NOT NULL REFERENCES analytics."DimLocation"("LocationKey"),
    "ScheduledHours" NUMERIC(8,2) NOT NULL,
    "RegularHours" NUMERIC(8,2) NOT NULL,
    "OvertimeHours" NUMERIC(8,2) NOT NULL,
    "AvailableProductiveHours" NUMERIC(8,2) NOT NULL,
    "BillableHours" NUMERIC(8,2) NOT NULL,
    "NonBillableHours" NUMERIC(8,2) NOT NULL,
    "BaseHourlyRate" NUMERIC(12,2) NOT NULL,
    "OvertimeMultiplier" NUMERIC(5,2) NOT NULL,
    "EmployerBurdenRate" NUMERIC(5,2) NOT NULL,
    "GrossWages" NUMERIC(14,2) NOT NULL,
    "EmployerBurdenCost" NUMERIC(14,2) NOT NULL,
    "FullyLoadedLaborCost" NUMERIC(14,2) NOT NULL,
    "DirectServiceLaborCost" NUMERIC(14,2) NOT NULL,
    "NonDirectLaborCost" NUMERIC(14,2) NOT NULL,
    CONSTRAINT uq_labor_employee_date_location
        UNIQUE ("EmployeeKey", "DateKey", "LocationKey")
);

CREATE TABLE IF NOT EXISTS analytics."FactJobLaborAllocation" (
    "JobLaborAllocationKey" INTEGER PRIMARY KEY,
    "LaborKey" INTEGER NOT NULL REFERENCES analytics."FactLabor"("LaborKey"),
    "ServiceJobKey" INTEGER NOT NULL REFERENCES analytics."FactServiceJobs"("ServiceJobKey"),
    "AllocatedRegularHours" NUMERIC(8,2) NOT NULL,
    "AllocatedOvertimeHours" NUMERIC(8,2) NOT NULL,
    "AllocatedHours" NUMERIC(8,2) NOT NULL,
    "AllocatedDirectLaborCost" NUMERIC(14,2) NOT NULL,
    CONSTRAINT uq_job_labor_allocation
        UNIQUE ("LaborKey", "ServiceJobKey")
);

CREATE TABLE IF NOT EXISTS analytics."FactExpenses" (
    "ExpenseKey" INTEGER PRIMARY KEY,
    "ExpenseReference" TEXT NOT NULL,
    "DateKey" INTEGER NOT NULL REFERENCES analytics."DimDate"("DateKey"),
    "LocationKey" INTEGER NOT NULL REFERENCES analytics."DimLocation"("LocationKey"),
    "ExpenseCategoryKey" INTEGER NOT NULL
        REFERENCES analytics."DimExpenseCategory"("ExpenseCategoryKey"),
    "VendorCode" TEXT NOT NULL,
    "ExpenseDescription" TEXT NOT NULL,
    "ExpenseAmount" NUMERIC(14,2) NOT NULL,
    "IsRecurring" BOOLEAN NOT NULL,
    "AllocationMethod" TEXT NOT NULL,
    CONSTRAINT uq_expense_reference_location
        UNIQUE ("ExpenseReference", "LocationKey")
);

CREATE TABLE IF NOT EXISTS analytics."FactInventorySnapshot" (
    "InventorySnapshotKey" INTEGER PRIMARY KEY,
    "DateKey" INTEGER NOT NULL REFERENCES analytics."DimDate"("DateKey"),
    "LocationKey" INTEGER NOT NULL REFERENCES analytics."DimLocation"("LocationKey"),
    "ProductKey" INTEGER NOT NULL REFERENCES analytics."DimProduct"("ProductKey"),
    "UnitsOnHand" INTEGER NOT NULL,
    "UnitsReserved" INTEGER NOT NULL,
    "UnitsAvailable" INTEGER NOT NULL,
    "UnitInventoryCost" NUMERIC(12,2) NOT NULL,
    "InventoryValue" NUMERIC(14,2) NOT NULL,
    "ReorderPoint" INTEGER NOT NULL,
    "DaysSinceLastSale" INTEGER NOT NULL,
    "StockStatus" TEXT NOT NULL,
    CONSTRAINT uq_inventory_snapshot
        UNIQUE ("DateKey", "LocationKey", "ProductKey"),
    CONSTRAINT chk_inventory_quantities
        CHECK (
            "UnitsOnHand" >= 0
            AND "UnitsReserved" >= 0
            AND "UnitsAvailable" >= 0
            AND "UnitsOnHand" = "UnitsReserved" + "UnitsAvailable"
        )
);

COMMIT;