# Northstar Home & Tech
## Business Performance Analytics — Portfolio Case Study

**Project:** 002 — Northstar Business Performance Analytics
**Organization:** Northstar Home & Tech (fictional)
**Reporting period:** January 2025–December 2026
**Technology:** Python, PostgreSQL, SQL, Power BI, DAX
**Data classification:** Fully synthetic

## 1. Executive Summary

Northstar Home & Tech is a fictional retailer and technology services provider operating three business locations. Its operations include retail product sales, device repairs, technical support, network installation, and smart-home services.

This analytics project developed an integrated reporting solution to evaluate the company's financial performance, workforce productivity, operating expenses, and inventory position.

The completed solution combines 13 analytical tables containing 106,997 synthetic records with six interactive Power BI business dashboards.

Across the two-year reporting period, Northstar generated $19.88 million in revenue and an estimated operating result of $716,171.96. However, the analysis identified meaningful differences in profitability between locations, product categories, and service activities.

The findings demonstrate how integrated business intelligence can support more informed operational and financial decisions.

## 2. Business Challenge

Northstar's simulated retail, service, workforce, expense, and inventory data originates from different business processes.

Analyzing these activities independently can make it difficult to understand how operational performance contributes to overall profitability.

The project addresses several management questions:

- Which locations generate profitable operating results?
- Which retail categories provide the strongest margins?
- How do service operations contribute to gross profit?
- How do labor costs and technician utilization affect profitability?
- Where are non-payroll operating costs concentrated?
- How is inventory investment distributed across products and locations?

The objective was to develop a unified analytical view rather than a collection of unrelated reports.

## 3. Analytical Solution

The solution uses a dimensional PostgreSQL analytical warehouse populated by Python-generated synthetic data.

Power BI provides six interactive reporting pages:

| Dashboard | Primary purpose |
|---|---|
| Executive Overview | Consolidated revenue, profitability, cost ratios, and trends |
| Retail Sales Performance | Product-category revenue, gross profit, margins, and rankings |
| Service Operations | Completed-service revenue, profitability, and category performance |
| Labor & Workforce | Payroll, direct labor allocation, hours, and technician utilization |
| Operating Expenses | Non-payroll expense composition, trends, and location profitability |
| Inventory Performance | Closing inventory valuation, availability, and reorder indicators |

Synchronized Year and Location slicers allow users to examine consistent reporting contexts across the dashboards.

Financial and inventory calculations were independently reconciled against PostgreSQL aggregates for documented reporting periods.

## 4. Key Business Findings

### Finding 1 — Northstar East Requires Profitability Review

Across 2025–2026, Northstar East generated $4,633,936.48 in total revenue but recorded an estimated operating loss of $65,982.09.

By comparison, Northstar Central generated an estimated operating result of $591,180.49, while Northstar West generated $190,973.56.

Northstar East also recorded the highest technician utilization at 46.18%, compared with 37.82% for Central and 35.93% for West.

These findings demonstrate that relatively high technician utilization does not automatically translate into overall location profitability.

East's reported gross profit of $1,040,227.14 was insufficient to cover its $824,802.43 in non-direct labor and $281,406.80 in non-payroll operating expenses.

**Recommended management investigation:** Review East's retail and service revenue mix, staffing and scheduling, non-direct labor allocation, and location-level gross margins before making staffing or cost-reduction decisions.

### Finding 2 — Retail Product Categories Have Different Profit Profiles

Across the reporting period, Northstar's retail product categories produced materially different gross margins:

| Product category | Retail gross margin |
|---|---:|
| Accessories | 44.46% |
| Smart Home | 32.76% |
| Networking | 27.73% |
| Computers | 13.26% |

Computers generated substantial revenue but had the lowest gross margin among the four categories.

At the December 2025 inventory snapshot, computers represented approximately 60% of Northstar's total inventory valuation.

This combination raises questions about capital allocation and the relationship between sales volume, product margins, and inventory investment.

**Recommended management investigation:** Compare product-category sales velocity, profitability, inventory investment, and replenishment policies. Evaluate opportunities to improve product mix and complementary accessory sales without assuming that low-margin categories should be eliminated.

### Finding 3 — Non-Payroll Expenses Are Concentrated in Two Categories

Northstar recorded $1,005,670.94 in non-payroll operating expenses.

Merchant Processing Fees accounted for $496,926.43, while Rent accounted for $278,400.00.

Together, these categories represented approximately 77.1% of non-payroll operating expenses.

This concentration provides management with a focused starting point for cost analysis.

**Recommended management investigation:** Review payment processing assumptions, transaction economics, lease arrangements, and expense allocation policies. Because some costs are necessary or revenue-dependent, the analysis does not establish that they are excessive.

### Finding 4 — Service Profitability Varies by Activity

Completed technical services generated $1,004,778.85 in revenue and $394,949.75 in gross profit, representing a 39.31% gross margin.

Service-category analysis identified differences in gross profitability.

Technical Support achieved a gross margin of approximately 56.32%, while Computer Repair achieved approximately 22.99%.

These differences reflect varying combinations of service pricing, parts costs, and direct labor requirements.

**Recommended management investigation:** Evaluate service pricing, technician time requirements, parts consumption, and demand patterns by service category. Review opportunities to improve lower-margin services while preserving customer value.

### Finding 5 — Inventory Availability Is High, but the Simulation Limits Interpretation

At December 31, 2026, Northstar held $2,004,290.88 in inventory representing 14,549 units on hand.

Of those units, 14,275 were available and 274 were reserved.

No product-location inventory positions were below their recorded reorder points.

The synthetic data also contained no positions with 30 or more days since their last recorded sale at the December 2026 snapshot.

These results reflect the inventory simulation's replenishment and sales-generation assumptions rather than proven real-world inventory optimization.

**Recommended management investigation:** In a production implementation, incorporate actual supplier lead times, replenishment variability, aging, turnover, and stockout history before developing inventory-efficiency recommendations.

## 5. Business Value

Northstar demonstrates several practical benefits of integrated business intelligence.

**Financial visibility:** Management can compare revenue, gross profit, expenses, and operating results across locations.

**Operational insight:** Retail, service, and workforce performance can be evaluated using shared reporting dimensions.

**Cost transparency:** Direct service labor and non-direct labor are distinguished to avoid double-counting costs.

**Inventory awareness:** Month-end inventory balances are reported using point-in-time calculations rather than inappropriate aggregation across reporting periods.

**Decision support:** The dashboards reveal issues that warrant investigation and provide a foundation for more detailed operational analysis.

## 6. Technical and Validation Highlights

The project incorporates:

- Python-based synthetic data generation.
- A 13-table PostgreSQL analytical warehouse.
- Dimensional data modeling.
- SQL-based financial and operational validation.
- DAX measures for revenue, margins, labor, expenses, and inventory.
- Job-level direct labor allocation for service profitability.
- Snapshot-aware inventory valuation.
- Six interactive Power BI dashboards.
- Synchronized Year and Location slicers.
- Independent reconciliation of selected reporting contexts.

Detailed validation evidence is available in [Data and Report Validation](validation.md).

## 7. Limitations

Northstar is entirely fictional. No actual business, customer, employee, or transaction information was used.

The project demonstrates an analytical approach rather than measuring the performance of an actual company.

Important limitations include simplified staffing patterns, modeled employer payroll burden, fixed expense allocation assumptions, simulated inventory replenishment, and a limited inventory-aging distribution.

Estimated operating results are analytical estimates based on the project's defined financial model, not audited financial statements.

The recommendations are proposed areas for investigation, not evidence that specific management interventions will produce financial improvements.

## 8. Conclusion

Northstar Business Performance Analytics demonstrates the design, development, validation, and presentation of an integrated business intelligence solution.

By connecting retail sales, technical services, workforce costs, operating expenses, and inventory data, the project moves beyond isolated reporting toward a more complete view of business performance.

The resulting dashboards support meaningful management questions, including why a location with relatively high technician utilization may still operate at a loss, how retail margin differences relate to inventory investment, and where operating expenses are concentrated.

The solution serves as a portfolio demonstration of the analytical and reporting capabilities that could be adapted to real business environments.

---

**Portfolio project:** Analytics Lab — Project 002
**Prepared as a synthetic business intelligence demonstration**
