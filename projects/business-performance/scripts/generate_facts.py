"""
Northstar Home & Tech
Portfolio Project 002 — Business Performance Analytics

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

    print("\nCapacity-aware rescheduling results:")
    print(f"Jobs rescheduled: {rescheduled_count:,}")
    print(f"Jobs still unresolved: {unresolved_count:,}")

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

    return pd.DataFrame()

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

    generate_service_jobs(dimensions, rng)

if __name__ == "__main__":
    main()