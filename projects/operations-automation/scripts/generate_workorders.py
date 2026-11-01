
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import random

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "data" / "samples"

# Fixed values make our tests reproducible
REPORT_DATE = date(2026, 10, 31)
TOTAL_RECORDS = 20

# Full-scale Meridian simulation
RANDOM_SEED = 42
MONTHLY_WORK_ORDERS = 1100
PROPERTY_COUNT = 24
REGIONS = ("North", "Central", "South")

FULL_OUTPUT_DIR = PROJECT_DIR / "data" / "daily-exports"

# Generate historical requests so older unresolved orders
# can appear in the reporting-date backlog.
SIMULATION_START = date(2026, 7, 1)
SIMULATION_END = REPORT_DATE


def generate_sample():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records = []

    for i in range(1, TOTAL_RECORDS + 1):
        work_order_id = f"WO-{i:05d}"
        created_date = REPORT_DATE - timedelta(days=i + 1)

        records.append({
            "WorkOrderID": work_order_id,
            "CreatedDate": created_date.isoformat(),
            "PropertyID": f"PROP-{((i - 1) % 24) + 1:03d}",
            "RequestType": "General Maintenance",
            "Priority": "Normal",
            "DueDate": (
                created_date + timedelta(days=10)
            ).isoformat(),
            "AssignedTo": f"TECH-{((i - 1) % 12) + 1:03d}",
            "Region": ["North", "Central", "South"][(i - 1) % 3],
        })

    master = pd.DataFrame(records)

    # Controlled source populations
    external_ids = set(master.iloc[:15]["WorkOrderID"])  # 1–15
    internal_ids = set(master.iloc[:12]["WorkOrderID"])   # 1–12
    internal_ids.update(master.iloc[15:18]["WorkOrderID"])  # 16–18

    external_columns = [
        "WorkOrderID", "CreatedDate", "PropertyID",
        "RequestType", "Priority", "DueDate"
    ]

    internal_columns = [
        "WorkOrderID", "CreatedDate", "AssignedTo",
        "Region", "DueDate"
    ]

    external = master[
        master["WorkOrderID"].isin(external_ids)
    ][external_columns]

    internal = master[
        master["WorkOrderID"].isin(internal_ids)
    ][internal_columns]

    expected = master.copy()
    expected["ExternalOpen"] = expected["WorkOrderID"].isin(external_ids)
    expected["InternalOpen"] = expected["WorkOrderID"].isin(internal_ids)

    expected["IncludeInAging"] = (
        expected["ExternalOpen"] | expected["InternalOpen"]
    )
   
    expected["AgeDays"] = (
        pd.Timestamp(REPORT_DATE)
    - pd.to_datetime(expected["CreatedDate"])
).dt.days

    expected["Classification"] = expected.apply(
        lambda row: (
            "Matched"
            if row["ExternalOpen"] and row["InternalOpen"]
            else "External Only"
            if row["ExternalOpen"]
            else "Internal Only"
            if row["InternalOpen"]
            else "Excluded"
        ),
        axis=1,
    )

    external.to_csv(OUTPUT_DIR / "External_Open.csv", index=False)
    internal.to_csv(OUTPUT_DIR / "Internal_Open.csv", index=False)
    expected.to_csv(
        OUTPUT_DIR / "Expected_Reconciliation.csv", index=False
    )

    print("Sample generation complete.")
    print(f"External open: {len(external)}")
    print(f"Internal open: {len(internal)}")
    print(f"Unique active: {expected['IncludeInAging'].sum()}")
    print(f"Excluded: {(~expected['IncludeInAging']).sum()}")


def generate_full():
    """Generate Meridian's synthetic work-order lifecycle and daily exports."""
    rng = random.Random(RANDOM_SEED)
    FULL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    current_date = SIMULATION_START
    order_number = 1

    while current_date <= SIMULATION_END:
        # Approximately 1,100 new work orders per 30-day month.
        daily_count = max(
            0, round(rng.gauss(MONTHLY_WORK_ORDERS / 30, 7))
        )

        for _ in range(daily_count):
            work_order_id = f"WO-{order_number:06d}"
            property_number = rng.randint(1, PROPERTY_COUNT)
            property_id = f"PROP-{property_number:03d}"

            # Every property belongs to one consistent region.
            region = REGIONS[(property_number - 1) % len(REGIONS)]

            request_type = rng.choice([
                "Preventive Maintenance",
                "Electrical",
                "Plumbing",
                "HVAC",
                "General Repair",
                "Inspection",
            ])

            priority = rng.choices(
                ["Low", "Normal", "High", "Emergency"],
                weights=[15, 55, 25, 5],
                k=1,
            )[0]

            # Most requests resolve quickly, but some take weeks.
            resolution_days = rng.choices(
                [2, 5, 10, 20, 45, 75],
                weights=[20, 30, 25, 15, 7, 3],
                k=1,
            )[0]

            # Independent resolution dates simulate system differences.
            external_resolution = (
                current_date
                + timedelta(days=resolution_days)
            )

            internal_resolution = (
                external_resolution
                + timedelta(days=rng.choices(
                    [-3, -1, 0, 1, 3, 7],
                    weights=[5, 10, 55, 15, 10, 5],
                    k=1,
                )[0])
            )

            # Neither system can resolve before the order exists.
            internal_resolution = max(
                current_date, internal_resolution
            )

            due_days = {
                "Low": 21,
                "Normal": 14,
                "High": 7,
                "Emergency": 1,
            }[priority]

            records.append({
                "WorkOrderID": work_order_id,
                "CreatedDate": current_date.isoformat(),
                "PropertyID": property_id,
                "RequestType": request_type,
                "Priority": priority,
                "DueDate": (
                    current_date + timedelta(days=due_days)
                ).isoformat(),
                "AssignedTo": f"TECH-{rng.randint(1, 24):03d}",
                "Region": region,
                "ExternalResolutionDate": external_resolution.isoformat(),
                "InternalResolutionDate": internal_resolution.isoformat(),
            })

            order_number += 1

        current_date += timedelta(days=1)

    master = pd.DataFrame(records)

    # A work order is open until its resolution date.
    external_open = (
        pd.to_datetime(master["ExternalResolutionDate"]).dt.date
        > REPORT_DATE
    )

    internal_open = (
        pd.to_datetime(master["InternalResolutionDate"]).dt.date
        > REPORT_DATE
    )

    external_columns = [
        "WorkOrderID", "CreatedDate", "PropertyID",
        "RequestType", "Priority", "DueDate",
    ]

    internal_columns = [
        "WorkOrderID", "CreatedDate", "AssignedTo",
        "Region", "DueDate",
    ]

    external = master.loc[external_open, external_columns]
    internal = master.loc[internal_open, internal_columns]

    expected = master.copy()
    expected["ExternalOpen"] = external_open
    expected["InternalOpen"] = internal_open
    expected["IncludeInAging"] = external_open | internal_open

    expected["AgeDays"] = (
        pd.Timestamp(REPORT_DATE)
        - pd.to_datetime(expected["CreatedDate"])
    ).dt.days

    expected["Classification"] = [
        "Matched" if a and b else
        "External Only" if a else
        "Internal Only" if b else
        "Excluded"
        for a, b in zip(external_open, internal_open)
    ]

    external.to_csv(
        FULL_OUTPUT_DIR / "External_Open.csv", index=False
    )
    internal.to_csv(
        FULL_OUTPUT_DIR / "Internal_Open.csv", index=False
    )
    expected.to_csv(
        FULL_OUTPUT_DIR / "Expected_Reconciliation.csv", index=False
    )

    print("\nFull Meridian simulation complete.")
    print(f"Total historical work orders: {len(master):,}")
    print(f"External open: {len(external):,}")
    print(f"Internal open: {len(internal):,}")
    print(f"Unique active: {int(expected['IncludeInAging'].sum()):,}")
    print(
        "Source discrepancies:",
        int((external_open != internal_open).sum()),
    )

if __name__ == "__main__":
    generate_sample()
    generate_full()
