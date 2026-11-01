
from pathlib import Path
from datetime import date, timedelta
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "data" / "samples"

# Fixed values make our tests reproducible
REPORT_DATE = date(2026, 10, 31)
TOTAL_RECORDS = 20


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

    expected["AgeDays"] = [
        (REPORT_DATE - date.fromisoformat(value)).days
        for value in expected["CreatedDate"]
    ]

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


if __name__ == "__main__":
    generate_sample()
