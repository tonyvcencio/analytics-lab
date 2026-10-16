"""
Northstar Home & Tech
Portfolio Project 002 — Business Performance Analytics

Generate foundational synthetic dimension tables.

Initial scope:
    - DimDate
    - DimLocation
"""

from pathlib import Path
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data"

START_DATE = "2025-01-01"
END_DATE = "2026-12-31"
CALENDAR_END_DATE = "2027-01-14"


def generate_dates() -> pd.DataFrame:
    """Generate the Northstar calendar dimension."""

    dates = pd.date_range(
        start=START_DATE,
        end=CALENDAR_END_DATE,
        freq="D",
    )

    df = pd.DataFrame({"FullDate": dates})

    df["DateKey"] = df["FullDate"].dt.strftime("%Y%m%d").astype(int)
    df["Year"] = df["FullDate"].dt.year
    df["Quarter"] = df["FullDate"].dt.quarter
    df["MonthNumber"] = df["FullDate"].dt.month
    df["MonthName"] = df["FullDate"].dt.month_name()
    df["YearMonth"] = df["FullDate"].dt.strftime("%Y-%m")
    df["DayOfWeek"] = df["FullDate"].dt.dayofweek + 1
    df["IsWeekend"] = df["DayOfWeek"].isin([6, 7])

    columns = [
        "DateKey",
        "FullDate",
        "Year",
        "Quarter",
        "MonthNumber",
        "MonthName",
        "YearMonth",
        "DayOfWeek",
        "IsWeekend",
    ]

    return df[columns]


def generate_locations() -> pd.DataFrame:
    """Generate Northstar's three operating locations."""

    locations = [
        {
            "LocationKey": 1,
            "LocationName": "Northstar Central",
            "Region": "Central",
            "OpeningDate": "2022-06-01",
            "SquareFootage": 4200,
            "LocationType": "Flagship",
        },
        {
            "LocationKey": 2,
            "LocationName": "Northstar West",
            "Region": "West",
            "OpeningDate": "2023-03-15",
            "SquareFootage": 3100,
            "LocationType": "Retail-Focused",
        },
        {
            "LocationKey": 3,
            "LocationName": "Northstar East",
            "Region": "East",
            "OpeningDate": "2023-09-01",
            "SquareFootage": 2800,
            "LocationType": "Service-Focused",
        },
    ]

    return pd.DataFrame(locations)

def generate_products() -> pd.DataFrame:
    """Generate a reproducible catalog of 120 fictional products."""

    rng = np.random.default_rng(2026)

    price_ranges = {
    # Computers
    "Laptop": (499, 1799),
    "Desktop": (599, 1499),
    "Mini PC": (299, 899),
    "Monitor": (129, 699),
    "Workstation": (1199, 2499),

    # Accessories
    "Keyboard": (25, 179),
    "Mouse": (15, 129),
    "USB-C Dock": (49, 249),
    "External SSD": (59, 229),
    "Webcam": (29, 149),
    "Headset": (35, 199),
    "Cable Kit": (12, 49),
    "Laptop Stand": (19, 89),

    # Networking
    "Wi-Fi Router": (69, 399),
    "Network Switch": (39, 299),
    "Access Point": (79, 349),
    "Mesh Node": (59, 249),
    "Network Adapter": (19, 99),

    # Smart Home
    "Security Camera": (49, 249),
    "Smart Plug": (15, 49),
    "Smart Bulb": (12, 59),
    "Motion Sensor": (19, 79),
    "Smart Hub": (69, 249),
    "Video Doorbell": (79, 299),
}

    catalog = {
        "Computers": {
            "count": 25,
            "families": [
                "Laptop",
                "Desktop",
                "Mini PC",
                "Monitor",
                "Workstation",
            ],
            "margin_range": (0.12, 0.22),
            "reorder_range": (3, 12),
        },
        "Accessories": {
            "count": 40,
            "families": [
                "Keyboard",
                "Mouse",
                "USB-C Dock",
                "External SSD",
                "Webcam",
                "Headset",
                "Cable Kit",
                "Laptop Stand",
            ],
            "margin_range": (0.35, 0.60),
            "reorder_range": (10, 40),
        },
        "Networking": {
            "count": 25,
            "families": [
                "Wi-Fi Router",
                "Network Switch",
                "Access Point",
                "Mesh Node",
                "Network Adapter",
            ],
            "margin_range": (0.22, 0.40),
            "reorder_range": (5, 20),
        },
        "Smart Home": {
            "count": 30,
            "families": [
                "Security Camera",
                "Smart Plug",
                "Smart Bulb",
                "Motion Sensor",
                "Smart Hub",
                "Video Doorbell",
            ],
            "margin_range": (0.25, 0.45),
            "reorder_range": (5, 25),
        },
    }

    brands = [
        "Aster",
        "Novatek",
        "Orion",
        "Lumina",
        "Vantage",
        "Helix",
    ]

    category_codes = {
        "Computers": "CMP",
        "Accessories": "ACC",
        "Networking": "NET",
        "Smart Home": "SMH",
    }

    products = []
    product_key = 1

    for category, config in catalog.items():
        for index in range(1, config["count"] + 1):
            family = config["families"][
                (index - 1) % len(config["families"])
            ]

            brand = brands[
                (index - 1) % len(brands)
            ]

            retail_price = round(
                float(rng.uniform(*price_ranges[family])),
                2,
            )

            target_margin = float(
                rng.uniform(*config["margin_range"])
            )

            unit_cost = round(
                retail_price * (1 - target_margin),
                2,
            )

            reorder_point = int(
                rng.integers(
                    config["reorder_range"][0],
                    config["reorder_range"][1] + 1,
                )
            )

            sku = f"{category_codes[category]}-{index:04d}"

            products.append(
                {
                    "ProductKey": product_key,
                    "SKU": sku,
                    "ProductName": f"{brand} {family} {index:02d}",
                    "Category": category,
                    "Subcategory": family,
                    "Brand": brand,
                    "StandardRetailPrice": retail_price,
                    "StandardUnitCost": unit_cost,
                    "ReorderPoint": reorder_point,
                    "IsActive": True,
                }
            )

            product_key += 1

    return pd.DataFrame(products)

def generate_services() -> pd.DataFrame:
    """Generate Northstar's 20 standard service offerings."""

    offerings = [
        # Computer Repair
        ("Diagnostic Assessment", "Computer Repair", 49, 0.5, False),
        ("Operating System Repair", "Computer Repair", 129, 2.0, True),
        ("Hardware Replacement", "Computer Repair", 119, 1.5, True),
        ("Malware Removal", "Computer Repair", 99, 1.5, True),

        # Network Installation
        ("Router Installation", "Network Installation", 129, 1.5, True),
        ("Mesh Network Setup", "Network Installation", 199, 2.5, True),
        ("Small Office Network Setup", "Network Installation", 399, 5.0, True),
        ("Network Optimization", "Network Installation", 149, 2.0, True),

        # Smart Home Installation
        ("Security Camera Installation", "Smart Home Installation", 149, 2.0, True),
        ("Smart Lighting Setup", "Smart Home Installation", 99, 1.5, True),
        ("Video Doorbell Installation", "Smart Home Installation", 129, 1.5, True),
        ("Smart Home Integration", "Smart Home Installation", 249, 3.0, True),

        # Troubleshooting
        ("Computer Troubleshooting", "Troubleshooting", 79, 1.0, False),
        ("Network Troubleshooting", "Troubleshooting", 99, 1.5, False),
        ("Peripheral Troubleshooting", "Troubleshooting", 59, 0.75, False),

        # Technical Support
        ("Remote Support Session", "Technical Support", 49, 0.5, False),
        ("On-Site Technical Support", "Technical Support", 129, 1.5, True),

        # Device Setup
        ("New Computer Setup", "Device Setup", 99, 1.5, True),
        ("Data Transfer", "Device Setup", 149, 2.0, True),
        ("Printer Setup", "Device Setup", 69, 1.0, False),
    ]

    rows = []

    for index, (name, category, rate, duration, appointment) in enumerate(
        offerings, start=1
    ):
        rows.append(
            {
                "ServiceKey": index,
                "ServiceCode": f"SRV-{index:04d}",
                "ServiceName": name,
                "ServiceCategory": category,
                "StandardRate": float(rate),
                "EstimatedDurationHours": float(duration),
                "RequiresAppointment": appointment,
                "IsActive": True,
            }
        )

    return pd.DataFrame(rows)

def generate_expense_categories() -> pd.DataFrame:
    """Generate Northstar's operating expense classifications."""

    categories = [
        ("Rent", "Occupancy", "Fixed",
         "Lease expense for retail and service locations."),
        ("Utilities", "Occupancy", "Mixed",
         "Electricity, water, and other facility utilities."),
        ("Insurance", "General Operations", "Fixed",
         "Business liability and property insurance."),
        ("Marketing", "Sales and Marketing", "Variable",
         "Advertising, promotions, and customer acquisition."),
        ("Software Subscriptions", "Technology", "Fixed",
         "Recurring software and business application expenses."),
        ("Equipment Maintenance", "General Operations", "Mixed",
         "Maintenance of company-owned operational equipment."),
        ("Administrative Supplies", "Administration", "Variable",
         "Office supplies and administrative consumables."),
        ("Merchant Processing Fees", "Sales and Marketing", "Variable",
         "Payment processing fees associated with transactions."),
        ("Other Operating Expenses", "General Operations", "Mixed",
         "Operating expenses not classified elsewhere."),
    ]

    return pd.DataFrame(
        [
            {
                "ExpenseCategoryKey": index,
                "ExpenseCategory": name,
                "ExpenseGroup": group,
                "CostBehavior": behavior,
                "Description": description,
            }
            for index, (name, group, behavior, description)
            in enumerate(categories, start=1)
        ]
    )

def validate_dimensions(
    dates: pd.DataFrame,
    locations: pd.DataFrame,
    products: pd.DataFrame,
    services: pd.DataFrame,
    expense_categories: pd.DataFrame,
    employees: pd.DataFrame,
    customers: pd.DataFrame
) -> None:
    """Validate foundational dimension integrity."""

    expected_calendar_days = (
        pd.Timestamp(CALENDAR_END_DATE)
        - pd.Timestamp(START_DATE)
    ).days + 1

    if len(dates) != expected_calendar_days:
        raise ValueError(
            f"Unexpected calendar row count. "
            f"Expected {expected_calendar_days}, "
            f"found {len(dates)}."
        )

    if not dates["DateKey"].is_unique:
        raise ValueError("Duplicate DateKey detected.")

    if not dates["FullDate"].is_unique:
        raise ValueError("Duplicate FullDate detected.")

    if len(locations) != 3:
        raise ValueError("Unexpected location count.")

    if not locations["LocationKey"].is_unique:
        raise ValueError("Duplicate LocationKey detected.")

    if len(products) != 120:
        raise ValueError("Unexpected product count.")

    if not products["ProductKey"].is_unique:
        raise ValueError("Duplicate ProductKey detected.")

    if not products["SKU"].is_unique:
        raise ValueError("Duplicate SKU detected.")

    if products.isnull().any().any():
        raise ValueError("Missing product values detected.")

    if (products["StandardRetailPrice"] < 0).any():
        raise ValueError("Negative retail price detected.")

    if (products["StandardUnitCost"] < 0).any():
        raise ValueError("Negative unit cost detected.")

    if (
        products["StandardUnitCost"]
        > products["StandardRetailPrice"]
    ).any():
        raise ValueError("Product cost exceeds retail price.")

    expected_categories = {
        "Computers",
        "Accessories",
        "Networking",
        "Smart Home",
    }

    if set(products["Category"]) != expected_categories:
        raise ValueError("Unexpected product categories.")

    # Validate services
    if len(services) != 20:
        raise ValueError("Unexpected service count.")

    if not services["ServiceKey"].is_unique:
        raise ValueError("Duplicate ServiceKey detected.")

    if not services["ServiceCode"].is_unique:
        raise ValueError("Duplicate ServiceCode detected.")

    if services.isnull().any().any():
        raise ValueError("Missing service values detected.")

    if (services["StandardRate"] < 0).any():
        raise ValueError("Negative service rate detected.")

    if (services["EstimatedDurationHours"] < 0).any():
        raise ValueError("Negative service duration detected.")

    expected_service_categories = {
        "Computer Repair",
        "Network Installation",
        "Smart Home Installation",
        "Troubleshooting",
        "Technical Support",
        "Device Setup",
    }

    if set(services["ServiceCategory"]) != expected_service_categories:
        raise ValueError("Unexpected service categories.")

    # Validate expense categories
    if len(expense_categories) != 9:
        raise ValueError("Unexpected expense category count.")

    if not expense_categories["ExpenseCategoryKey"].is_unique:
        raise ValueError("Duplicate ExpenseCategoryKey detected.")

    if not expense_categories["ExpenseCategory"].is_unique:
        raise ValueError("Duplicate expense category detected.")

    if expense_categories.isnull().any().any():
        raise ValueError("Missing expense category values detected.")

    valid_cost_behaviors = {"Fixed", "Variable", "Mixed"}

    if not set(expense_categories["CostBehavior"]).issubset(
        valid_cost_behaviors
    ):
        raise ValueError("Invalid expense cost behavior.")
        
    # Validate employees
    if len(employees) != 30:
        raise ValueError("Unexpected employee count.")

    if not employees["EmployeeKey"].is_unique:
        raise ValueError("Duplicate EmployeeKey detected.")

    if not employees["EmployeeCode"].is_unique:
        raise ValueError("Duplicate EmployeeCode detected.")

    required_columns = [
        "EmployeeKey",
        "EmployeeCode",
        "JobRole",
        "Department",
        "HomeLocationKey",
        "HireDate",
        "EmploymentType",
        "StandardHourlyRate",
        "IsActive",
    ]

    if employees[required_columns].isnull().any().any():
        raise ValueError("Missing required employee values.")

    if not employees["HomeLocationKey"].isin(
        locations["LocationKey"]
    ).all():
        raise ValueError("Invalid employee home location.")

    hire_dates = pd.to_datetime(employees["HireDate"])
    termination_dates = pd.to_datetime(employees["TerminationDate"])

    if (
        termination_dates.notna()
        & (termination_dates < hire_dates)
    ).any():
        raise ValueError("Termination date precedes hire date.")

    if (
        employees["IsActive"].astype(bool)
        != termination_dates.isna()
    ).any():
        raise ValueError("Employee active status is inconsistent.")

    if (employees["StandardHourlyRate"] < 0).any():
        raise ValueError("Negative employee hourly rate.")

    if not employees["EmploymentType"].isin(
        ["Full-Time", "Part-Time"]
    ).all():
        raise ValueError("Invalid employee employment type.")

    if not employees["Department"].isin(
        ["Retail", "Service", "Administration"]
    ).all():
        raise ValueError("Invalid employee department.")

    # Validate customers
    if len(customers) != 8000:
        raise ValueError("Unexpected customer count.")

    if customers["CustomerKey"].isnull().any():
        raise ValueError("Missing CustomerKey detected.")

    if not customers["CustomerKey"].is_unique:
        raise ValueError("Duplicate CustomerKey detected.")

    if customers.isnull().any().any():
        raise ValueError("Missing customer values detected.")

    if not customers["CustomerType"].isin(
        ["Residential", "Small Business"]
    ).all():
        raise ValueError("Invalid customer type.")

    valid_channels = {
        "Walk-In",
        "Online Search",
        "Referral",
        "Social Media",
        "Local Advertising",
        "Business Partnership",
    }

    if not customers["AcquisitionChannel"].isin(valid_channels).all():
        raise ValueError("Invalid customer acquisition channel.")

    if not customers["HomeLocationKey"].isin(
        locations["LocationKey"]
    ).all():
        raise ValueError("Invalid customer home location.")

    signup_dates = pd.to_datetime(customers["SignupDate"])

    if signup_dates.isnull().any():
        raise ValueError("Invalid customer signup date.")

    if (
        (signup_dates < pd.Timestamp("2023-01-01"))
        | (signup_dates > pd.Timestamp("2026-12-31"))
    ).any():
        raise ValueError("Customer signup date outside expected range.")

    print("Dimension validation passed.")

def generate_customers() -> pd.DataFrame:
    """Generate 8,000 reproducible fictional customer records."""

    rng = np.random.default_rng(2028)
    customer_count = 8000

    customer_types = rng.choice(
        ["Residential", "Small Business"],
        size=customer_count,
        p=[0.84, 0.16],
    )

    channels = [
        "Walk-In",
        "Online Search",
        "Referral",
        "Social Media",
        "Local Advertising",
        "Business Partnership",
    ]

    residential_weights = [0.32, 0.26, 0.19, 0.13, 0.08, 0.02]
    business_weights = [0.10, 0.20, 0.24, 0.05, 0.11, 0.30]

    acquisition_channels = [
        rng.choice(
            channels,
            p=(
                residential_weights
                if customer_type == "Residential"
                else business_weights
            ),
        )
        for customer_type in customer_types
    ]

    home_locations = rng.choice(
        [1, 2, 3],
        size=customer_count,
        p=[0.42, 0.33, 0.25],
    )

    # Allow customers to register before the reporting period.
    signup_start = pd.Timestamp("2023-01-01")
    signup_end = pd.Timestamp("2026-12-31")
    date_range_days = (signup_end - signup_start).days + 1

    signup_offsets = rng.integers(
        0, date_range_days, size=customer_count
    )

    signup_dates = [
        (signup_start + pd.Timedelta(days=int(offset))).date()
        for offset in signup_offsets
    ]

    return pd.DataFrame(
        {
            "CustomerKey": np.arange(1, customer_count + 1),
            "CustomerType": customer_types,
            "AcquisitionChannel": acquisition_channels,
            "SignupDate": signup_dates,
            "HomeLocationKey": home_locations,
        }
    )

def main() -> None:
    """Generate, validate, and export dimensions."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dates = generate_dates()
    locations = generate_locations()
    products = generate_products()
    services = generate_services()
    expense_categories = generate_expense_categories()
    employees = generate_employees()
    customers = generate_customers()
    validate_dimensions(
    dates,
        locations,
        products,
        services,
        expense_categories,
        employees,
        customers
    )

    dates.to_csv(OUTPUT_DIR / "DimDate.csv", index=False)
    locations.to_csv(OUTPUT_DIR / "DimLocation.csv", index=False)
    products.to_csv(OUTPUT_DIR / "DimProduct.csv", index=False)
    services.to_csv(OUTPUT_DIR / "DimService.csv", index=False)
    expense_categories.to_csv(
        OUTPUT_DIR / "DimExpenseCategory.csv", index=False
    )
    employees.to_csv(OUTPUT_DIR / "DimEmployee.csv", index=False)
    customers.to_csv(OUTPUT_DIR / "DimCustomer.csv", index=False)

    print(f"DimDate: {len(dates):,} records")
    print(f"DimLocation: {len(locations):,} records")
    print(f"DimProduct: {len(products):,} records")
    print(f"DimService: {len(services):,} records")
    print(f"DimExpenseCategory: {len(expense_categories):,} records")
    print(f"DimEmployee: {len(employees):,} records")
    print(f"DimCustomer: {len(customers):,} records")
    print(f"Output directory: {OUTPUT_DIR}")


def generate_employees() -> pd.DataFrame:
    """Generate 30 fictional Northstar employees."""

    rng = np.random.default_rng(2027)

    roles = [
        ("Retail Associate", "Retail", 17, 23),
        ("Senior Retail Associate", "Retail", 22, 29),
        ("Service Technician", "Service", 22, 32),
        ("Senior Service Technician", "Service", 30, 42),
        ("Store Manager", "Administration", 34, 46),
        ("Assistant Manager", "Administration", 26, 36),
        ("Administrative Support", "Administration", 18, 26),
    ]

    # Each location receives ten employees.
    location_roles = {
        1: [0, 0, 0, 1, 1, 2, 2, 3, 4, 5],
        2: [0, 0, 0, 0, 1, 2, 2, 4, 5, 6],
        3: [0, 0, 1, 2, 2, 2, 3, 3, 4, 5],
    }

    rows = []
    employee_key = 1

    for location_key, role_indices in location_roles.items():
        for role_index in role_indices:
            role, department, wage_min, wage_max = roles[role_index]

            hire_date = pd.Timestamp("2023-01-01") + pd.Timedelta(
                days=int(rng.integers(0, 1370))
            )

            employment_type = (
                "Part-Time"
                if role_index in (0, 6) and rng.random() < 0.35
                else "Full-Time"
            )

            termination_date = pd.NaT

            # Some earlier hires leave during the reporting period.
            if hire_date < pd.Timestamp("2026-04-01") and rng.random() < 0.12:
                earliest_exit = max(
                    hire_date + pd.Timedelta(days=90),
                    pd.Timestamp("2025-01-01"),
                )
                latest_exit = pd.Timestamp("2026-12-31")

                if earliest_exit <= latest_exit:
                    available_days = (latest_exit - earliest_exit).days
                    termination_date = earliest_exit + pd.Timedelta(
                        days=int(rng.integers(0, available_days + 1))
                    )

            rows.append(
                {
                    "EmployeeKey": employee_key,
                    "EmployeeCode": f"EMP-{employee_key:04d}",
                    "JobRole": role,
                    "Department": department,
                    "HomeLocationKey": location_key,
                    "HireDate": hire_date.date(),
                    "TerminationDate": (
                        termination_date.date()
                        if pd.notna(termination_date)
                        else None
                    ),
                    "EmploymentType": employment_type,
                    "StandardHourlyRate": round(
                        float(rng.uniform(wage_min, wage_max)), 2
                    ),
                    "IsActive": pd.isna(termination_date),
                }
            )

            employee_key += 1

    return pd.DataFrame(rows)



if __name__ == "__main__":
    main()
