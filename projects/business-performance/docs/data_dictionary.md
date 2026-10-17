
# Northstar Home & Tech — Data Dictionary

**Project:** Project 002 — Northstar Business Performance Analytics  
**Organization:** Northstar Home & Tech (fictional)  
**Consultancy:** Atlas Realm Consulting  
**Dataset:** 100% synthetic  
**Version:** 0.1 — Draft

## 1. Data Architecture

Northstar uses a dimensional data model with shared dimensions and multiple fact tables.

The model supports retail sales, technical services, workforce efficiency, inventory management, customer analytics, and financial performance.

### Design Principles

- Use a star-schema-oriented dimensional model.
- Assign integer surrogate keys to dimensions.
- Maintain clearly defined fact table grains.
- Use one-to-many relationships with single-direction filtering in Power BI.
- Preserve historical transaction prices and costs.
- Avoid double-counting revenue, labor, and operating expenses.
- Generate reproducible synthetic data using a fixed random seed.
- Validate primary keys, foreign keys, and financial reconciliation rules.
- Store all monetary values in USD, excluding sales tax.
- Use ISO 8601 dates in source CSV files.
- Use null values for genuinely unknown or inapplicable attributes.

## 2. Dimension Tables

### 2.1 DimDate

**Grain:** One row per calendar date.

**Primary key:** `DateKey`

| Column | Data Type | Description |
|---|---|---|
| DateKey | INTEGER | Date identifier in YYYYMMDD format |
| FullDate | DATE | Actual calendar date |
| Year | INTEGER | Calendar year |
| Quarter | INTEGER | Calendar quarter, 1–4 |
| MonthNumber | INTEGER | Calendar month, 1–12 |
| MonthName | VARCHAR(20) | Full month name |
| YearMonth | VARCHAR(7) | Year and month in YYYY-MM format |
| DayOfWeek | INTEGER | ISO weekday, Monday = 1 |
| IsWeekend | BOOLEAN | True for Saturday or Sunday |

**Business rules:**

- `DateKey` must be unique.
- `FullDate` must be unique.
- The calendar must have no missing dates within its defined range.
- The initial simulation covers January 1, 2025, through December 31, 2026.
- Calendar coverage may extend beyond the simulation period to support future scheduling and analysis.
- DateKey must equal the YYYYMMDD representation of FullDate.

### 2.2 DimLocation

**Grain:** One row per Northstar business location.

**Primary key:** `LocationKey`

| Column | Data Type | Description |
|---|---|---|
| LocationKey | INTEGER | Unique location identifier |
| LocationName | VARCHAR(100) | Business location name |
| Region | VARCHAR(50) | Geographic operating region |
| OpeningDate | DATE | Date location began operations |
| SquareFootage | INTEGER | Approximate retail/service floor area |
| LocationType | VARCHAR(50) | Operational classification |

**Initial locations:**

| LocationKey | LocationName | Region | LocationType |
|---|---|---|---|
| 1 | Northstar Central | Central | Flagship |
| 2 | Northstar West | West | Retail-Focused |
| 3 | Northstar East | East | Service-Focused |

**Business rules:**

- Exactly three operating locations are included initially.
- LocationKey must be unique and non-null.
- All transactions must reference a valid location.
- OpeningDate must precede the location's first transaction.
- Locations may have different sales mixes, operating costs, and staffing patterns.

### 2.3 DimCustomer

**Grain:** One row per unique customer.

**Primary key:** `CustomerKey`

| Column | Data Type | Description |
|---|---|---|
| CustomerKey | INTEGER | Unique customer identifier |
| CustomerType | VARCHAR(30) | Residential or Small Business |
| AcquisitionChannel | VARCHAR(50) | Original customer acquisition source |
| SignupDate | DATE | Date customer first registered |
| HomeLocationKey | INTEGER | Customer's primary business location |

**CustomerType values:**

- Residential
- Small Business

**AcquisitionChannel values:**

- Walk-In
- Online Search
- Referral
- Social Media
- Local Advertising
- Business Partnership

**Business rules:**

- CustomerKey must be unique and non-null.
- HomeLocationKey must reference a valid DimLocation record.
- A customer's home location may differ from the location of a sale or service appointment.
- Customers may have multiple retail transactions and service appointments.
- SignupDate must not be later than the customer's first recorded transaction.
- Customer segmentation must remain consistent across retail and service analysis.
- Synthetic customer records must contain no real personal information.

### 2.4 DimProduct

**Grain:** One row per distinct product SKU.

**Primary key:** `ProductKey`

| Column | Data Type | Description |
|---|---|---|
| ProductKey | INTEGER | Unique product identifier |
| SKU | VARCHAR(30) | Unique stock-keeping unit |
| ProductName | VARCHAR(150) | Product description |
| Category | VARCHAR(50) | Primary product category |
| Subcategory | VARCHAR(50) | Product classification |
| Brand | VARCHAR(50) | Fictional product brand |
| StandardRetailPrice | DECIMAL(12,2) | Reference selling price in USD |
| StandardUnitCost | DECIMAL(12,2) | Reference acquisition cost in USD |
| ReorderPoint | INTEGER | Reference minimum stock threshold |
| IsActive | BOOLEAN | Whether product remains available for sale |

**Initial product categories:**

- Computers
- Accessories
- Networking
- Smart Home

**Business rules:**

- ProductKey and SKU must each be unique.
- StandardRetailPrice and StandardUnitCost must be nonnegative.
- Actual sale prices and costs must be stored in FactSales.
- Product categories and subcategories must be standardized.
- Inactive products must remain available for historical analysis.
- Inventory levels vary by product and location.
- Standard prices and costs are reference values, not historical financial records.

### 2.5 DimService

**Grain:** One row per distinct service offering.

**Primary key:** `ServiceKey`

| Column | Data Type | Description |
|---|---|---|
| ServiceKey | INTEGER | Unique service identifier |
| ServiceCode | VARCHAR(30) | Unique service offering code |
| ServiceName | VARCHAR(100) | Service description |
| ServiceCategory | VARCHAR(50) | Service classification |
| StandardRate | DECIMAL(12,2) | Reference customer charge |
| EstimatedDurationHours | DECIMAL(5,2) | Expected labor duration |
| RequiresAppointment | BOOLEAN | Whether scheduling is required |
| IsActive | BOOLEAN | Whether service is currently offered |

**Initial service categories:**

- Computer Repair
- Network Installation
- Smart Home Installation
- Troubleshooting
- Technical Support
- Device Setup

**Business rules:**

- ServiceKey and ServiceCode must each be unique.
- StandardRate and EstimatedDurationHours must be nonnegative.
- Actual service revenue is determined by completed, billable jobs.
- Cancelled jobs do not generate service revenue unless a valid cancellation fee is recorded.
- Service labor costs must reconcile with employee labor records.
- Services may be associated with earlier retail purchases.
- Actual service duration may differ from the estimated duration.

### 2.6 DimEmployee

**Grain:** One row per employee in the initial model.

**Primary key:** `EmployeeKey`

| Column | Data Type | Description |
|---|---|---|
| EmployeeKey | INTEGER | Unique employee identifier |
| EmployeeCode | VARCHAR(20) | Fictional employee reference |
| JobRole | VARCHAR(50) | Employee's primary role |
| Department | VARCHAR(50) | Retail, Service, or Administration |
| HomeLocationKey | INTEGER | Employee's primary location |
| HireDate | DATE | Employment start date |
| TerminationDate | DATE | Employment end date, if applicable |
| EmploymentType | VARCHAR(30) | Full-Time or Part-Time |
| StandardHourlyRate | DECIMAL(10,2) | Reference hourly wage |
| IsActive | BOOLEAN | Current employment status |

**Initial job roles:**

- Retail Associate
- Senior Retail Associate
- Service Technician
- Senior Service Technician
- Store Manager
- Assistant Manager
- Administrative Support

**Business rules:**

- EmployeeKey and EmployeeCode must each be unique.
- HomeLocationKey must reference DimLocation.
- HireDate must precede or equal the employee's first labor record.
- TerminationDate, when populated, must not precede HireDate.
- Actual historical labor costs must come from FactLabor.
- StandardHourlyRate is a reference value, not an authoritative historical wage.
- Employees may work at locations other than their home location.
- Employee labor records must distinguish billable and nonbillable work.
- Employee records must contain fictional identifiers only.

### 2.7 DimExpenseCategory

**Grain:** One row per distinct operating expense category.

**Primary key:** `ExpenseCategoryKey`

| Column | Data Type | Description |
|---|---|---|
| ExpenseCategoryKey | INTEGER | Unique category identifier |
| ExpenseCategory | VARCHAR(60) | Expense classification |
| ExpenseGroup | VARCHAR(50) | Higher-level financial grouping |
| CostBehavior | VARCHAR(20) | Fixed, Variable, or Mixed |
| Description | VARCHAR(250) | Category definition |

**Initial expense categories:**

- Rent
- Utilities
- Insurance
- Marketing
- Software Subscriptions
- Equipment Maintenance
- Administrative Supplies
- Merchant Processing Fees
- Other Operating Expenses

**Business rules:**

- ExpenseCategoryKey must be unique.
- ExpenseCategory must have a consistent financial definition.
- FactExpenses records operating expenses, not product COGS.
- Direct service labor is accounted for through FactLabor.
- Administrative and other non-direct labor costs are also sourced from FactLabor and included in operating profit.
- Employee labor must not be duplicated in FactExpenses.
- Expense categories must support aggregation by location and period.
- CostBehavior describes expected cost behavior, not an absolute accounting rule.


## 3. Fact Tables

### 3.1 FactSales

**Grain:** One product line within a retail transaction, including separate return lines.

**Primary key:** `SalesLineKey`

| Column | Data Type | Description |
|---|---|---|
| SalesLineKey | BIGINT | Unique sales line identifier |
| TransactionID | VARCHAR(30) | Groups lines belonging to one transaction |
| OriginalSalesLineKey | BIGINT | Original line reference for returns; null for sales |
| DateKey | INTEGER | Transaction date |
| LocationKey | INTEGER | Location processing the transaction |
| CustomerKey | INTEGER | Purchasing or returning customer |
| ProductKey | INTEGER | Product sold or returned |
| TransactionType | VARCHAR(20) | Sale or Return |
| Quantity | INTEGER | Positive for sales, negative for returns |
| UnitListPrice | DECIMAL(12,2) | Unit price before discounts |
| DiscountAmount | DECIMAL(12,2) | Signed total discount adjustment |
| NetRevenue | DECIMAL(12,2) | Signed revenue excluding sales tax |
| UnitCost | DECIMAL(12,2) | Historical acquisition cost per unit |
| TotalCOGS | DECIMAL(12,2) | Signed cost of goods sold |

**Business rules:**

- SalesLineKey must be unique and non-null.
- TransactionID may appear on multiple product lines.
- Sale quantities must be positive.
- Return quantities must be negative.
- Return lines must reference a valid original sales line.
- Returns must not exceed the quantity originally sold, accounting for earlier returns.
- UnitListPrice and UnitCost must be nonnegative.
- DiscountAmount is positive for sales discounts and negative when reversing discounts on returned goods.
- NetRevenue = Quantity × UnitListPrice − DiscountAmount.
- TotalCOGS = Quantity × UnitCost.
- Sales and returns must use the original transaction-time unit cost for consistent cost reversal.
- CustomerKey, ProductKey, LocationKey, and DateKey must reference valid dimension records.
- Revenue and COGS exclude sales tax.
- Net retail gross profit = SUM(NetRevenue) − SUM(TotalCOGS).
- All sales are assumed financially posted; cancelled or abandoned checkout attempts are excluded.
- Returned products are assumed resalable unless a future returns-disposition model identifies otherwise.

### 3.2 FactServiceJobs

**Grain:** One service appointment or job.

**Primary key:** `ServiceJobKey`

| Column | Data Type | Description |
|---|---|---|
| ServiceJobKey | BIGINT | Unique service job identifier |
| JobReference | VARCHAR(30) | Human-readable fictional job identifier |
| CustomerKey | INTEGER | Customer receiving service |
| LocationKey | INTEGER | Location responsible for the job |
| ServiceKey | INTEGER | Service offering |
| EmployeeKey | INTEGER | Primary assigned technician |
| ScheduledDateKey | INTEGER | Original scheduled service date |
| CompletedDateKey | INTEGER | Actual completion date, if applicable |
| JobStatus | VARCHAR(30) | Appointment or job status |
| ScheduledHours | DECIMAL(6,2) | Planned service duration |
| ActualServiceHours | DECIMAL(6,2) | Recorded service effort |
| StandardServiceFee | DECIMAL(12,2) | Reference fee at booking |
| DiscountAmount | DECIMAL(12,2) | Actual discount applied |
| ServiceRevenue | DECIMAL(12,2) | Earned service revenue |
| PartsCost | DECIMAL(12,2) | Actual consumed parts cost |
| CancellationReason | VARCHAR(100) | Reason for cancellation, if applicable |
| RelatedTransactionID | VARCHAR(30) | Optional retail transaction reference |

**JobStatus values:**

- Scheduled
- Completed
- Cancelled
- No-Show

**Business rules:**

- ServiceJobKey and JobReference must each be unique.
- CustomerKey, LocationKey, ServiceKey, and EmployeeKey must reference valid dimension records.
- ScheduledDateKey must be populated.
- CompletedDateKey must be populated only for completed jobs.
- Completed jobs must have a completion date on or after the scheduled date, unless an explicitly documented rescheduling rule applies.
- ScheduledHours and ActualServiceHours must be nonnegative.
- StandardServiceFee and PartsCost must be nonnegative.
- Completed jobs may generate earned service revenue.
- Scheduled, Cancelled, and No-Show jobs generate no service revenue in the initial model.
- DiscountAmount must not exceed the applicable service fee.
- ServiceRevenue for completed jobs equals StandardServiceFee minus DiscountAmount.
- ActualServiceHours is an operational measure; authoritative labor costs come from FactLabor and the future job-labor allocation table.
- PartsCost represents parts consumed for the job and must not also be recorded as retail COGS.
- RelatedTransactionID is optional and may identify a retail purchase associated with a service.
- Job-level gross profit = ServiceRevenue − PartsCost − AllocatedDirectLaborCost.
- Cancelled and no-show appointments remain in the dataset for operational analysis.


### 3.3 FactLabor

**Grain:** One employee, one work date, one worked location.

**Primary key:** `LaborKey`

| Column | Data Type | Description |
|---|---|---|
| LaborKey | BIGINT | Unique daily labor record |
| DateKey | INTEGER | Date work was performed |
| EmployeeKey | INTEGER | Employee performing the work |
| LocationKey | INTEGER | Location where work was performed |
| ScheduledHours | DECIMAL(6,2) | Planned shift hours |
| RegularHours | DECIMAL(6,2) | Regular hours actually worked |
| OvertimeHours | DECIMAL(6,2) | Overtime hours actually worked |
| AvailableProductiveHours | DECIMAL(6,2) | Worked hours available for productive activities |
| BillableHours | DECIMAL(6,2) | Hours attributable to billable service work |
| NonBillableHours | DECIMAL(6,2) | Worked hours not attributable to billable service work |
| BaseHourlyRate | DECIMAL(10,2) | Historical regular hourly wage |
| OvertimeMultiplier | DECIMAL(4,2) | Overtime wage multiplier |
| EmployerBurdenRate | DECIMAL(5,4) | Employer payroll burden percentage as a decimal |
| GrossWages | DECIMAL(12,2) | Regular and overtime wages |
| EmployerBurdenCost | DECIMAL(12,2) | Employer burden on gross wages |
| FullyLoadedLaborCost | DECIMAL(12,2) | Total labor cost |
| DirectServiceLaborCost | DECIMAL(12,2) | Cost allocated to service jobs |
| NonDirectLaborCost | DECIMAL(12,2) | Remaining labor cost |

**Business rules:**

- LaborKey must be unique and non-null.
- EmployeeKey, DateKey, and LocationKey must reference valid dimensions.
- The combination of EmployeeKey, DateKey, and LocationKey must be unique.
- Employees may have records at multiple locations on the same date.
- All hours must be nonnegative.
- TotalWorkedHours = RegularHours + OvertimeHours.
- BillableHours + NonBillableHours = TotalWorkedHours.
- AvailableProductiveHours must be greater than or equal to BillableHours and less than or equal to TotalWorkedHours.
- BillableHours must reconcile with the employee's allocated service-job hours.
- BaseHourlyRate must represent the rate effective on the work date.
- OvertimeMultiplier defaults to 1.50 for qualifying overtime.
- EmployerBurdenRate defaults to 0.25 in the initial synthetic model.
- GrossWages = (RegularHours × BaseHourlyRate) + (OvertimeHours × BaseHourlyRate × OvertimeMultiplier).
- EmployerBurdenCost = GrossWages × EmployerBurdenRate.
- FullyLoadedLaborCost = GrossWages + EmployerBurdenCost.
- DirectServiceLaborCost equals the sum of allocated direct labor costs associated with the labor record.
- NonDirectLaborCost = FullyLoadedLaborCost - DirectServiceLaborCost.
- All monetary calculations must use decimal arithmetic and documented rounding rules.
- FullyLoadedLaborCost must reconcile with DirectServiceLaborCost + NonDirectLaborCost.
- ScheduledHours must not be interpreted as actual hours worked.
- OvertimeHours is an input from the simulated payroll process, not automatically inferred from daily hours.
- Labor costs are recorded once in FactLabor and must not be duplicated in FactExpenses.

### 3.4 FactJobLaborAllocation

**Grain:** One employee's labor allocation from one FactLabor record to one service job.

**Primary key:** `JobLaborAllocationKey`

| Column | Data Type | Description |
|---|---|---|
| JobLaborAllocationKey | BIGINT | Unique labor allocation identifier |
| LaborKey | BIGINT | Source FactLabor record |
| ServiceJobKey | BIGINT | Service job receiving labor |
| AllocatedRegularHours | DECIMAL(6,2) | Regular hours attributed to job |
| AllocatedOvertimeHours | DECIMAL(6,2) | Overtime hours attributed to job |
| AllocatedHours | DECIMAL(6,2) | Total hours attributed to job |
| AllocatedDirectLaborCost | DECIMAL(12,2) | Fully loaded labor cost attributed to job |

**Business rules:**

- JobLaborAllocationKey must be unique and non-null.
- LaborKey must reference an existing FactLabor record.
- ServiceJobKey must reference an existing FactServiceJobs record.
- The combination of LaborKey and ServiceJobKey must be unique.
- All allocated hours and costs must be nonnegative.
- AllocatedHours = AllocatedRegularHours + AllocatedOvertimeHours.
- Total allocated regular hours must not exceed the source labor record's RegularHours.
- Total allocated overtime hours must not exceed the source labor record's OvertimeHours.
- Total allocated hours per LaborKey must equal FactLabor.BillableHours.
- AllocatedDirectLaborCost uses the historical wage, overtime multiplier, and employer burden from the source FactLabor record.
- AllocatedDirectLaborCost = (AllocatedRegularHours × BaseHourlyRate + AllocatedOvertimeHours × BaseHourlyRate × OvertimeMultiplier) × (1 + EmployerBurdenRate), subject to documented rounding reconciliation.
- Total AllocatedDirectLaborCost per LaborKey must equal FactLabor.DirectServiceLaborCost.
- Allocation work dates must fall within the service job's valid work period.
- Initial-model allocations are limited to completed, revenue-generating jobs.
- Labor spent on cancelled, no-show, or otherwise unbilled jobs remains non-direct labor in the initial model.
- Service jobs may have multiple labor allocations from different employees or dates.
- Allocations must not create additional payroll expense.
- AllocatedDirectLaborCost is used for job profitability, not added again to company-wide labor expense.

**Job-level profitability:**

ServiceJobGrossProfit = ServiceRevenue - PartsCost - SUM(AllocatedDirectLaborCost)

**Reconciliation requirement:**

SUM(FactLabor.DirectServiceLaborCost) =
SUM(FactJobLaborAllocation.AllocatedDirectLaborCost)

The reconciliation must hold within the complete dataset and within any consistently defined reporting period or location.

**Power BI modeling note:**

FactJobLaborAllocation is a supporting fact table, not a conventional dimension.

Avoid unrestricted bidirectional fact-to-fact filtering. Employee, date, and location analysis will primarily use shared dimensions. Job-level allocations will use explicit, tested relationships or DAX calculations to avoid ambiguous filter paths.


### 3.5 FactExpenses

**Grain:** One posted non-payroll operating expense entry attributable to one location and expense category.

**Primary key:** `ExpenseKey`

| Column | Data Type | Description |
|---|---|---|
| ExpenseKey | BIGINT | Unique operating expense entry |
| ExpenseReference | VARCHAR(30) | Fictional accounting entry reference |
| DateKey | INTEGER | Accounting recognition date |
| LocationKey | INTEGER | Location receiving expense allocation |
| ExpenseCategoryKey | INTEGER | Operating expense classification |
| VendorCode | VARCHAR(30) | Fictional vendor reference |
| ExpenseDescription | VARCHAR(250) | Description of the expense |
| ExpenseAmount | DECIMAL(12,2) | Signed expense amount in USD |
| IsRecurring | BOOLEAN | Indicates recurring expense |
| AllocationMethod | VARCHAR(30) | Direct or Allocated |

**Business rules:**

- ExpenseKey must be unique and non-null.
- ExpenseReference must identify a unique accounting entry.
- DateKey, LocationKey, and ExpenseCategoryKey must reference valid dimensions.
- ExpenseAmount is positive for recognized expenses and negative for reversals or credits.
- Zero-value expense entries are excluded from the initial dataset.
- Expenses must be recognized in the period to which they relate.
- FactExpenses excludes retail product COGS.
- FactExpenses excludes service parts costs already recorded in FactServiceJobs.
- FactExpenses excludes all employee wages and employer burden already recorded in FactLabor.
- FactExpenses excludes inventory purchases that have not yet become recognized expenses.
- Expense categories must be consistent with DimExpenseCategory.
- Direct expenses belong to the location that incurred them.
- Shared operating expenses must be allocated across locations using a documented allocation method.
- Shared expense allocations must sum to the original expense amount.
- All expense amounts exclude recoverable sales taxes.
- No expense may be counted more than once in company-wide profitability.

**Financial calculation:**

NonPayrollOperatingExpenses = SUM(FactExpenses.ExpenseAmount)

TotalOperatingExpenses =
NonPayrollOperatingExpenses +
SUM(FactLabor.NonDirectLaborCost)

**Profitability treatment:**

OperatingProfit =
RetailNetRevenue +
ServiceNetRevenue -
RetailCOGS -
ServicePartsCost -
DirectServiceLaborCost -
NonDirectLaborCost -
NonPayrollOperatingExpenses

Operating expenses are separate from direct service labor and retail COGS.

### 3.6 FactInventorySnapshot

**Grain:** One product, one location, one month-end snapshot date.

**Primary key:** `InventorySnapshotKey`

| Column | Data Type | Description |
|---|---|---|
| InventorySnapshotKey | BIGINT | Unique inventory snapshot identifier |
| DateKey | INTEGER | Month-end snapshot date |
| LocationKey | INTEGER | Location holding inventory |
| ProductKey | INTEGER | Product SKU |
| UnitsOnHand | INTEGER | Physical inventory units |
| UnitsReserved | INTEGER | Units reserved for pending orders |
| UnitsAvailable | INTEGER | Units available for sale |
| UnitInventoryCost | DECIMAL(12,2) | Weighted-average inventory unit cost |
| InventoryValue | DECIMAL(14,2) | Total inventory carrying value |
| ReorderPoint | INTEGER | Location-specific reorder threshold |
| DaysSinceLastSale | INTEGER | Days since last recorded sale at location |
| StockStatus | VARCHAR(30) | Derived inventory status |

**StockStatus values:**

- Healthy
- Low Stock
- Out of Stock
- Overstocked

**Business rules:**

- InventorySnapshotKey must be unique and non-null.
- DateKey, LocationKey, and ProductKey must reference valid dimensions.
- The combination of DateKey, LocationKey, and ProductKey must be unique.
- Snapshot dates must represent the final calendar day of each month.
- UnitsOnHand, UnitsReserved, and UnitsAvailable must be nonnegative.
- UnitsReserved must not exceed UnitsOnHand.
- UnitsAvailable = UnitsOnHand - UnitsReserved.
- UnitInventoryCost must be nonnegative.
- InventoryValue = UnitsOnHand × UnitInventoryCost.
- ReorderPoint may vary by location and product.
- DaysSinceLastSale must be nonnegative when populated.
- DaysSinceLastSale is null when no historical sale exists at the location.
- StockStatus must be derived from documented inventory thresholds.
- Overstock thresholds must account for product demand and expected replenishment cycles.
- Inventory snapshots must reflect simulated sales, returns, receipts, and inventory adjustments.
- Inventory balances must not be summed across multiple snapshot dates.
- Product-location combinations with zero inventory must remain represented.
- Inventory valuation must use consistent weighted-average cost assumptions.
- Inventory values represent assets, not operating expenses.

**Inventory KPIs:**

EndingInventoryValue =
SUM(InventoryValue) for the latest applicable snapshot date.

AverageInventoryValue =
Average of relevant period-end inventory balances.

InventoryTurnover =
RetailCOGS / AverageInventoryValue.

DaysInventoryOutstanding =
DaysInPeriod / InventoryTurnover.

**Important aggregation rule:**

InventoryValue is additive across products and locations for a single snapshot date but is not additive across time.

Power BI measures must explicitly select appropriate snapshot dates.

Inventory turnover and days inventory outstanding require consistent reporting periods and a positive average inventory balance.

**Inventory data limitation:**

Monthly snapshots support inventory valuation, turnover, and month-end stock analysis.

They do not establish the exact number of stockout days or the timing of replenishment events.

Daily stockout rates and detailed inventory movement analysis require additional source data and are outside the initial model.


## 4. Model Architecture Status

All seven initial dimension tables and six fact tables have been defined.

**Dimensions:**

- DimDate
- DimLocation
- DimCustomer
- DimProduct
- DimService
- DimEmployee
- DimExpenseCategory

**Fact tables:**

- FactSales
- FactServiceJobs
- FactLabor
- FactJobLaborAllocation
- FactExpenses
- FactInventorySnapshot

**Architecture decisions still pending:**

- Final relationship and filter-direction definitions
- Date role handling
- Financial reconciliation and rounding specifications
- Synthetic data generation constraints
- Data quality and validation tests
- Power BI semantic model implementation

## 5. Model Status

- [x] Define initial architecture principles
- [x] Define all seven dimensions
- [x] Define FactSales
- [x] Define FactServiceJobs
- [x] Define remaining fact tables
- [x] Define job-labor allocation rules
- [ ] Define relationships and filter directions
- [ ] Define financial calculations
- [ ] Define validation rules
- [ ] Generate synthetic data
- [ ] Import data into Power BI

## 6. Relationships and Filter Direction

### 6.1 Relationship Strategy

The Northstar Power BI semantic model uses shared dimensions and multiple fact tables.

**General rules:**

- All dimension-to-fact relationships are one-to-many.
- Dimension tables are on the one side.
- Fact tables are on the many side.
- Cross-filter direction is Single.
- Dimensions filter facts.
- No active fact-to-fact relationships are permitted in the initial model.
- All foreign keys must reference valid dimension keys.
- Relationships must not create ambiguous active filter paths.

### 6.2 Active Relationships

| Dimension | Dimension Key | Fact Table | Foreign Key |
|---|---|---|---|
| DimDate | DateKey | FactSales | DateKey |
| DimDate | DateKey | FactLabor | DateKey |
| DimDate | DateKey | FactExpenses | DateKey |
| DimDate | DateKey | FactInventorySnapshot | DateKey |
| DimDate | DateKey | FactServiceJobs | ScheduledDateKey |
| DimLocation | LocationKey | FactSales | LocationKey |
| DimLocation | LocationKey | FactServiceJobs | LocationKey |
| DimLocation | LocationKey | FactLabor | LocationKey |
| DimLocation | LocationKey | FactExpenses | LocationKey |
| DimLocation | LocationKey | FactInventorySnapshot | LocationKey |
| DimCustomer | CustomerKey | FactSales | CustomerKey |
| DimCustomer | CustomerKey | FactServiceJobs | CustomerKey |
| DimProduct | ProductKey | FactSales | ProductKey |
| DimProduct | ProductKey | FactInventorySnapshot | ProductKey |
| DimService | ServiceKey | FactServiceJobs | ServiceKey |
| DimEmployee | EmployeeKey | FactLabor | EmployeeKey |
| DimEmployee | EmployeeKey | FactServiceJobs | EmployeeKey |
| DimExpenseCategory | ExpenseCategoryKey | FactExpenses | ExpenseCategoryKey |

### 6.3 Inactive Date Relationships

The following relationship is inactive:

DimDate.DateKey ->
FactServiceJobs.CompletedDateKey

Completed-date measures will use USERELATIONSHIP() to activate
DimDate.DateKey -> FactServiceJobs.CompletedDateKey.

These measures must also use CROSSFILTER() with NONE to disable
the active ScheduledDateKey relationship for that calculation.

This prevents the selected reporting period from requiring
both the scheduled date and completed date to fall within
the same date range.

Service revenue and service parts costs must be reported
using completed dates.

Measures must explicitly identify whether they use scheduled dates or completed dates.

Service revenue reporting must use completion dates, not scheduled dates.

### 6.4 Supporting Fact Table

FactJobLaborAllocation contains:

- JobLaborAllocationKey
- LaborKey
- ServiceJobKey
- AllocatedRegularHours
- AllocatedOvertimeHours
- AllocatedHours
- AllocatedDirectLaborCost

LaborKey references FactLabor.LaborKey.

ServiceJobKey references FactServiceJobs.ServiceJobKey.

The initial Power BI model will not create active relationships between FactJobLaborAllocation and other fact tables.

Job-level labor costs will be calculated through explicit DAX filtering using matching ServiceJobKey values.

Employee, date, and location allocations must be validated against their source FactLabor records.

Company-wide direct service labor cost will be sourced from FactLabor to avoid duplication.

**Initial Power BI allocation strategy:**

- FactLabor remains the authoritative source for payroll expenses.
- FactJobLaborAllocation is used for job-level profitability.
- Job-level allocation measures use TREATAS() to apply selected
  ServiceJobKey values to FactJobLaborAllocation.
- Company-wide direct labor expense is never calculated by adding
  allocation costs to FactLabor costs.
- Employee and work-date allocation analysis will use explicit
  measures and reconciliation tests.
- Job-level profitability measures must be tested under date,
  location, service, and employee filters.
- Primary technician filters do not necessarily represent every
  employee who worked on a job.

### 6.5 Additional Foreign Key Constraints

The following attributes also reference DimLocation:

- DimCustomer.HomeLocationKey
- DimEmployee.HomeLocationKey

These relationships are maintained in source data and PostgreSQL but are not active Power BI relationships in the initial model.

Customer and employee home locations must not override the actual transaction or worked location.

### 6.6 Relationship Validation

Before Power BI implementation:

- Verify dimension primary key uniqueness.
- Verify foreign key referential integrity.
- Verify fact table grains.
- Verify no unexpected many-to-many relationships.
- Verify single-direction filtering.
- Verify scheduled-date and completed-date calculations independently.
- Verify location totals reconcile with company-wide totals.
- Verify job-level allocated labor costs reconcile with FactLabor.

## 7. Financial Definitions and Reconciliation

### 7.1 Accounting Basis

Northstar uses a simplified accrual-based financial model.

- Currency: USD.
- Monetary values are stored using decimal arithmetic.
- Source monetary amounts are rounded to two decimal places.
- Revenue excludes sales tax.
- Retail revenue is recognized on posted sales and returns.
- Service revenue is recognized when jobs are completed.
- Labor costs are recognized on the dates work occurs.
- Non-payroll expenses are recognized in their applicable accounting periods.
- Inventory purchases are not immediately recognized as operating expenses.
- Financing costs, income taxes, depreciation, and amortization are outside the initial model.

The resulting OperatingProfit metric is a simplified operating profit before excluded items.

### 7.2 Revenue

RetailNetRevenue =
SUM(FactSales.NetRevenue)

ServiceNetRevenue =
SUM(FactServiceJobs.ServiceRevenue)

TotalRevenue =
RetailNetRevenue + ServiceNetRevenue

Retail returns reduce retail revenue.

Service revenue is recognized using CompletedDateKey.

Cancelled, scheduled, and no-show appointments have zero earned service revenue in the initial model.

### 7.3 Direct Costs

RetailCOGS =
SUM(FactSales.TotalCOGS)

ServicePartsCost =
SUM(FactServiceJobs.PartsCost)

DirectServiceLaborCost =
SUM(FactLabor.DirectServiceLaborCost)

TotalDirectCosts =
RetailCOGS +
ServicePartsCost +
DirectServiceLaborCost

Service parts costs are recognized when the related job is completed in the initial model.

Direct service labor costs are recognized on the dates work was performed.

### 7.4 Gross Profit

RetailGrossProfit =
RetailNetRevenue - RetailCOGS

ServiceGrossProfit =
ServiceNetRevenue -
ServicePartsCost -
DirectServiceLaborCost

TotalGrossProfit =
RetailGrossProfit + ServiceGrossProfit

GrossMarginPct =
TotalGrossProfit / TotalRevenue

Division by zero returns a blank or explicitly documented undefined value.

### 7.5 Operating Expenses

NonDirectLaborCost =
SUM(FactLabor.NonDirectLaborCost)

NonPayrollOperatingExpenses =
SUM(FactExpenses.ExpenseAmount)

TotalOperatingExpenses =
NonDirectLaborCost +
NonPayrollOperatingExpenses

Operating expenses exclude costs already classified as direct costs.

### 7.6 Operating Profit

OperatingProfit =
TotalGrossProfit - TotalOperatingExpenses

Equivalent reconciliation formula:

OperatingProfit =
TotalRevenue -
RetailCOGS -
ServicePartsCost -
SUM(FactLabor.FullyLoadedLaborCost) -
NonPayrollOperatingExpenses

Both calculations must produce the same result.

OperatingMarginPct =
OperatingProfit / TotalRevenue

### 7.7 Job-Level Profitability

JobDirectLaborCost =
SUM(FactJobLaborAllocation.AllocatedDirectLaborCost)
for the selected service job.

JobGrossProfit =
ServiceRevenue -
PartsCost -
JobDirectLaborCost

JobGrossMarginPct =
JobGrossProfit / ServiceRevenue

Job-level labor allocation must reconcile with FactLabor.

Job-level profitability and calendar-period profitability may differ because labor costs and service revenue can be recognized on different dates.

### 7.8 Labor Cost Reconciliation

For every FactLabor record:

FullyLoadedLaborCost =
DirectServiceLaborCost + NonDirectLaborCost

For the complete dataset:

SUM(FactLabor.DirectServiceLaborCost) =
SUM(FactJobLaborAllocation.AllocatedDirectLaborCost)

The allocation reconciliation must also hold for comparable employee, work-date, and worked-location groupings.

Allocation amounts must never be added to company-wide payroll costs a second time.

### 7.9 Inventory Valuation

InventoryValue =
UnitsOnHand × UnitInventoryCost

EndingInventoryValue is calculated using the final available snapshot date in the selected reporting period.

InventoryValue must not be summed across different snapshot dates.

InventoryTurnover =
PeriodRetailCOGS / AverageInventoryValue

AverageInventoryValue must use a documented sequence of opening and closing inventory balances.

A December 31, 2024 opening snapshot will be generated to support January 2025 inventory analysis.

Inventory turnover is undefined when average inventory value is zero or negative.

### 7.10 Rounding and Validation

- Use fixed-precision decimal calculations for currency.
- Round stored monetary values to two decimal places using ROUND_HALF_UP.
- Calculate line-level amounts before aggregation.
- Reconcile allocation rounding differences within the originating labor record.
- Financial identities must reconcile to the cent.
- Do not use binary floating-point arithmetic for authoritative financial calculations.
- Negative operating profit is valid and must not be automatically corrected.
- Negative retail revenue or COGS may occur due to returns.
- Financial reconciliation failures must stop the synthetic data generation validation process.

### 7.11 Required Financial Tests

- Retail net revenue equals the sum of posted sales and returns.
- Retail COGS equals the sum of signed transaction costs.
- Total revenue equals retail plus service revenue.
- Fully loaded labor equals direct plus non-direct labor.
- Allocated job labor equals direct service labor.
- Gross profit equals revenue minus direct costs.
- Operating profit equals gross profit minus operating expenses.
- Operating profit also equals revenue minus all recognized costs.
- Company-wide totals equal the sum of location-level totals.
- Inventory snapshots are not summed across dates.
- No cost is counted twice.
