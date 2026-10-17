"""
Northstar Home & Tech
Project 002 — Northstar Business Performance Analytics

Generate reproducible synthetic fact tables.

Fact tables:
    - FactSales
    - FactServiceJobs
    - FactLabor
    - FactJobLaborAllocation
    - FactExpenses
    - FactInventorySnapshot

Reporting period:
    January 1, 2025 through December 31, 2026.
"""

from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2026-12-31")

RANDOM_SEED = 2029


def money(value) -> Decimal:
    """Round monetary values to two decimal places."""

    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def load_dimensions() -> dict[str, pd.DataFrame]:
    """Load the seven existing Northstar dimension tables."""

    dimension_names = [
        "DimDate",
        "DimLocation",
        "DimCustomer",
        "DimProduct",
        "DimService",
        "DimEmployee",
        "DimExpenseCategory",
    ]

    dimensions = {}

    for name in dimension_names:
        path = DATA_DIR / f"{name}.csv"

        if not path.exists():
            raise FileNotFoundError(
                f"Required dimension file missing: {path}"
            )

        dimensions[name] = pd.read_csv(path)

    return dimensions

def generate_sales(
    dimensions: dict[str, pd.DataFrame],
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate Northstar retail sales with realistic demand patterns."""

    customers = dimensions["DimCustomer"].copy()
    products = dimensions["DimProduct"].copy()

    customers["SignupDate"] = pd.to_datetime(customers["SignupDate"])

    active_products = products.loc[
        products["IsActive"].astype(str).str.lower() == "true"
    ].copy()

    if active_products.empty:
        raise ValueError("No active products available for sales.")

    # Retail activity varies by location.
    location_weights = {
        1: 0.43,  # Northstar Central
        2: 0.35,  # Northstar West
        3: 0.22,  # Northstar East
    }

    # Seasonal demand multipliers.
    month_weights = {
        1: 0.85,
        2: 0.88,
        3: 0.95,
        4: 0.97,
        5: 1.00,
        6: 1.05,
        7: 1.08,
        8: 1.02,
        9: 0.96,
        10: 1.08,
        11: 1.35,
        12: 1.55,
    }

    dates = pd.date_range(START_DATE, END_DATE, freq="D")

    date_weights = np.array(
        [
            month_weights[date.month]
            * (1.18 if date.dayofweek >= 5 else 1.0)
            for date in dates
        ],
        dtype=float,
    )

    date_weights /= date_weights.sum()

    transaction_count = 35_000

    transaction_dates = rng.choice(
        dates.to_numpy(),
        size=transaction_count,
        p=date_weights,
    )

    transaction_dates.sort()

    product_keys = active_products["ProductKey"].to_numpy()
    product_lookup = active_products.set_index("ProductKey")

    customers = customers.sort_values("SignupDate").reset_index(drop=True)
    customer_keys = customers["CustomerKey"].to_numpy()
    customer_signup_dates = customers["SignupDate"].to_numpy()
    customer_home_locations = customers["HomeLocationKey"].to_numpy()

    sales_records = []
    sales_line_key = 1

    for transaction_number, transaction_date in enumerate(
        transaction_dates,
        start=1,
    ):
        transaction_date = pd.Timestamp(transaction_date)

        location_key = int(
            rng.choice(
                list(location_weights.keys()),
                p=list(location_weights.values()),
            )
        )

        eligible_count = int(
            np.searchsorted(
                customer_signup_dates,
                np.datetime64(transaction_date),
                side="right",
            )
        )

        if eligible_count == 0:
            continue

        customer_index = int(rng.integers(0, eligible_count))
        customer_key = int(customer_keys[customer_index])

        transaction_id = f"NS-TXN-{transaction_number:07d}"

        line_count = int(
            rng.choice(
                [1, 2, 3, 4],
                p=[0.58, 0.27, 0.11, 0.04],
            )
        )

        selected_products = rng.choice(
            product_keys,
            size=line_count,
            replace=False,
        )

        for product_key in selected_products:
            product = product_lookup.loc[int(product_key)]

            quantity = int(
                rng.choice(
                    [1, 2, 3],
                    p=[0.88, 0.10, 0.02],
                )
            )

            unit_price = money(product["StandardRetailPrice"])
            unit_cost = money(product["StandardUnitCost"])

            # West discounts more aggressively.
            discount_probability = (
                0.48 if location_key == 2 else 0.24
            )

            discount_rate = Decimal("0.00")

            if rng.random() < discount_probability:
                discount_rate = Decimal(
                    str(rng.choice([0.05, 0.10, 0.15, 0.20]))
                )

            gross_revenue = money(quantity * unit_price)
            discount_amount = money(
                gross_revenue * discount_rate
            )

            net_revenue = money(
                gross_revenue - discount_amount
            )

            total_cogs = money(quantity * unit_cost)

            sales_records.append(
                {
                    "SalesLineKey": sales_line_key,
                    "TransactionID": transaction_id,
                    "OriginalSalesLineKey": None,
                    "DateKey": int(
                        transaction_date.strftime("%Y%m%d")
                    ),
                    "LocationKey": location_key,
                    "CustomerKey": customer_key,
                    "ProductKey": int(product_key),
                    "TransactionType": "Sale",
                    "Quantity": quantity,
                    "UnitListPrice": unit_price,
                    "DiscountAmount": discount_amount,
                    "NetRevenue": net_revenue,
                    "UnitCost": unit_cost,
                    "TotalCOGS": total_cogs,
                }
            )

            sales_line_key += 1

    return pd.DataFrame(sales_records)

def generate_returns(
    sales: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate returns referencing original retail sales."""

    return_records = []
    next_sales_line_key = int(sales["SalesLineKey"].max()) + 1

    original_sales = sales.loc[
        sales["TransactionType"] == "Sale"
    ].copy()

    # Approximately 5% of sales lines experience a return.
    return_count = int(len(original_sales) * 0.05)

    selected_indices = rng.choice(
        original_sales.index.to_numpy(),
        size=return_count,
        replace=False,
    )

    for return_number, index in enumerate(selected_indices, start=1):
        original = original_sales.loc[index]

        original_date = pd.to_datetime(
            str(original["DateKey"]),
            format="%Y%m%d",
        )

        days_until_return = int(rng.integers(1, 31))
        return_date = original_date + pd.Timedelta(
            days=days_until_return
        )

        # Do not generate returns outside the reporting period.
        if return_date > END_DATE:
            continue

        original_quantity = int(original["Quantity"])

        return_quantity = int(
            rng.integers(1, original_quantity + 1)
        )

        quantity = -return_quantity

        unit_price = money(original["UnitListPrice"])
        unit_cost = money(original["UnitCost"])

        # Reverse the proportional discount from the original sale.
        original_discount = money(original["DiscountAmount"])

        discount_per_unit = (
            original_discount / Decimal(original_quantity)
        )

        discount_amount = money(
            discount_per_unit * quantity
        )

        net_revenue = money(
            Decimal(quantity) * unit_price - discount_amount
        )

        total_cogs = money(
            Decimal(quantity) * unit_cost
        )

        return_records.append(
            {
                "SalesLineKey": next_sales_line_key,
                "TransactionID": f"NS-RET-{return_number:07d}",
                "OriginalSalesLineKey": int(original["SalesLineKey"]),
                "DateKey": int(return_date.strftime("%Y%m%d")),
                "LocationKey": int(original["LocationKey"]),
                "CustomerKey": int(original["CustomerKey"]),
                "ProductKey": int(original["ProductKey"]),
                "TransactionType": "Return",
                "Quantity": quantity,
                "UnitListPrice": unit_price,
                "DiscountAmount": discount_amount,
                "NetRevenue": net_revenue,
                "UnitCost": unit_cost,
                "TotalCOGS": total_cogs,
            }
        )

        next_sales_line_key += 1

    return pd.DataFrame(return_records)

def validate_sales(
    sales: pd.DataFrame,
    dimensions: dict[str, pd.DataFrame],
) -> None:
    """Validate FactSales integrity and financial calculations."""

    required_columns = [
        "SalesLineKey",
        "TransactionID",
        "OriginalSalesLineKey",
        "DateKey",
        "LocationKey",
        "CustomerKey",
        "ProductKey",
        "TransactionType",
        "Quantity",
        "UnitListPrice",
        "DiscountAmount",
        "NetRevenue",
        "UnitCost",
        "TotalCOGS",
    ]

    assert list(sales.columns) == required_columns, (
        "FactSales schema does not match the data dictionary."
    )

    assert sales["SalesLineKey"].notna().all()
    assert sales["SalesLineKey"].is_unique

    assert sales["TransactionType"].isin(["Sale", "Return"]).all()

    sale_rows = sales["TransactionType"] == "Sale"
    return_rows = sales["TransactionType"] == "Return"

    assert (sales.loc[sale_rows, "Quantity"] > 0).all()
    assert (sales.loc[return_rows, "Quantity"] < 0).all()

    # Validate dimension foreign keys.
    foreign_keys = {
        "DateKey": "DimDate",
        "LocationKey": "DimLocation",
        "CustomerKey": "DimCustomer",
        "ProductKey": "DimProduct",
    }

    for column, dimension_name in foreign_keys.items():
        valid_keys = set(dimensions[dimension_name][column])

        assert sales[column].isin(valid_keys).all(), (
            f"Invalid foreign keys in {column}"
        )

    # Validate financial calculations using Decimal.
    for row in sales.itertuples(index=False):
        quantity = Decimal(int(row.Quantity))
        unit_price = money(row.UnitListPrice)
        discount = money(row.DiscountAmount)
        unit_cost = money(row.UnitCost)

        expected_revenue = money(
            quantity * unit_price - discount
        )

        expected_cogs = money(
            quantity * unit_cost
        )

        assert money(row.NetRevenue) == expected_revenue, (
            f"Revenue mismatch: SalesLineKey {row.SalesLineKey}"
        )

        assert money(row.TotalCOGS) == expected_cogs, (
            f"COGS mismatch: SalesLineKey {row.SalesLineKey}"
        )

    # Validate return references.
    originals = sales.loc[
        sale_rows
    ].set_index("SalesLineKey")

    returns = sales.loc[return_rows]

    assert returns["OriginalSalesLineKey"].notna().all()

    assert returns["OriginalSalesLineKey"].isin(
        originals.index
    ).all()

    for original_key, group in returns.groupby("OriginalSalesLineKey"):
        original = originals.loc[int(original_key)]

        assert abs(group["Quantity"].sum()) <= original["Quantity"], (
            f"Excessive returns against SalesLineKey {original_key}"
        )

        assert (group["CustomerKey"] == original["CustomerKey"]).all()
        assert (group["ProductKey"] == original["ProductKey"]).all()

        assert (group["DateKey"] > original["DateKey"]).all()

        assert (
            group["UnitCost"].apply(money)
            == money(original["UnitCost"])
        ).all()

    # Customers cannot transact before their signup dates.
    customer_signup = (
        dimensions["DimCustomer"]
        .set_index("CustomerKey")["SignupDate"]
    )

    transaction_dates = pd.to_datetime(
        sales["DateKey"].astype(str),
        format="%Y%m%d",
    )

    signup_dates = pd.to_datetime(
        sales["CustomerKey"].map(customer_signup)
    )

    assert (transaction_dates >= signup_dates).all(), (
        "Transactions exist before customer signup dates."
    )

    # All lines in a transaction must share a date,
    # customer, and processing location.
    transaction_consistency = sales.groupby("TransactionID")[
        ["DateKey", "CustomerKey", "LocationKey"]
    ].nunique()

    assert (transaction_consistency == 1).all().all(), (
        "Inconsistent transaction-level attributes."
    )

    # Prices and acquisition costs cannot be negative.
    assert (
        sales["UnitListPrice"].apply(money) >= Decimal("0")
    ).all()

    assert (
        sales["UnitCost"].apply(money) >= Decimal("0")
    ).all()

    # Discounts must have the appropriate sign.
    assert (
        sales.loc[sale_rows, "DiscountAmount"].apply(money)
        >= Decimal("0")
    ).all()

    assert (
        sales.loc[return_rows, "DiscountAmount"].apply(money)
        <= Decimal("0")
    ).all()

    # Returns must preserve the original unit price.
    for original_key, group in returns.groupby("OriginalSalesLineKey"):
        original = originals.loc[int(original_key)]

        assert (
            group["UnitListPrice"].apply(money)
            == money(original["UnitListPrice"])
        ).all(), (
            f"Return price mismatch: {original_key}"
        )

        assert (
            -group["DiscountAmount"].apply(money).sum()
            <= money(original["DiscountAmount"])
        ), (
            f"Excessive discount reversal: {original_key}"
        )

        # Returns cannot reverse more revenue or COGS
        # than the original sale recorded.
        assert (
            -group["NetRevenue"].apply(money).sum()
            <= money(original["NetRevenue"])
        ), (
            f"Excessive revenue reversal: {original_key}"
        )

        assert (
            -group["TotalCOGS"].apply(money).sum()
            <= money(original["TotalCOGS"])
        ), (
            f"Excessive COGS reversal: {original_key}"
        )

    print("FactSales validation passed.")

def technician_workdays(
    technicians: pd.DataFrame,
) -> dict[int, set[int]]:
    """
    Assign recurring five-day work schedules to service technicians.

    Weekdays use Python's convention:
    Monday = 0, Sunday = 6.
    """

    schedules = {}

    # Stagger schedules independently within each location.
    # Stagger technician schedules to preserve weekend coverage.
    # Monday = 0, Sunday = 6.
    #
    # A two-technician location needs complementary schedules
    # so at least one technician is available every weekday.
    workweek_starts = [0, 2, 4, 1, 3]

    for location_key, group in technicians.groupby(
        "HomeLocationKey"
    ):
        location_technicians = group.sort_values("EmployeeKey")

        for position, technician in enumerate(
            location_technicians.itertuples(index=False)
        ):
            start_day = workweek_starts[
                position % len(workweek_starts)
            ]

            schedules[int(technician.EmployeeKey)] = {
                (start_day + offset) % 7
                for offset in range(5)
            }

    return schedules

def generate_service_jobs(
    dimensions: dict[str, pd.DataFrame],
    rng: np.random.Generator,
) -> pd.DataFrame:
    """
    Generate Northstar service jobs for the reporting period.

    Service jobs will include:
    - Scheduled appointments and walk-in services
    - Technician assignments based on employment dates
    - Completed, cancelled, no-show, and pending jobs
    - Service revenue, discounts, and parts costs

    Technician workload will be coordinated with FactLabor
    and FactJobLaborAllocation.
    """

    services = dimensions["DimService"].copy()
    employees = dimensions["DimEmployee"].copy()
    customers = dimensions["DimCustomer"].copy()
    locations = dimensions["DimLocation"].copy()

    technicians = employees[
        employees["Department"] == "Service"
    ].copy()

        # Establish recurring technician work schedules.
    technician_schedules = technician_workdays(technicians)

    print("\nTechnician weekly schedules:")

    for employee_key, weekdays in sorted(
        technician_schedules.items()
    ):
        print(
            f"Employee {employee_key}: "
            f"{sorted(weekdays)}"
        )

    # Convert employment dates for historical eligibility checks.
    technicians["HireDate"] = pd.to_datetime(
        technicians["HireDate"]
    )

    technicians["TerminationDate"] = pd.to_datetime(
        technicians["TerminationDate"]
    )

    # Build a daily calendar of available service technicians.
    calendar = pd.date_range(
        START_DATE,
        END_DATE,
        freq="D"
    )

    staffing_records = []

    for date in calendar:
        eligible = technicians[
            (technicians["HireDate"] <= date)
            & (
                technicians["TerminationDate"].isna()
                | (technicians["TerminationDate"] >= date)
            )
        ]

        for location_key in locations["LocationKey"]:
            location_technicians = eligible[
                eligible["HomeLocationKey"] == location_key
            ].copy()

            # Only scheduled employees contribute to daily capacity.
            location_technicians = location_technicians[
                location_technicians["EmployeeKey"].map(
                    lambda employee_key: (
                        date.weekday()
                        in technician_schedules[int(employee_key)]
                    )
                )
            ]

            staffing_records.append(
                {
                    "Date": date,
                    "LocationKey": int(location_key),
                    "AvailableTechnicians": len(
                        location_technicians
                    ),
                }
            )

    staffing_calendar = pd.DataFrame(staffing_records)

    # Generate service demand based on historical staffing.
    # These are incoming requests, not completed jobs.
    demand_records = []

    for row in staffing_calendar.itertuples(index=False):
        date = row.Date
        location_key = row.LocationKey
        technician_count = row.AvailableTechnicians

        # Reduced demand on weekends.
        weekend_factor = 0.65 if date.weekday() >= 5 else 1.0

        # Location-specific demand patterns.
        location_factor = {
            1: 1.00,  # Central
            2: 0.85,  # West
            3: 1.15,  # East
        }[location_key]

        # Approximate incoming requests per technician.
        expected_requests = (
            technician_count
            * 2.8
            * weekend_factor
            * location_factor
        )

        # Poisson distribution introduces natural variation.
        requests = int(
            rng.poisson(expected_requests)
        )

        demand_records.append(
            {
                "Date": date,
                "LocationKey": location_key,
                "ServiceRequests": requests,
            }
        )

    demand_calendar = pd.DataFrame(demand_records)

    # Validate the service-demand calendar.
    expected_records = len(calendar) * len(locations)

    assert len(demand_calendar) == expected_records, (
        "Service demand calendar has missing records."
    )

    assert not demand_calendar[
        ["Date", "LocationKey", "ServiceRequests"]
    ].isna().any().any(), (
        "Service demand calendar contains null values."
    )

    assert (
        demand_calendar["ServiceRequests"] >= 0
    ).all(), (
        "Service demand contains negative request counts."
    )

    assert not demand_calendar.duplicated(
        subset=["Date", "LocationKey"]
    ).any(), (
        "Duplicate date/location combinations detected."
    )

    assert set(demand_calendar["LocationKey"]) == set(
        locations["LocationKey"]
    ), (
        "Service demand contains invalid location keys."
    )

    print("Service demand validation passed.")

    print(
        f"Service demand generated: "
        f"{demand_calendar['ServiceRequests'].sum():,} "
        f"requests."
    )

    print("\nService requests by location:")
    print(
        demand_calendar.groupby("LocationKey")[
            "ServiceRequests"
        ].sum().to_string()
    )

    print(
        f"Daily staffing calendar generated: "
        f"{len(staffing_calendar):,} records."
    )

    services = services[
        services["IsActive"] == True
    ].copy()

    print(
        f"Service-job generator initialized: "
        f"{len(services)} services, "
        f"{len(technicians)} technicians, "
        f"{len(customers):,} customers, "
        f"{len(locations)} locations."
    )

    # Convert daily demand into individual service requests.
    job_records = []
    job_key = 1

    customers["SignupDate"] = pd.to_datetime(
        customers["SignupDate"]
    )

    active_services = services[
        services["IsActive"] == True
    ].copy()

    # Weight service demand by estimated duration.
    # Shorter services tend to receive more requests.
    active_services["DemandWeight"] = (
        1.0
        / np.sqrt(
            active_services["EstimatedDurationHours"]
        )
    )

    # Normalize weights into selection probabilities.
    service_probabilities = (
        active_services["DemandWeight"]
        / active_services["DemandWeight"].sum()
    ).to_numpy()

    for row in demand_calendar.itertuples(index=False):
        request_date = row.Date
        location_key = int(row.LocationKey)

        # Customers must have signed up by the request date.
        eligible_customers = customers[
            customers["SignupDate"] <= request_date
        ]

        if eligible_customers.empty:
            continue

        for _ in range(int(row.ServiceRequests)):
            customer = eligible_customers.iloc[
                rng.integers(len(eligible_customers))
            ]

            service = active_services.iloc[
                rng.choice(
                    len(active_services),
                    p=service_probabilities,
                )
            ]

            job_records.append(
                {
                    "ServiceJobKey": job_key,
                    "JobReference": f"NS-JOB-{job_key:07d}",
                    "CustomerKey": int(customer["CustomerKey"]),
                    "LocationKey": location_key,
                    "ServiceKey": int(service["ServiceKey"]),
                    "RequestDate": request_date,
                }
            )

            job_key += 1

    service_jobs = pd.DataFrame(job_records)

    # Assign scheduled dates based on appointment requirements.
    appointment_lookup = services.set_index(
        "ServiceKey"
    )["RequiresAppointment"].to_dict()

    scheduled_dates = []

    for row in service_jobs.itertuples(index=False):
        request_date = row.RequestDate

        requires_appointment = bool(
            appointment_lookup[row.ServiceKey]
        )

        if requires_appointment:
            # Most appointments occur within one week.
            delay_days = int(
                rng.choice(
                    [1, 2, 3, 4, 5, 6, 7],
                    p=[0.25, 0.22, 0.18, 0.13, 0.10, 0.07, 0.05],
                )
            )
        else:
            # Walk-in and remote services can occur immediately.
            delay_days = 0

        scheduled_date = (
            request_date + pd.Timedelta(days=delay_days)
        )

        scheduled_dates.append(scheduled_date)

    service_jobs["ScheduledDate"] = pd.to_datetime(
        scheduled_dates
    )

    service_jobs["ScheduledDateKey"] = (
        service_jobs["ScheduledDate"].dt.strftime("%Y%m%d").astype(int)
    )

    # Validate appointment scheduling.
    assert (
        service_jobs["ScheduledDate"]
        >= service_jobs["RequestDate"]
    ).all(), "Scheduled date precedes request date."

    MAX_INITIAL_APPOINTMENT_DATE = (
        END_DATE + pd.Timedelta(days=7)
    )

    assert (
        service_jobs["ScheduledDate"]
        <= MAX_INITIAL_APPOINTMENT_DATE
    ).all(), "Scheduled date exceeds appointment horizon."

    assert service_jobs["ScheduledDateKey"].isin(
        dimensions["DimDate"]["DateKey"]
    ).all(), "Invalid scheduled date key."

    print("Service appointment scheduling validation passed.")

    # Assign preliminary service-job outcomes.
    # Scheduled jobs are limited to the reporting-period boundary.
    job_statuses = []

    pending_window_start = END_DATE - pd.Timedelta(days=14)

    for row in service_jobs.itertuples(index=False):
        scheduled_date = row.ScheduledDate

        # Appointments beyond the reporting period remain outstanding.
        if scheduled_date > END_DATE:
            job_statuses.append("Scheduled")
            continue

        if scheduled_date >= pending_window_start:
            statuses = [
                "Completed",
                "Cancelled",
                "No-Show",
                "Scheduled",
            ]

            probabilities = [0.70, 0.08, 0.05, 0.17]

        else:
            statuses = [
                "Completed",
                "Cancelled",
                "No-Show",
            ]

            probabilities = [0.87, 0.08, 0.05]

        status = rng.choice(
            statuses,
            p=probabilities,
        )

        job_statuses.append(status)

    service_jobs["JobStatus"] = job_statuses

    # Validate job-status assignments.
    valid_statuses = {
        "Completed",
        "Cancelled",
        "No-Show",
        "Scheduled",
    }

    assert set(service_jobs["JobStatus"]).issubset(
        valid_statuses
    ), "Invalid service-job status detected."

    pending_jobs = service_jobs[
        service_jobs["JobStatus"] == "Scheduled"
    ]

    assert (
        pending_jobs["ScheduledDate"] >= pending_window_start
    ).all(), "Scheduled jobs exist outside the pending window."

    print("\nService-job status distribution:")
    print(
        service_jobs["JobStatus"]
        .value_counts()
        .to_string()
    )

    print("Service-job status validation passed.")

    # Assign technicians while respecting daily service capacity.
    MAX_DAILY_SERVICE_HOURS = 8.0

    service_duration_lookup = services.set_index(
        "ServiceKey"
    )["EstimatedDurationHours"].to_dict()

    # Tracks completed-service hours per technician and date.
    technician_daily_hours = {}

    technician_assignments = []

    for row in service_jobs.itertuples(index=False):
        scheduled_date = row.ScheduledDate
        location_key = row.LocationKey
        job_status = row.JobStatus

        eligible_technicians = technicians[
            (technicians["HomeLocationKey"] == location_key)
            & (technicians["HireDate"] <= scheduled_date)
            & (
                technicians["TerminationDate"].isna()
                | (technicians["TerminationDate"] >= scheduled_date)
            )
        ]

        # Only assign technicians scheduled to work this weekday.
        eligible_technicians = eligible_technicians[
            eligible_technicians["EmployeeKey"].map(
                lambda employee_key: (
                    scheduled_date.weekday()
                    in technician_schedules[int(employee_key)]
                )
            )
        ]

        if eligible_technicians.empty:
            technician_assignments.append(pd.NA)
            continue

        # Non-completed jobs do not consume completed-service hours.
        if job_status != "Completed":
            technician = eligible_technicians.iloc[
                rng.integers(len(eligible_technicians))
            ]

            technician_assignments.append(
                int(technician["EmployeeKey"])
            )
            continue

        required_hours = float(
            service_duration_lookup[row.ServiceKey]
        )

        candidates = []

        for technician in eligible_technicians.itertuples(index=False):
            employee_key = int(technician.EmployeeKey)

            workload_key = (
                scheduled_date,
                employee_key,
            )

            current_hours = technician_daily_hours.get(
                workload_key,
                0.0,
            )

            remaining_hours = (
                MAX_DAILY_SERVICE_HOURS - current_hours
            )

            if remaining_hours >= required_hours:
                candidates.append(
                    (
                        remaining_hours,
                        employee_key,
                        workload_key,
                    )
                )

        if not candidates:
            technician_assignments.append(pd.NA)
            continue

        # Prefer the technician with the most remaining capacity.
        candidates.sort(reverse=True)

        _, employee_key, workload_key = candidates[0]

        technician_daily_hours[workload_key] = (
            technician_daily_hours.get(workload_key, 0.0)
            + required_hours
        )

        technician_assignments.append(employee_key)

    service_jobs["EmployeeKey"] = pd.array(
        technician_assignments,
        dtype="Int64",
    )

    assigned_count = service_jobs["EmployeeKey"].notna().sum()
    unassigned_count = service_jobs["EmployeeKey"].isna().sum()

    unassigned_completed = service_jobs[
        (service_jobs["JobStatus"] == "Completed")
        & (service_jobs["EmployeeKey"].isna())
    ]

    print("\nCapacity-aware technician assignment:")
    print(f"Assigned jobs: {assigned_count:,}")
    print(f"Unassigned jobs: {unassigned_count:,}")
    print(
        f"Completed jobs requiring reassessment: "
        f"{len(unassigned_completed):,}"
    )

    # Reschedule completed jobs that could not fit
    # within their original appointment dates.
    MAX_RESCHEDULE_DAYS = 7

    service_jobs["OriginalScheduledDate"] = (
        service_jobs["ScheduledDate"].copy()
    )

    rescheduled_count = 0
    unresolved_count = 0

    unassigned_indices = service_jobs.index[
        (service_jobs["JobStatus"] == "Completed")
        & (service_jobs["EmployeeKey"].isna())
    ]

    service_jobs["CapacityCancellation"] = False

    for job_index in unassigned_indices:
        job = service_jobs.loc[job_index]

        original_date = job["ScheduledDate"]
        location_key = int(job["LocationKey"])

        required_hours = float(
            service_duration_lookup[job["ServiceKey"]]
        )

        rescheduled = False

        for delay_days in range(1, MAX_RESCHEDULE_DAYS + 1):
            candidate_date = (
                original_date
                + pd.Timedelta(days=delay_days)
            )

            # Do not complete jobs beyond the reporting period.
            if candidate_date > END_DATE:
                break

            eligible_technicians = technicians[
                (technicians["HomeLocationKey"] == location_key)
                & (technicians["HireDate"] <= candidate_date)
                & (
                    technicians["TerminationDate"].isna()
                    | (
                        technicians["TerminationDate"]
                        >= candidate_date
                    )
                )
            ]

            # Rescheduled jobs must also respect technician days off.
            eligible_technicians = eligible_technicians[
                eligible_technicians["EmployeeKey"].map(
                    lambda employee_key: (
                        candidate_date.weekday()
                        in technician_schedules[int(employee_key)]
                    )
                )
            ]

            candidates = []

            for technician in eligible_technicians.itertuples(
                index=False
            ):
                employee_key = int(technician.EmployeeKey)

                workload_key = (
                    candidate_date,
                    employee_key,
                )

                current_hours = technician_daily_hours.get(
                    workload_key,
                    0.0,
                )

                remaining_hours = (
                    MAX_DAILY_SERVICE_HOURS - current_hours
                )

                if remaining_hours >= required_hours:
                    candidates.append(
                        (
                            remaining_hours,
                            employee_key,
                            workload_key,
                        )
                    )

            if not candidates:
                continue

            candidates.sort(reverse=True)

            _, employee_key, workload_key = candidates[0]

            technician_daily_hours[workload_key] = (
                technician_daily_hours.get(workload_key, 0.0)
                + required_hours
            )

            service_jobs.at[
                job_index, "ScheduledDate"
            ] = candidate_date

            service_jobs.at[
                job_index, "ScheduledDateKey"
            ] = int(candidate_date.strftime("%Y%m%d"))

            service_jobs.at[
                job_index, "EmployeeKey"
            ] = employee_key

            rescheduled_count += 1
            rescheduled = True
            break

        if not rescheduled:
            unresolved_count += 1

            # A service cannot be completed without an eligible technician.
            # Jobs exceeding available capacity become cancellations.
            service_jobs.at[job_index, "JobStatus"] = "Cancelled"
            service_jobs.at[job_index, "EmployeeKey"] = pd.NA
            service_jobs.at[job_index, "CapacityCancellation"] = True

    print("\nCapacity-aware rescheduling results:")
    print(f"Jobs rescheduled: {rescheduled_count:,}")
    print(
    f"Jobs cancelled due to staffing capacity: "
    f"{unresolved_count:,}"
)

    # Diagnose completed jobs that remain unassigned.
    unresolved_jobs = service_jobs[
        (service_jobs["JobStatus"] == "Completed")
        & (service_jobs["EmployeeKey"].isna())
    ].copy()

    if not unresolved_jobs.empty:
        unresolved_jobs = unresolved_jobs.merge(
            services[
                [
                    "ServiceKey",
                    "ServiceName",
                    "EstimatedDurationHours",
                ]
            ],
            on="ServiceKey",
            how="left",
            validate="many_to_one",
        )

        print("\nUnresolved completed-job details:")
        print(
            unresolved_jobs[
                [
                    "ServiceJobKey",
                    "LocationKey",
                    "ServiceName",
                    "OriginalScheduledDate",
                    "EstimatedDurationHours",
                ]
            ].to_string(index=False)
        )

        print("\nUnresolved jobs by location:")
        print(
            unresolved_jobs.groupby("LocationKey")
            .size()
            .to_string()
        )

    # Completed jobs must always have a valid technician assignment.
    assert unresolved_jobs.empty, (
        "Completed service jobs remain without assigned technicians."
    )

    # Validate that completed work occurs on scheduled workdays.
    completed_assignments = service_jobs.loc[
        service_jobs["JobStatus"] == "Completed",
        ["EmployeeKey", "ScheduledDate"],
    ].copy()

    scheduled_workday_valid = completed_assignments.apply(
        lambda row: (
            row["ScheduledDate"].weekday()
            in technician_schedules[int(row["EmployeeKey"])]
        ),
        axis=1,
    )

    assert scheduled_workday_valid.all(), (
        "Completed jobs assigned on technician days off."
    )

    print("Technician workday validation passed.")

    # Examine preliminary technician workload.
    completed_jobs = service_jobs[
        service_jobs["JobStatus"] == "Completed"
    ].copy()

    completed_jobs = completed_jobs.merge(
        services[
            ["ServiceKey", "EstimatedDurationHours"]
        ],
        on="ServiceKey",
        how="left",
        validate="many_to_one",
    )

    technician_workload = (
        completed_jobs.groupby(
            ["ScheduledDate", "EmployeeKey"],
            as_index=False,
        )["EstimatedDurationHours"]
        .sum()
    )

    print("\nPreliminary technician workload:")

    print(
        technician_workload["EstimatedDurationHours"]
        .describe()
        .round(2)
        .to_string()
    )

    overloaded_days = technician_workload[
        technician_workload["EstimatedDurationHours"] > 8
    ]

    print(
        f"\nTechnician-days exceeding 8 service hours: "
        f"{len(overloaded_days):,}"
    )

    print(
        "Maximum assigned service hours in one day: "
        f"{technician_workload['EstimatedDurationHours'].max():.2f}"
    )

    # Validate service scheduling and technician assignments.
    assert len(service_jobs) == len(job_records), (
        "Service requests were lost during scheduling."
    )

    assert service_jobs["ServiceJobKey"].is_unique, (
        "Duplicate service-job keys detected."
    )

    assert completed_jobs["EmployeeKey"].notna().all(), (
        "Completed service jobs have no assigned technician."
    )

    assert (
        completed_jobs["ScheduledDate"] <= END_DATE
    ).all(), (
        "Completed service jobs extend beyond the reporting period."
    )

    assert service_jobs["ScheduledDateKey"].isin(
        dimensions["DimDate"]["DateKey"]
    ).all(), (
        "Service appointments contain invalid date keys."
    )

    assert overloaded_days.empty, (
        "Technician daily service capacity exceeded."
    )

    assert (
        service_jobs["ScheduledDate"]
        >= service_jobs["OriginalScheduledDate"]
    ).all(), (
        "A rescheduled appointment precedes its original date."
    )

    # Verify assigned technicians were employed on appointment dates.
    assigned_jobs = service_jobs[
        service_jobs["EmployeeKey"].notna()
    ].copy()

    assigned_jobs = assigned_jobs.merge(
        technicians[
            [
                "EmployeeKey",
                "HomeLocationKey",
                "HireDate",
                "TerminationDate",
            ]
        ],
        on="EmployeeKey",
        how="left",
        validate="many_to_one",
    )

    assert (
        assigned_jobs["LocationKey"]
        == assigned_jobs["HomeLocationKey"]
    ).all(), (
        "Technician assigned outside their home location."
    )

    assert (
        assigned_jobs["ScheduledDate"]
        >= assigned_jobs["HireDate"]
    ).all(), (
        "Technician assigned before their hire date."
    )

    assert (
        assigned_jobs["TerminationDate"].isna()
        | (
            assigned_jobs["ScheduledDate"]
            <= assigned_jobs["TerminationDate"]
        )
    ).all(), (
        "Technician assigned after their termination date."
    )

    print("\nService scheduling integrity validation passed.")

    print(
        f"\nIndividual service requests generated: "
        f"{len(service_jobs):,}"
    )

    print("\nService requests by category:")

    category_summary = service_jobs.merge(
        services[["ServiceKey", "ServiceCategory"]],
        on="ServiceKey",
        how="left",
    )

    print(
        category_summary.groupby("ServiceCategory")
        .size()
        .sort_values(ascending=False)
        .to_string()
    )

    # Populate operational service-job fields.
    # Scheduled hours represent the appointment's estimated duration.
    duration_lookup = services.set_index(
        "ServiceKey"
    )["EstimatedDurationHours"].to_dict()

    service_jobs["ScheduledHours"] = (
        service_jobs["ServiceKey"]
        .map(duration_lookup)
        .astype(float)
    )

    # Completed jobs are modeled as same-day service completions.
    # Incomplete jobs have no completion date.
    completed_mask = service_jobs["JobStatus"] == "Completed"

    service_jobs["CompletedDateKey"] = pd.Series(
        pd.NA,
        index=service_jobs.index,
        dtype="Int64",
    )

    service_jobs.loc[
        completed_mask, "CompletedDateKey"
    ] = service_jobs.loc[
        completed_mask, "ScheduledDateKey"
    ].astype("Int64")

    # Validate operational fields.
    assert service_jobs["ScheduledHours"].notna().all(), (
        "Service jobs contain missing scheduled hours."
    )

    assert (service_jobs["ScheduledHours"] > 0).all(), (
        "Service jobs contain invalid scheduled hours."
    )

    assert service_jobs.loc[
        completed_mask, "CompletedDateKey"
    ].notna().all(), (
        "Completed jobs are missing completion dates."
    )

    assert service_jobs.loc[
        ~completed_mask, "CompletedDateKey"
    ].isna().all(), (
        "Incomplete jobs contain completion dates."
    )

    print("\nService operational fields validated.")
    print(
        f"Total scheduled service hours: "
        f"{service_jobs['ScheduledHours'].sum():,.2f}"
    )

    # Generate actual service hours for completed jobs.
    # Incomplete jobs do not consume completed-job labor hours.
    service_jobs["ActualServiceHours"] = 0.0

    completed_indices = service_jobs.index[completed_mask]

    # Introduce realistic variation around estimated durations.
    duration_factors = rng.uniform(
        0.85,
        1.15,
        size=len(completed_indices),
    )

    service_jobs.loc[
        completed_indices, "ActualServiceHours"
    ] = (
        service_jobs.loc[
            completed_indices, "ScheduledHours"
        ].to_numpy()
        * duration_factors
    )

    # Calculate technician workload using actual service hours.
    # ScheduledDate represents the completion date for completed jobs.
    daily_actual_hours = (
        service_jobs.loc[completed_mask]
        .groupby(["ScheduledDate", "EmployeeKey"])[
            "ActualServiceHours"
        ]
        .transform("sum")
    )

    # Scale overloaded technician-days to the eight-hour limit.
    capacity_factors = np.minimum(
        1.0,
        8.0 / daily_actual_hours.to_numpy(),
    )

    # Quantify how often capacity normalization is required.
    adjusted_job_count = int(
        (capacity_factors < 1.0).sum()
    )

    adjusted_technician_days = (
        service_jobs.loc[completed_mask]
        .assign(RequiredAdjustment=capacity_factors < 1.0)
        .groupby(["ScheduledDate", "EmployeeKey"])[
            "RequiredAdjustment"
        ]
        .any()
        .sum()
    )

    print("\nActual service capacity adjustments:")
    print(f"Jobs adjusted: {adjusted_job_count:,}")
    print(
        f"Technician-days requiring adjustment: "
        f"{adjusted_technician_days:,}"
    )

    adjusted_hours = (
        service_jobs.loc[
            completed_mask, "ActualServiceHours"
        ].to_numpy()
        * capacity_factors
    )

    # Round down to hundredths to avoid exceeding capacity
    # because of rounding.
    service_jobs.loc[
        completed_mask, "ActualServiceHours"
    ] = (
        np.floor(adjusted_hours * 100 + 1e-9) / 100
    )

    # Validate generated service hours.
    assert (
        service_jobs.loc[
            completed_mask, "ActualServiceHours"
        ] > 0
    ).all(), (
        "Completed jobs contain invalid actual service hours."
    )

    assert (
        service_jobs.loc[
            ~completed_mask, "ActualServiceHours"
        ] == 0
    ).all(), (
        "Incomplete jobs contain actual service hours."
    )

    actual_workload = (
        service_jobs.loc[completed_mask]
        .groupby(["ScheduledDate", "EmployeeKey"])[
            "ActualServiceHours"
        ]
        .sum()
    )

    assert (actual_workload <= 8.0 + 1e-9).all(), (
        "Actual technician workload exceeds daily capacity."
    )

    print("\nActual service hours validation passed.")

    print(
        f"Total actual service hours: "
        f"{service_jobs['ActualServiceHours'].sum():,.2f}"
    )

    print(
        f"Maximum actual technician workload: "
        f"{actual_workload.max():.2f} hours"
    )

    print(
        f"Technician-days exceeding actual capacity: "
        f"{(actual_workload > 8.0).sum():,}"
    )

    # Generate service financial fields.
    # StandardServiceFee is the published catalog price.
    fee_lookup = services.set_index(
        "ServiceKey"
    )["StandardRate"].to_dict()

    service_jobs["StandardServiceFee"] = (
        service_jobs["ServiceKey"]
        .map(fee_lookup)
        .astype(float)
        .round(2)
    )

    service_jobs["DiscountAmount"] = 0.0
    service_jobs["ServiceRevenue"] = 0.0
    service_jobs["PartsCost"] = 0.0

    # Apply discounts to completed jobs only.
    discount_rates = rng.choice(
        [0.00, 0.05, 0.10, 0.15],
        size=int(completed_mask.sum()),
        p=[0.75, 0.10, 0.10, 0.05],
    )

    completed_fees = service_jobs.loc[
        completed_mask, "StandardServiceFee"
    ].to_numpy()

    discounts = np.round(
        completed_fees * discount_rates,
        2,
    )

    service_jobs.loc[
        completed_mask, "DiscountAmount"
    ] = discounts

    service_jobs.loc[
        completed_mask, "ServiceRevenue"
    ] = np.round(
        completed_fees - discounts,
        2,
    )

    # Parts consumption varies by service category.
    parts_rules = {
        "Computer Repair": (0.45, 10, 85),
        "Device Setup": (0.10, 5, 20),
        "Network Installation": (0.35, 15, 100),
        "Smart Home Installation": (0.40, 10, 80),
        "Technical Support": (0.05, 5, 15),
        "Troubleshooting": (0.10, 5, 25),
    }

    category_lookup = services.set_index(
        "ServiceKey"
    )["ServiceCategory"].to_dict()

    service_jobs["ServiceCategory"] = (
        service_jobs["ServiceKey"].map(category_lookup)
    )

    for category, (probability, minimum, maximum) in parts_rules.items():
        category_mask = (
            completed_mask
            & (service_jobs["ServiceCategory"] == category)
        )

        category_indices = service_jobs.index[category_mask]
        count = len(category_indices)

        if count == 0:
            continue

        uses_parts = rng.random(count) < probability

        generated_costs = np.round(
            rng.uniform(minimum, maximum, size=count),
            2,
        )

        service_jobs.loc[
            category_indices, "PartsCost"
        ] = np.where(uses_parts, generated_costs, 0.0)

    # Keep category as a dimension attribute, not a fact column.
    service_jobs.drop(
        columns=["ServiceCategory"],
        inplace=True,
    )

    # Validate financial integrity.
    assert service_jobs["StandardServiceFee"].notna().all(), (
        "Missing standard service fees."
    )

    assert (
        service_jobs["StandardServiceFee"] > 0
    ).all(), "Invalid standard service fees."

    assert (
        service_jobs["DiscountAmount"]
        <= service_jobs["StandardServiceFee"]
    ).all(), "Discount exceeds standard service fee."

    assert (
        service_jobs["ServiceRevenue"] >= 0
    ).all(), "Negative service revenue detected."

    assert (
        service_jobs["PartsCost"] >= 0
    ).all(), "Negative parts cost detected."

    assert (
        service_jobs.loc[
            ~completed_mask,
            ["DiscountAmount", "ServiceRevenue", "PartsCost"],
        ] == 0
    ).all().all(), (
        "Incomplete jobs contain recognized financial activity."
    )

    expected_revenue = (
        service_jobs.loc[
            completed_mask, "StandardServiceFee"
        ]
        - service_jobs.loc[
            completed_mask, "DiscountAmount"
        ]
    )

    assert np.allclose(
        service_jobs.loc[
            completed_mask, "ServiceRevenue"
        ],
        expected_revenue,
    ), "Service revenue reconciliation failed."

    print("\nService financial validation passed.")

    print(
        f"Gross completed service fees: "
        f"${completed_fees.sum():,.2f}"
    )

    print(
        f"Total service discounts: "
        f"${service_jobs['DiscountAmount'].sum():,.2f}"
    )

    print(
        f"Net service revenue: "
        f"${service_jobs['ServiceRevenue'].sum():,.2f}"
    )

    print(
        f"Total service parts cost: "
        f"${service_jobs['PartsCost'].sum():,.2f}"
    )

    # Assign cancellation reasons only to cancelled service jobs.
    cancellation_reasons = [
        "Customer Request",
        "Scheduling Conflict",
        "Price Concern",
        "Service No Longer Needed",
        "Unable to Contact Customer",
        "Other",
    ]

    cancellation_probabilities = [
        0.30,
        0.20,
        0.15,
        0.20,
        0.10,
        0.05,
    ]

    service_jobs["CancellationReason"] = pd.Series(
        pd.NA,
        index=service_jobs.index,
        dtype="string",
    )

    cancelled_mask = service_jobs["JobStatus"] == "Cancelled"

    # Distinguish customer cancellations from staffing failures.
    capacity_cancelled = (
        cancelled_mask
        & service_jobs["CapacityCancellation"]
    )

    ordinary_cancelled = (
        cancelled_mask
        & ~service_jobs["CapacityCancellation"]
    )

    service_jobs.loc[
        ordinary_cancelled, "CancellationReason"
    ] = rng.choice(
        cancellation_reasons,
        size=int(ordinary_cancelled.sum()),
        p=cancellation_probabilities,
    )

    service_jobs.loc[
        capacity_cancelled, "CancellationReason"
    ] = "Staffing Capacity"

    # Related retail transactions are optional.
    # Leave them unassigned until cross-table matching is implemented.
    service_jobs["RelatedTransactionID"] = pd.Series(
        pd.NA,
        index=service_jobs.index,
        dtype="string",
    )

    # Validate cancellation data.
    assert service_jobs.loc[
        cancelled_mask, "CancellationReason"
    ].notna().all(), (
        "Cancelled jobs are missing cancellation reasons."
    )

    assert service_jobs.loc[
        ~cancelled_mask, "CancellationReason"
    ].isna().all(), (
        "Non-cancelled jobs contain cancellation reasons."
    )

    assert service_jobs["RelatedTransactionID"].isna().all(), (
        "Unexpected related retail transactions detected."
    )

    print("\nCancellation and transaction-link validation passed.")

    print("\nCancellation reasons:")
    print(
        service_jobs.loc[
            cancelled_mask, "CancellationReason"
        ]
        .value_counts()
        .to_string()
    )

    # Select the documented analytical schema.
    service_job_columns = [
        "ServiceJobKey",
        "JobReference",
        "CustomerKey",
        "LocationKey",
        "ServiceKey",
        "EmployeeKey",
        "ScheduledDateKey",
        "CompletedDateKey",
        "JobStatus",
        "ScheduledHours",
        "ActualServiceHours",
        "StandardServiceFee",
        "DiscountAmount",
        "ServiceRevenue",
        "PartsCost",
        "CancellationReason",
        "RelatedTransactionID",
    ]

    # Ensure every required field exists.
    missing_columns = set(service_job_columns) - set(
        service_jobs.columns
    )

    assert not missing_columns, (
        f"Missing FactServiceJobs columns: {missing_columns}"
    )

    service_jobs = service_jobs[service_job_columns].copy()

    assert len(service_jobs) == len(job_records), (
        "Service-job rows were lost during schema selection."
    )

    assert service_jobs["ServiceJobKey"].is_unique, (
        "Duplicate service-job keys detected."
    )

    print("\nFinal FactServiceJobs schema validation passed.")
    print(f"Rows: {len(service_jobs):,}")
    print(f"Columns: {len(service_jobs.columns)}")

    return service_jobs

def generate_labor(
    dimensions: dict[str, pd.DataFrame],
    service_jobs: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """
    Generate Northstar employee labor records.

    Labor records will reconcile with completed service jobs
    and provide the authoritative source for payroll costs.
    """

    employees = dimensions["DimEmployee"].copy()

    employees["HireDate"] = pd.to_datetime(
        employees["HireDate"]
    )

    employees["TerminationDate"] = pd.to_datetime(
        employees["TerminationDate"]
    )

    # Start with actual service work already performed.
    completed_jobs = service_jobs.loc[
        service_jobs["JobStatus"] == "Completed"
    ].copy()

    completed_jobs["WorkDate"] = pd.to_datetime(
        completed_jobs["CompletedDateKey"].astype(str),
        format="%Y%m%d",
    )

    # Aggregate service hours by technician, date, and location.
    service_workload = (
        completed_jobs.groupby(
            ["EmployeeKey", "WorkDate", "LocationKey"],
            as_index=False,
        )["ActualServiceHours"]
        .sum()
        .rename(
            columns={
                "ActualServiceHours": "RequiredServiceHours"
            }
        )
    )

    print("\nFactLabor generation initialized.")

    print(
        f"Completed service hours: "
        f"{completed_jobs['ActualServiceHours'].sum():,.2f}"
    )

    print(
        f"Labor assignments requiring coverage: "
        f"{len(service_workload):,}"
    )

    # Validate that all service assignments have valid employees.
    assert service_workload["EmployeeKey"].isin(
        employees["EmployeeKey"]
    ).all(), (
        "Service work references an invalid employee."
    )

    assert (
        service_workload["RequiredServiceHours"] > 0
    ).all(), (
        "Service work contains invalid required hours."
    )

    assert abs(
        service_workload["RequiredServiceHours"].sum()
        - completed_jobs["ActualServiceHours"].sum()
    ) < 0.01, (
        "Service labor hours do not reconcile."
    )

    print("Service workload aggregation validated.")

    # Create recurring employee work schedules.
    # Service technicians retain the schedules used for job assignment.
    technician_schedules = technician_workdays(
        employees[employees["Department"] == "Service"]
    )

    employee_schedules = {}

    for department, group in employees.groupby("Department"):
        group = group.sort_values("EmployeeKey")

        for position, employee in enumerate(
            group.itertuples(index=False)
        ):
            employee_key = int(employee.EmployeeKey)

            if department == "Service":
                employee_schedules[employee_key] = (
                    technician_schedules[employee_key]
                )
                continue

            if employee.EmploymentType == "Part-Time":
                if department == "Retail":
                    patterns = [
                        {0, 2, 5},
                        {1, 4, 6},
                        {2, 4, 5},
                    ]
                else:
                    patterns = [
                        {0, 2, 4},
                        {1, 3, 4},
                    ]
            else:
                if department == "Retail":
                    starts = [0, 2, 4, 1, 3]
                    start = starts[position % len(starts)]

                    employee_schedules[employee_key] = {
                        (start + offset) % 7
                        for offset in range(5)
                    }
                    continue

                patterns = [{0, 1, 2, 3, 4}]

            employee_schedules[employee_key] = patterns[
                position % len(patterns)
            ]

    # Generate workdays within each employee's employment period.
    labor_records = []

    for employee in employees.itertuples(index=False):
        employee_key = int(employee.EmployeeKey)

        first_day = max(employee.HireDate, START_DATE)

        last_day = (
            min(employee.TerminationDate, END_DATE)
            if pd.notna(employee.TerminationDate)
            else END_DATE
        )

        if first_day > last_day:
            continue

        for work_date in pd.date_range(
            first_day,
            last_day,
            freq="D",
        ):
            if (
                work_date.weekday()
                not in employee_schedules[employee_key]
            ):
                continue

            labor_records.append(
                {
                    "EmployeeKey": employee_key,
                    "WorkDate": work_date,
                    "LocationKey": int(
                        employee.HomeLocationKey
                    ),
                    "Department": employee.Department,
                    "EmploymentType": employee.EmploymentType,
                    "StandardHourlyRate": float(
                        employee.StandardHourlyRate
                    ),
                }
            )

    labor_calendar = pd.DataFrame(labor_records)

    # Attach completed service hours to employee workdays.
    labor_calendar = labor_calendar.merge(
        service_workload,
        on=["EmployeeKey", "WorkDate", "LocationKey"],
        how="left",
        validate="one_to_one",
    )

    labor_calendar["RequiredServiceHours"] = (
        labor_calendar["RequiredServiceHours"].fillna(0.0)
    )

    # Verify all completed service assignments were preserved.
    assert abs(
        labor_calendar["RequiredServiceHours"].sum()
        - service_workload["RequiredServiceHours"].sum()
    ) < 0.01, (
        "Employee calendar failed to preserve service hours."
    )

    assert not labor_calendar.duplicated(
        ["EmployeeKey", "WorkDate", "LocationKey"]
    ).any(), (
        "Duplicate employee workday records detected."
    )

    print("\nFull employee labor calendar generated.")

    print(
        f"Employee workday records: "
        f"{len(labor_calendar):,}"
    )

    print("\nWorkdays by department:")
    print(
        labor_calendar.groupby("Department")
        .size()
        .to_string()
    )

    print(
        f"\nService hours preserved: "
        f"{labor_calendar['RequiredServiceHours'].sum():,.2f}"
    )

    # Generate initial employee shift and paid-hour fields.
    # Full-time employees work eight-hour shifts.
    # Part-time employees work four-hour shifts.
    shift_hours = {
        "Full-Time": 8.0,
        "Part-Time": 4.0,
    }

    labor_calendar["ScheduledHours"] = (
        labor_calendar["EmploymentType"]
        .map(shift_hours)
        .astype(float)
    )

    # Initial model: paid hours equal scheduled hours.
    # Overtime will be introduced after baseline validation.
    labor_calendar["RegularHours"] = (
        labor_calendar["ScheduledHours"].copy()
    )

    labor_calendar["OvertimeHours"] = 0.0

    # Completed service hours are billable technician hours.
    labor_calendar["BillableHours"] = (
        labor_calendar["RequiredServiceHours"].round(2)
    )

    # Nonbillable hours include retail work, administration,
    # technician preparation, documentation, and idle time.
    labor_calendar["NonBillableHours"] = (
        labor_calendar["RegularHours"]
        + labor_calendar["OvertimeHours"]
        - labor_calendar["BillableHours"]
    ).round(2)

    # Initial assumption: all paid hours are available for
    # productive activity, including nonbillable duties.
    labor_calendar["AvailableProductiveHours"] = (
        labor_calendar["RegularHours"]
        + labor_calendar["OvertimeHours"]
    )

    # Add the date dimension foreign key.
    labor_calendar["DateKey"] = (
        labor_calendar["WorkDate"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    # Validate employee work hours.
    assert labor_calendar["ScheduledHours"].notna().all(), (
        "Missing scheduled shift hours."
    )

    assert (
        labor_calendar["BillableHours"]
        <= labor_calendar["AvailableProductiveHours"] + 1e-9
    ).all(), (
        "Billable service hours exceed available labor hours."
    )

    assert (
        labor_calendar["NonBillableHours"] >= -1e-9
    ).all(), (
        "Negative nonbillable labor hours detected."
    )

    total_worked = (
        labor_calendar["RegularHours"]
        + labor_calendar["OvertimeHours"]
    )

    allocated_hours = (
        labor_calendar["BillableHours"]
        + labor_calendar["NonBillableHours"]
    )

    assert np.allclose(
        total_worked,
        allocated_hours,
        atol=1e-9,
    ), (
        "Paid labor hours do not reconcile."
    )

    assert labor_calendar["DateKey"].isin(
        dimensions["DimDate"]["DateKey"]
    ).all(), (
        "Labor records contain invalid date keys."
    )

    print("\nEmployee paid-hour validation passed.")

    print(
        f"Total paid hours: "
        f"{total_worked.sum():,.2f}"
    )

    print(
        f"Billable service hours: "
        f"{labor_calendar['BillableHours'].sum():,.2f}"
    )

    print(
        f"Nonbillable hours: "
        f"{labor_calendar['NonBillableHours'].sum():,.2f}"
    )

    print(
        f"Overall service-billable utilization: "
        f"{labor_calendar['BillableHours'].sum() / total_worked.sum():.1%}"
    )

    # Generate historical wage and payroll fields.
    # Initial model assumes constant hourly rates during employment.
    labor_calendar["BaseHourlyRate"] = (
        labor_calendar["StandardHourlyRate"]
        .round(2)
    )

    labor_calendar["OvertimeMultiplier"] = 1.50
    labor_calendar["EmployerBurdenRate"] = 0.25

    gross_wages = []
    employer_burden = []
    fully_loaded_costs = []

    for row in labor_calendar.itertuples(index=False):
        regular_wages = (
            Decimal(str(row.RegularHours))
            * Decimal(str(row.BaseHourlyRate))
        )

        overtime_wages = (
            Decimal(str(row.OvertimeHours))
            * Decimal(str(row.BaseHourlyRate))
            * Decimal(str(row.OvertimeMultiplier))
        )

        wages = money(regular_wages + overtime_wages)

        burden = money(
            wages * Decimal(str(row.EmployerBurdenRate))
        )

        fully_loaded = money(wages + burden)

        gross_wages.append(float(wages))
        employer_burden.append(float(burden))
        fully_loaded_costs.append(float(fully_loaded))

    labor_calendar["GrossWages"] = gross_wages
    labor_calendar["EmployerBurdenCost"] = employer_burden
    labor_calendar["FullyLoadedLaborCost"] = fully_loaded_costs

    # Direct labor costs will be determined from job allocations.
    labor_calendar["DirectServiceLaborCost"] = 0.0

    labor_calendar["NonDirectLaborCost"] = (
        labor_calendar["FullyLoadedLaborCost"].copy()
    )

    # Validate payroll calculations.
    assert (
        labor_calendar["GrossWages"] >= 0
    ).all(), "Negative gross wages detected."

    assert (
        labor_calendar["EmployerBurdenCost"] >= 0
    ).all(), "Negative employer burden detected."

    assert np.allclose(
        labor_calendar["FullyLoadedLaborCost"],
        labor_calendar["GrossWages"]
        + labor_calendar["EmployerBurdenCost"],
        atol=0.001,
    ), "Fully loaded labor costs do not reconcile."

    print("\nPayroll cost validation passed.")

    print(
        f"Gross wages: "
        f"${labor_calendar['GrossWages'].sum():,.2f}"
    )

    print(
        f"Employer burden: "
        f"${labor_calendar['EmployerBurdenCost'].sum():,.2f}"
    )

    print(
        f"Fully loaded labor cost: "
        f"${labor_calendar['FullyLoadedLaborCost'].sum():,.2f}"
    )

    # Calculate technician-specific service utilization.
    service_labor = labor_calendar[
        labor_calendar["Department"] == "Service"
    ].copy()

    technician_paid_hours = (
        service_labor["RegularHours"]
        + service_labor["OvertimeHours"]
    ).sum()

    technician_billable_hours = (
        service_labor["BillableHours"].sum()
    )

    technician_utilization = (
        technician_billable_hours / technician_paid_hours
        if technician_paid_hours > 0
        else 0.0
    )

    print("\nTechnician labor utilization:")
    print(f"Technician paid hours: {technician_paid_hours:,.2f}")
    print(f"Technician billable hours: {technician_billable_hours:,.2f}")
    print(f"Technician utilization: {technician_utilization:.1%}")

    # Assign stable, unique labor record identifiers.
    labor_calendar = labor_calendar.sort_values(
        ["WorkDate", "EmployeeKey", "LocationKey"]
    ).reset_index(drop=True)

    labor_calendar.insert(
        0,
        "LaborKey",
        np.arange(1, len(labor_calendar) + 1),
    )

    # Validate labor record grain and identifiers.
    assert labor_calendar["LaborKey"].is_unique, (
        "Duplicate labor keys detected."
    )

    assert not labor_calendar.duplicated(
        ["EmployeeKey", "DateKey", "LocationKey"]
    ).any(), (
        "Duplicate employee/date/location labor records."
    )

    assert labor_calendar["LaborKey"].notna().all(), (
        "Missing labor record identifiers."
    )

    print("\nLabor record identifiers validated.")
    print(f"Unique LaborKeys: {labor_calendar['LaborKey'].nunique():,}")

    return labor_calendar

def generate_job_labor_allocations(
    service_jobs: pd.DataFrame,
    labor: pd.DataFrame,
) -> pd.DataFrame:
    """
    Allocate completed service hours to their source labor records.

    FactLabor remains the authoritative source of payroll costs.
    Allocations support job-level profitability without
    introducing additional payroll expense.
    """

    completed = service_jobs.loc[
        service_jobs["JobStatus"] == "Completed"
    ].copy()

    # Match completed jobs to employee/date/location labor records.
    labor_reference = labor[
        [
            "LaborKey",
            "EmployeeKey",
            "DateKey",
            "LocationKey",
            "BaseHourlyRate",
            "OvertimeMultiplier",
            "EmployerBurdenRate",
            "BillableHours",
        ]
    ].copy()

    allocations = completed.merge(
        labor_reference,
        left_on=[
            "EmployeeKey",
            "CompletedDateKey",
            "LocationKey",
        ],
        right_on=[
            "EmployeeKey",
            "DateKey",
            "LocationKey",
        ],
        how="left",
        validate="many_to_one",
    )

    assert allocations["LaborKey"].notna().all(), (
        "Completed jobs could not be matched to labor records."
    )

    assert len(allocations) == len(completed), (
        "Completed jobs were lost or duplicated during allocation."
    )

    # The initial model has no overtime.
    allocations["AllocatedRegularHours"] = (
        allocations["ActualServiceHours"].round(2)
    )

    allocations["AllocatedOvertimeHours"] = 0.0

    allocations["AllocatedHours"] = (
        allocations["AllocatedRegularHours"]
        + allocations["AllocatedOvertimeHours"]
    )

    allocations = allocations.sort_values(
        ["LaborKey", "ServiceJobKey"]
    ).reset_index(drop=True)

    allocations.insert(
        0,
        "JobLaborAllocationKey",
        np.arange(1, len(allocations) + 1),
    )

    print("\nJob labor allocation initialized.")

    print(
        f"Completed jobs matched: "
        f"{len(allocations):,}"
    )

    print(
        f"Allocated service hours: "
        f"{allocations['AllocatedHours'].sum():,.2f}"
    )

    # Validate allocated hours by originating labor record.
    allocated_by_labor = (
        allocations.groupby("LaborKey")["AllocatedHours"]
        .sum()
    )

    expected_by_labor = labor.set_index(
        "LaborKey"
    )["BillableHours"]

    reconciled = expected_by_labor.subtract(
        allocated_by_labor,
        fill_value=0,
    )

    assert (reconciled.abs() < 0.01).all(), (
        "Allocated service hours do not reconcile to FactLabor."
    )

    assert not allocations.duplicated(
        ["LaborKey", "ServiceJobKey"]
    ).any(), (
        "Duplicate labor-to-job allocations detected."
    )

    print("Job labor hour reconciliation passed.")

    # Calculate fully loaded direct labor costs.
    # Decimal arithmetic avoids binary floating-point rounding errors.
    allocations["AllocatedDirectLaborCost"] = [
        float(
            money(
                (
                    Decimal(str(row.AllocatedRegularHours))
                    * Decimal(str(row.BaseHourlyRate))
                    + Decimal(str(row.AllocatedOvertimeHours))
                    * Decimal(str(row.BaseHourlyRate))
                    * Decimal(str(row.OvertimeMultiplier))
                )
                * (
                    Decimal("1")
                    + Decimal(str(row.EmployerBurdenRate))
                )
            )
        )
        for row in allocations.itertuples(index=False)
    ]

    # The authoritative direct labor cost is the sum of
    # allocations, not a second independently generated expense.
    direct_costs = (
        allocations.groupby("LaborKey")[
            "AllocatedDirectLaborCost"
        ]
        .sum()
    )

    print("\nDirect labor cost allocation:")

    print(
        f"Allocated direct labor cost: "
        f"${allocations['AllocatedDirectLaborCost'].sum():,.2f}"
    )

    print(
        f"Labor records receiving allocations: "
        f"{len(direct_costs):,}"
    )

    assert (
        allocations["AllocatedDirectLaborCost"] >= 0
    ).all(), (
        "Negative allocated direct labor cost detected."
    )

    assert allocations["JobLaborAllocationKey"].is_unique, (
        "Duplicate job-labor allocation keys detected."
    )

    print("Job labor cost generation validated.")

    return allocations

def generate_expenses(
    dimensions: dict[str, pd.DataFrame],
    sales: pd.DataFrame,
    service_jobs: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Generate Northstar non-payroll operating expenses."""

    categories = dimensions["DimExpenseCategory"]
    locations = dimensions["DimLocation"]

    category_lookup = categories.set_index(
        "ExpenseCategory"
    )["ExpenseCategoryKey"].to_dict()

    location_keys = sorted(
        locations["LocationKey"].astype(int).tolist()
    )

    # Shared company expenses are allocated across locations.
    allocation_weights = {
        1: Decimal("0.40"),
        2: Decimal("0.30"),
        3: Decimal("0.30"),
    }

    assert set(location_keys) == set(allocation_weights), (
        "Missing shared-expense allocation weights."
    )

    records = []
    expense_key = 1
    reference_number = 1

    months = pd.date_range(
        START_DATE,
        END_DATE,
        freq="MS",
    )

    def add_expense(
        date,
        category,
        amount,
        description,
        recurring,
        location_key=None,
        vendor="NS-VENDOR-001",
    ):
        nonlocal expense_key, reference_number

        reference = f"NS-EXP-{reference_number:07d}"
        reference_number += 1

        amount = money(amount)

        if amount == 0:
            return

        if location_key is not None:
            allocations = {
                int(location_key): amount
            }
            method = "Direct"

        else:
            # Allocate to all locations, assigning any rounding
            # remainder to the final location.
            allocations = {}
            remaining = amount

            for key in location_keys[:-1]:
                allocated = money(
                    amount * allocation_weights[key]
                )
                allocations[key] = allocated
                remaining -= allocated

            allocations[location_keys[-1]] = money(remaining)
            method = "Allocated"

            assert sum(
                allocations.values(),
                Decimal("0"),
            ) == amount

        for key, allocated_amount in allocations.items():
            if allocated_amount == 0:
                continue

            records.append({
                "ExpenseKey": expense_key,
                "ExpenseReference": reference,
                "DateKey": int(date.strftime("%Y%m%d")),
                "LocationKey": key,
                "ExpenseCategoryKey": int(
                    category_lookup[category]
                ),
                "VendorCode": vendor,
                "ExpenseDescription": description,
                "ExpenseAmount": float(allocated_amount),
                "IsRecurring": bool(recurring),
                "AllocationMethod": method,
            })

            expense_key += 1

    # Monthly expenses.
    for month in months:
        # Use month-end as the accounting recognition date.
        date = month + pd.offsets.MonthEnd(0)

        for location_key in location_keys:
            # Location-specific monthly rent.
            rent = {
                1: 4500,
                2: 3200,
                3: 3900,
            }[location_key]

            add_expense(
                date,
                "Rent",
                rent,
                "Monthly facility lease",
                True,
                location_key,
                "NS-VENDOR-RENT",
            )

            # Utilities fluctuate with seasonal demand.
            seasonal_factor = (
                1.15 if month.month in [6, 7, 8, 9]
                else 1.0
            )

            utilities = money(
                Decimal(str(rng.uniform(450, 900)))
                * Decimal(str(seasonal_factor))
            )

            add_expense(
                date,
                "Utilities",
                utilities,
                "Monthly facility utilities",
                True,
                location_key,
                "NS-VENDOR-UTILITY",
            )

            # Periodic administrative supplies.
            if rng.random() < 0.65:
                add_expense(
                    date,
                    "Administrative Supplies",
                    rng.uniform(75, 350),
                    "Administrative and office supplies",
                    False,
                    location_key,
                    "NS-VENDOR-SUPPLIES",
                )

            # Equipment maintenance.
            if rng.random() < 0.30:
                add_expense(
                    date,
                    "Equipment Maintenance",
                    rng.uniform(150, 1200),
                    "Operational equipment maintenance",
                    False,
                    location_key,
                    "NS-VENDOR-MAINT",
                )

            # Other miscellaneous operating expenses.
            if rng.random() < 0.45:
                add_expense(
                    date,
                    "Other Operating Expenses",
                    rng.uniform(100, 700),
                    "Miscellaneous location operating expense",
                    False,
                    location_key,
                    "NS-VENDOR-OTHER",
                )

        # Shared company expenses.
        add_expense(
            date,
            "Insurance",
            1800,
            "Monthly business insurance",
            True,
            vendor="NS-VENDOR-INS",
        )

        add_expense(
            date,
            "Software Subscriptions",
            950,
            "Monthly business software subscriptions",
            True,
            vendor="NS-VENDOR-SOFTWARE",
        )

        # Marketing varies by campaign and season.
        marketing = money(
            rng.uniform(1800, 4200)
            * (1.30 if month.month in [11, 12] else 1.0)
        )

        add_expense(
            date,
            "Marketing",
            marketing,
            "Company-wide marketing campaign",
            False,
            vendor="NS-VENDOR-MARKETING",
        )

    # Generate monthly merchant processing fees.
    # Fees are based on recognized retail and service revenue.
    processing_rate = Decimal("0.025")

    retail_activity = sales.copy()

    retail_activity["Month"] = (
        pd.to_datetime(
            retail_activity["DateKey"].astype(str),
            format="%Y%m%d",
        )
        .dt.to_period("M")
    )

    retail_monthly = (
        retail_activity.groupby(
            ["Month", "LocationKey"]
        )["NetRevenue"]
        .sum()
    )

    completed_services = service_jobs[
        service_jobs["JobStatus"] == "Completed"
    ].copy()

    completed_services["Month"] = (
        pd.to_datetime(
            completed_services["CompletedDateKey"]
            .astype(int)
            .astype(str),
            format="%Y%m%d",
        )
        .dt.to_period("M")
    )

    service_monthly = (
        completed_services.groupby(
            ["Month", "LocationKey"]
        )["ServiceRevenue"]
        .sum()
    )

    for month in months:
        period = month.to_period("M")
        recognition_date = month + pd.offsets.MonthEnd(0)

        for location_key in location_keys:
            retail_revenue = retail_monthly.get(
                (period, location_key),
                0.0,
            )

            service_revenue = service_monthly.get(
                (period, location_key),
                0.0,
            )

            combined_revenue = money(
                Decimal(str(retail_revenue))
                + Decimal(str(service_revenue))
            )

            processing_fee = money(
                combined_revenue * processing_rate
            )

            if processing_fee <= 0:
                continue

            add_expense(
                recognition_date,
                "Merchant Processing Fees",
                processing_fee,
                "Monthly payment processing fees",
                True,
                location_key,
                "NS-VENDOR-PAYMENTS",
            )

    expenses = pd.DataFrame(records)

    print("\nFactExpenses generation initialized.")
    print(f"Expense records generated: {len(expenses):,}")

    assert expenses["ExpenseKey"].is_unique
    assert expenses["DateKey"].isin(
        dimensions["DimDate"]["DateKey"]
    ).all()

    assert expenses["LocationKey"].isin(
        locations["LocationKey"]
    ).all()

    assert expenses["ExpenseCategoryKey"].isin(
        categories["ExpenseCategoryKey"]
    ).all()

    assert (expenses["ExpenseAmount"] != 0).all()

    print("Expense primary-key and foreign-key validation passed.")

    # Verify all documented expense categories are represented.
    expected_categories = set(
        categories["ExpenseCategoryKey"]
    )

    actual_categories = set(
        expenses["ExpenseCategoryKey"]
    )

    assert expected_categories == actual_categories, (
        "One or more expense categories are missing."
    )

    # Shared expenses must reconcile to their original amount.
    allocated = expenses[
        expenses["AllocationMethod"] == "Allocated"
    ]

    allocation_counts = (
        allocated.groupby("ExpenseReference")[
            "LocationKey"
        ]
        .nunique()
    )

    assert (
        allocation_counts == len(location_keys)
    ).all(), (
        "Shared expenses are missing location allocations."
    )

    assert not expenses.duplicated(
        ["ExpenseReference", "LocationKey"]
    ).any(), (
        "Duplicate expense reference/location combinations."
    )

    print("\nAll nine expense categories validated.")

    print("\nExpenses by category:")

    summary = expenses.merge(
        categories[
            ["ExpenseCategoryKey", "ExpenseCategory"]
        ],
        on="ExpenseCategoryKey",
        validate="many_to_one",
    )

    print(
        summary.groupby("ExpenseCategory")[
            "ExpenseAmount"
        ]
        .agg(["count", "sum"])
        .round(2)
        .to_string()
    )

    print(
        f"\nTotal non-payroll operating expenses: "
        f"${expenses['ExpenseAmount'].sum():,.2f}"
    )

    # Final FactExpenses schema.
    expense_columns = [
        "ExpenseKey",
        "ExpenseReference",
        "DateKey",
        "LocationKey",
        "ExpenseCategoryKey",
        "VendorCode",
        "ExpenseDescription",
        "ExpenseAmount",
        "IsRecurring",
        "AllocationMethod",
    ]

    assert len(expenses) == 537
    assert len(expense_columns) == 10

    assert expenses["ExpenseKey"].is_unique
    assert not expenses[expense_columns].isna().any().any()

    assert expenses["AllocationMethod"].isin(
        ["Direct", "Allocated"]
    ).all()

    # Every shared expense must allocate to exactly three locations.
    shared = expenses[
        expenses["AllocationMethod"] == "Allocated"
    ]

    assert (
        shared.groupby("ExpenseReference")["LocationKey"]
        .nunique()
        == len(location_keys)
    ).all()

    expenses = expenses[expense_columns].copy()

    print("\nFinal FactExpenses schema validation passed.")
    print(f"Rows: {len(expenses):,}")
    print(f"Columns: {len(expenses.columns)}")

    expense_path = DATA_DIR / "FactExpenses.csv"
    expenses.to_csv(expense_path, index=False)

    print(f"FactExpenses exported: {expense_path}")

    return expenses

def generate_inventory_snapshots(
    dimensions: dict[str, pd.DataFrame],
    sales: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """
    Generate monthly product inventory snapshots.

    Inventory movements are based on FactSales quantities.
    Positive quantities represent sales.
    Negative quantities represent returns.
    """

    products = dimensions["DimProduct"].copy()
    locations = dimensions["DimLocation"].copy()

    months = pd.date_range(
        START_DATE,
        END_DATE,
        freq="MS",
    )

    print("\nFactInventorySnapshot generation initialized.")

    # Establish all product/location combinations.
    inventory_base = products[
        [
            "ProductKey",
            "Category",
            "StandardUnitCost",
            "ReorderPoint",
            "IsActive",
        ]
    ].merge(
        locations[["LocationKey"]],
        how="cross",
    )

    assert len(inventory_base) == (
        len(products) * len(locations)
    )

    assert not inventory_base.duplicated(
        ["LocationKey", "ProductKey"]
    ).any()

    print(
        f"Product/location combinations: "
        f"{len(inventory_base):,}"
    )

    # Opening inventory is established before January 2025.
    # The opening balance is internal to the simulation,
    # not an exported snapshot.
    inventory_base["OpeningUnits"] = [
        int(
            row.ReorderPoint
            * rng.integers(2, 5)
        )
        for row in inventory_base.itertuples(index=False)
    ]

    assert (
        inventory_base["OpeningUnits"] >=
        inventory_base["ReorderPoint"]
    ).all()

    print(
        f"Total opening inventory units: "
        f"{inventory_base['OpeningUnits'].sum():,}"
    )

    # Prepare sales and returns.
    inventory_sales = sales[
        [
            "DateKey",
            "LocationKey",
            "ProductKey",
            "TransactionType",
            "Quantity",
        ]
    ].copy()

    assert inventory_sales["TransactionType"].isin(
        ["Sale", "Return"]
    ).all()

    assert (
        inventory_sales.loc[
            inventory_sales["TransactionType"] == "Sale",
            "Quantity",
        ] > 0
    ).all()

    assert (
        inventory_sales.loc[
            inventory_sales["TransactionType"] == "Return",
            "Quantity",
        ] < 0
    ).all()

    inventory_sales["Month"] = (
        pd.to_datetime(
            inventory_sales["DateKey"].astype(str),
            format="%Y%m%d",
        )
        .dt.to_period("M")
    )

    monthly_sales = (
        inventory_sales.groupby(
            ["Month", "LocationKey", "ProductKey"]
        )["Quantity"]
        .sum()
    )

    print("\nInventory transaction quantities:")

    gross_sales = inventory_sales.loc[
        inventory_sales["TransactionType"] == "Sale",
        "Quantity",
    ].sum()

    returned_units = -inventory_sales.loc[
        inventory_sales["TransactionType"] == "Return",
        "Quantity",
    ].sum()

    net_sales = inventory_sales["Quantity"].sum()

    print(f"Gross units sold: {gross_sales:,}")
    print(f"Units returned: {returned_units:,}")
    print(f"Net units sold: {net_sales:,}")

    assert gross_sales == 64093
    assert returned_units == 2914
    assert net_sales == 61179

    assert monthly_sales.sum() == net_sales

    print("Inventory transaction reconciliation passed.")

    print(f"Reporting months: {len(months)}")

    # Daily sales quantities, preserving the signed-return convention.
    daily_sales = (
        inventory_sales.groupby(
            ["DateKey", "LocationKey", "ProductKey"]
        )["Quantity"]
        .sum()
        .to_dict()
    )

    # Initialize inventory balances and metadata.
    inventory_state = {}

    for row in inventory_base.itertuples(index=False):
        key = (int(row.LocationKey), int(row.ProductKey))

        inventory_state[key] = {
            "OnHand": int(row.OpeningUnits),
            "ReorderPoint": int(row.ReorderPoint),
            "UnitCost": Decimal(str(row.StandardUnitCost)),
            "LastSaleDate": None,
            "TotalReplenished": 0,
        }

    snapshots = []
    snapshot_key = 1

    # Process inventory chronologically.
    for month in months:
        month_end = month + pd.offsets.MonthEnd(0)

        days = pd.date_range(month, month_end, freq="D")

        for date in days:
            date_key = int(date.strftime("%Y%m%d"))

            for (location_key, product_key), state in inventory_state.items():
                net_quantity = int(
                    daily_sales.get(
                        (date_key, location_key, product_key),
                        0,
                    )
                )

                # Ensure sufficient inventory before fulfilling net sales.
                if net_quantity > state["OnHand"]:
                    reorder_quantity = max(
                        state["ReorderPoint"] * 3,
                        net_quantity - state["OnHand"]
                        + state["ReorderPoint"] * 2,
                    )

                    state["OnHand"] += reorder_quantity
                    state["TotalReplenished"] += reorder_quantity

                # Positive quantity reduces stock.
                # Negative quantity (net returns) increases stock.
                state["OnHand"] -= net_quantity

                assert state["OnHand"] >= 0

                if net_quantity > 0:
                    state["LastSaleDate"] = date

                # Replenish again when inventory reaches reorder point.
                if state["OnHand"] <= state["ReorderPoint"]:
                    reorder_quantity = state["ReorderPoint"] * 3

                    state["OnHand"] += reorder_quantity
                    state["TotalReplenished"] += reorder_quantity

        # Capture one month-end snapshot per product/location.
        for (location_key, product_key), state in inventory_state.items():
            on_hand = state["OnHand"]

            # Simplified reservation model: 0–5% of current stock.
            reserved = int(
                rng.integers(
                    0,
                    max(1, int(on_hand * 0.05) + 1),
                )
            )

            available = on_hand - reserved

            inventory_value = money(
                Decimal(on_hand) * state["UnitCost"]
            )

            if state["LastSaleDate"] is None:
                days_since_last_sale = (
                    month_end - pd.Timestamp(START_DATE)
                ).days + 1
            else:
                days_since_last_sale = (
                    month_end - state["LastSaleDate"]
                ).days

            if available == 0:
                stock_status = "Out of Stock"
            elif available <= state["ReorderPoint"]:
                stock_status = "Low Stock"
            else:
                stock_status = "Available"

            snapshots.append({
                "InventorySnapshotKey": snapshot_key,
                "DateKey": int(month_end.strftime("%Y%m%d")),
                "LocationKey": location_key,
                "ProductKey": product_key,
                "UnitsOnHand": on_hand,
                "UnitsReserved": reserved,
                "UnitsAvailable": available,
                "UnitInventoryCost": float(state["UnitCost"]),
                "InventoryValue": float(inventory_value),
                "ReorderPoint": state["ReorderPoint"],
                "DaysSinceLastSale": days_since_last_sale,
                "StockStatus": stock_status,
            })

            snapshot_key += 1

    inventory = pd.DataFrame(snapshots)

    print("\nInventory simulation completed.")
    print(f"Monthly snapshot records: {len(inventory):,}")

    assert len(inventory) == (
        len(products) * len(locations) * len(months)
    )

    assert inventory["InventorySnapshotKey"].is_unique

    assert not inventory.duplicated(
        ["DateKey", "LocationKey", "ProductKey"]
    ).any()

    assert (inventory["UnitsOnHand"] >= 0).all()
    assert (inventory["UnitsReserved"] >= 0).all()
    assert (inventory["UnitsAvailable"] >= 0).all()

    assert (
        inventory["UnitsOnHand"]
        == inventory["UnitsReserved"] + inventory["UnitsAvailable"]
    ).all()

    total_replenished = sum(
        state["TotalReplenished"]
        for state in inventory_state.values()
    )

    closing_units = sum(
        state["OnHand"]
        for state in inventory_state.values()
    )

    opening_units = inventory_base["OpeningUnits"].sum()

    assert (
        opening_units + total_replenished - net_sales
        == closing_units
    ), (
        "Inventory movement reconciliation failed."
    )

    print("\nInventory movement reconciliation:")
    print(f"Opening units: {opening_units:,}")
    print(f"Replenished units: {total_replenished:,}")
    print(f"Net units sold: {net_sales:,}")
    print(f"Closing units: {closing_units:,}")
    print("Inventory movement reconciliation passed.")

    print("\nStock status distribution:")
    print(inventory["StockStatus"].value_counts().to_string())

    # Validate inventory snapshot foreign keys.
    assert inventory["DateKey"].isin(
        dimensions["DimDate"]["DateKey"]
    ).all()

    assert inventory["LocationKey"].isin(
        locations["LocationKey"]
    ).all()

    assert inventory["ProductKey"].isin(
        products["ProductKey"]
    ).all()

    # Validate inventory valuation using exact decimal arithmetic.
    expected_values = [
        money(
            Decimal(int(row.UnitsOnHand))
            * Decimal(str(row.UnitInventoryCost))
        )
        for row in inventory.itertuples(index=False)
    ]

    actual_values = [
        Decimal(str(value))
        for value in inventory["InventoryValue"]
    ]

    assert expected_values == actual_values, (
        "Inventory valuations do not reconcile."
    )

    # Validate inventory aging.
    assert (
        inventory["DaysSinceLastSale"] >= 0
    ).all()

    # Validate inventory stock classifications.
    for row in inventory.itertuples(index=False):
        if row.UnitsAvailable == 0:
            expected_status = "Out of Stock"
        elif row.UnitsAvailable <= row.ReorderPoint:
            expected_status = "Low Stock"
        else:
            expected_status = "Available"

        assert row.StockStatus == expected_status, (
            "Inventory stock status does not match available units."
        )

    # Every reporting month must contain 360 snapshots.
    monthly_counts = inventory.groupby("DateKey").size()

    assert len(monthly_counts) == 24
    assert (monthly_counts == 360).all()

    print("\nInventory valuation and integrity validation passed.")

    print(
        f"Total inventory value across all snapshots: "
        f"${inventory['InventoryValue'].sum():,.2f}"
    )

    latest_date = inventory["DateKey"].max()

    latest_inventory = inventory[
        inventory["DateKey"] == latest_date
    ]

    print(
        f"Closing inventory value ({latest_date}): "
        f"${latest_inventory['InventoryValue'].sum():,.2f}"
    )

    # Final FactInventorySnapshot schema.
    inventory_columns = [
        "InventorySnapshotKey",
        "DateKey",
        "LocationKey",
        "ProductKey",
        "UnitsOnHand",
        "UnitsReserved",
        "UnitsAvailable",
        "UnitInventoryCost",
        "InventoryValue",
        "ReorderPoint",
        "DaysSinceLastSale",
        "StockStatus",
    ]

    assert len(inventory_columns) == 12
    assert set(inventory_columns).issubset(inventory.columns)

    inventory_final = inventory[inventory_columns].copy()

    assert inventory_final.shape == (8640, 12)
    assert not inventory_final.isna().any().any()
    assert inventory_final["InventorySnapshotKey"].is_unique

    print("\nFinal FactInventorySnapshot schema validated.")
    print(f"Rows: {len(inventory_final):,}")
    print(f"Columns: {len(inventory_final.columns)}")

    inventory_path = DATA_DIR / "FactInventorySnapshot.csv"

    inventory_final.to_csv(
        inventory_path,
        index=False,
        float_format="%.2f",
    )

    print(f"FactInventorySnapshot exported: {inventory_path}")

    return inventory_final

    return inventory

def main() -> None:
    """Generate and validate Northstar fact tables."""

    dimensions = load_dimensions()

    print("Northstar fact generator initialized.")
    print(f"Reporting period: {START_DATE.date()} to {END_DATE.date()}")
    print(f"Dimensions loaded: {len(dimensions)}")

    for name, dataframe in dimensions.items():
        print(f"  {name}: {len(dataframe):,} records")

    rng = np.random.default_rng(RANDOM_SEED)

    # Generate original retail transactions.
    sales = generate_sales(dimensions, rng)

    # Generate returns against existing sales.
    returns = generate_returns(sales, rng)

    sales = pd.concat(
        [sales, returns],
        ignore_index=True,
    )

    validate_sales(sales, dimensions)

    output_path = DATA_DIR / "FactSales.csv"
    sales.to_csv(output_path, index=False)

    print(f"FactSales exported: {output_path}")

    print(f"Returns generated: {len(returns):,}")

    print(f"\nFactSales generated: {len(sales):,} sales lines")
    print(f"Unique transactions: {sales['TransactionID'].nunique():,}")

    # Generate and export completed service-job fact table.
    service_jobs = generate_service_jobs(dimensions, rng)

    service_output_path = DATA_DIR / "FactServiceJobs.csv"

    service_jobs.to_csv(
        service_output_path,
        index=False,
    )

    print(f"\nFactServiceJobs exported: {service_output_path}")
    print(f"Service-job records exported: {len(service_jobs):,}")

    # Begin labor generation using completed service activity.
    labor_workload = generate_labor(
        dimensions,
        service_jobs,
        rng,
    )

    print(
        f"Service labor workload records: "
        f"{len(labor_workload):,}"
    )

    # Allocate completed jobs to their originating labor records.
    job_labor_allocations = generate_job_labor_allocations(
        service_jobs,
        labor_workload,
    )

    # Reconcile allocated direct labor costs to FactLabor.
    direct_costs = (
        job_labor_allocations.groupby("LaborKey")[
            "AllocatedDirectLaborCost"
        ]
        .sum()
        .round(2)
    )

    labor_workload["DirectServiceLaborCost"] = (
        labor_workload["LaborKey"]
        .map(direct_costs)
        .fillna(0.0)
        .round(2)
    )

    # Non-direct labor is the remaining fully loaded payroll cost.
    labor_workload["NonDirectLaborCost"] = (
        labor_workload["FullyLoadedLaborCost"]
        - labor_workload["DirectServiceLaborCost"]
    ).round(2)

    # Validate that allocations do not exceed the source payroll.
    assert (
        labor_workload["DirectServiceLaborCost"]
        <= labor_workload["FullyLoadedLaborCost"] + 0.001
    ).all(), (
        "Allocated direct labor exceeds fully loaded labor cost."
    )

    assert (
        labor_workload["NonDirectLaborCost"] >= -0.001
    ).all(), (
        "Negative non-direct labor cost detected."
    )

    # Validate labor cost reconciliation by individual labor record.
    assert np.allclose(
        labor_workload["FullyLoadedLaborCost"],
        labor_workload["DirectServiceLaborCost"]
        + labor_workload["NonDirectLaborCost"],
        atol=0.001,
    ), (
        "Labor costs do not reconcile by labor record."
    )

    # Validate total direct labor allocation.
    total_allocated = money(
        job_labor_allocations["AllocatedDirectLaborCost"].sum()
    )

    total_direct = money(
        labor_workload["DirectServiceLaborCost"].sum()
    )

    assert total_allocated == total_direct, (
        "Direct labor costs do not reconcile to allocations."
    )

    print("\n=== FINAL LABOR COST RECONCILIATION ===")

    print(
        f"Fully loaded payroll: "
        f"${labor_workload['FullyLoadedLaborCost'].sum():,.2f}"
    )

    print(
        f"Direct service labor: "
        f"${labor_workload['DirectServiceLaborCost'].sum():,.2f}"
    )

    print(
        f"Non-direct labor: "
        f"${labor_workload['NonDirectLaborCost'].sum():,.2f}"
    )

    print(
        f"Allocated job labor: "
        f"${job_labor_allocations['AllocatedDirectLaborCost'].sum():,.2f}"
    )

    print("Labor cost reconciliation passed.")

    # Finalize FactLabor using the documented analytical schema.
    labor_columns = [
        "LaborKey",
        "DateKey",
        "EmployeeKey",
        "LocationKey",
        "ScheduledHours",
        "RegularHours",
        "OvertimeHours",
        "AvailableProductiveHours",
        "BillableHours",
        "NonBillableHours",
        "BaseHourlyRate",
        "OvertimeMultiplier",
        "EmployerBurdenRate",
        "GrossWages",
        "EmployerBurdenCost",
        "FullyLoadedLaborCost",
        "DirectServiceLaborCost",
        "NonDirectLaborCost",
    ]

    # Finalize FactJobLaborAllocation.
    allocation_columns = [
        "JobLaborAllocationKey",
        "LaborKey",
        "ServiceJobKey",
        "AllocatedRegularHours",
        "AllocatedOvertimeHours",
        "AllocatedHours",
        "AllocatedDirectLaborCost",
    ]

    assert set(labor_columns).issubset(labor_workload.columns), (
        "FactLabor is missing required columns."
    )

    assert set(allocation_columns).issubset(
        job_labor_allocations.columns
    ), (
        "FactJobLaborAllocation is missing required columns."
    )

    labor_final = labor_workload[labor_columns].copy()

    allocations_final = job_labor_allocations[
        allocation_columns
    ].copy()

    assert len(labor_final) == 10524
    assert len(allocations_final) == 8944

    assert labor_final["LaborKey"].is_unique
    assert allocations_final["JobLaborAllocationKey"].is_unique

    print("\nFinal labor schemas validated.")
    print(
        f"FactLabor: {len(labor_final):,} rows, "
        f"{len(labor_final.columns)} columns"
    )
    print(
        f"FactJobLaborAllocation: "
        f"{len(allocations_final):,} rows, "
        f"{len(allocations_final.columns)} columns"
    )

    # Export the reconciled fact tables.
    labor_path = DATA_DIR / "FactLabor.csv"
    allocations_path = DATA_DIR / "FactJobLaborAllocation.csv"

    labor_final.to_csv(labor_path, index=False)
    allocations_final.to_csv(allocations_path, index=False)

    print(f"\nFactLabor exported: {labor_path}")
    print(f"FactJobLaborAllocation exported: {allocations_path}")

    print(
        f"Job labor allocation records: "
        f"{len(job_labor_allocations):,}"
    )

    # Generate non-payroll operating expenses.
    expenses = generate_expenses(
        dimensions,
        sales,
        service_jobs,
        rng,
    )

    print(
        f"FactExpenses working records: "
        f"{len(expenses):,}"
    )

    # Initialize the inventory snapshot simulation.
    inventory_snapshots = generate_inventory_snapshots(
        dimensions,
        sales,
        rng,
    )

    print(
        f"Inventory initialization records: "
        f"{len(inventory_snapshots):,}"
    )

if __name__ == "__main__":
    main()