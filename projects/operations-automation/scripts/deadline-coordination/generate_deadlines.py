
from pathlib import Path
from datetime import date, timedelta
import argparse
import random
import pandas as pd

# Module 2 — Meridian Deadline Coordination
# Independent synthetic data generator

MODULE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODULE_DIR.parents[1]

OUTPUT_DIR = PROJECT_DIR / "data" / "deadline-coordination"

RANDOM_SEED = 42
SAMPLE_RECORDS = 20

DEFAULT_REPORT_DATE = date(2026, 11, 6)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Meridian deadline coordination test data."
    )

    parser.add_argument(
        "--report-date",
        type=date.fromisoformat,
        default=DEFAULT_REPORT_DATE,
        help="Reporting date in YYYY-MM-DD format."
    )

    return parser.parse_args()

def generate_sample(report_date):
    # Days remaining for each of our 20 test records.
    # Negative values represent overdue deadlines.
    day_offsets = [
        -5, -2, -1,       # Overdue: 3
        0, 0,             # Due Today: 2
        1, 1, 2,          # Immediate: 3
        3, 3, 4, 5,       # Approaching: 4
        6, 7, 10, 14, 21, # On Track: 5
        None, None, None  # Undetermined: 3
    ]

    records = []

    for i, offset in enumerate(day_offsets, start=1):
        work_order_id = f"WO-{i:05d}"

        due_date = (
            report_date + timedelta(days=offset)
            if offset is not None
            else None
        )

        records.append({
            "WorkOrderID": work_order_id,
            "PropertyID": f"PROP-{((i - 1) % 24) + 1:03d}",
            "Priority": "High" if i % 4 == 0 else "Normal",
            "DueDate": due_date.isoformat() if due_date else "",
            "AssignedTo": f"TECH-{((i - 1) % 12) + 1:03d}",
            "InternalStatus": "Open"
        })

    return pd.DataFrame(records)

def generate_source_exports(master, report_date):
    # Controlled source membership.
    external_ids = set(master.iloc[:17]["WorkOrderID"])
    internal_ids = set(master.iloc[:15]["WorkOrderID"])
    internal_ids.update(master.iloc[17:]["WorkOrderID"])

    external = master[
        master["WorkOrderID"].isin(external_ids)
    ][["WorkOrderID", "PropertyID", "Priority", "DueDate"]].copy()

    internal = master[
        master["WorkOrderID"].isin(internal_ids)
    ][["WorkOrderID", "AssignedTo", "DueDate", "InternalStatus"]].copy()

    external = external.rename(
        columns={"DueDate": "ExternalDueDate"}
    )
    internal = internal.rename(
        columns={"DueDate": "InternalDueDate"}
    )

    # Simulate disagreements between the two systems.
    # Both dates remain valid; neither is automatically corrected.
    conflicts = {
        "WO-00002": 3,
        "WO-00007": -2,
        "WO-00014": -4
    }

    for work_order_id, adjustment in conflicts.items():
        mask = internal["WorkOrderID"] == work_order_id

        original = internal.loc[mask, "InternalDueDate"].iloc[0]
        adjusted = (
            date.fromisoformat(original)
            + timedelta(days=adjustment)
        )

        internal.loc[mask, "InternalDueDate"] = adjusted.isoformat()

    # Both exports independently represent open work orders.
    external["LastUpdated"] = report_date.isoformat()
    internal["LastUpdated"] = report_date.isoformat()

    external = external[
        ["WorkOrderID", "PropertyID", "Priority",
         "ExternalDueDate", "LastUpdated"]
    ]

    internal = internal[
        ["WorkOrderID", "AssignedTo", "InternalDueDate",
         "LastUpdated", "InternalStatus"]
    ]

    return external, internal

def classify_deadline(days_remaining):
    if pd.isna(days_remaining):
        return "Undetermined"
    if days_remaining < 0:
        return "Overdue"
    if days_remaining == 0:
        return "Due Today"
    if days_remaining <= 2:
        return "Immediate"
    if days_remaining <= 5:
        return "Approaching"
    return "On Track"


def calculate_expected(external, internal, report_date):
    expected = external.merge(
        internal,
        on="WorkOrderID",
        how="outer",
        indicator=True,
        validate="one_to_one"
    )

    expected["ReconciliationStatus"] = expected["_merge"].map({
        "both": "Matched",
        "left_only": "External Only",
        "right_only": "Internal Only"
    }).astype(str)

    expected = expected.drop(columns=["_merge"])

    # Both exports contain LastUpdated.
    expected = expected.rename(columns={
        "LastUpdated_x": "ExternalLastUpdated",
        "LastUpdated_y": "InternalLastUpdated"
    })

    external_dates = pd.to_datetime(
        expected["ExternalDueDate"], errors="coerce"
    )
    internal_dates = pd.to_datetime(
        expected["InternalDueDate"], errors="coerce"
    )

    expected["MonitoringDeadline"] = pd.concat(
        [external_dates, internal_dates], axis=1
    ).min(axis=1)

    expected["DaysRemaining"] = (
        expected["MonitoringDeadline"]
        - pd.Timestamp(report_date)
    ).dt.days

    expected["DeadlineStatus"] = expected[
        "DaysRemaining"
    ].apply(classify_deadline)

    expected["ConflictFlag"] = (
        external_dates.notna()
        & internal_dates.notna()
        & external_dates.ne(internal_dates)
    )


    # A missing deadline is a blank or invalid date in a
    # source where the work order actually exists.
    external_present = expected["ReconciliationStatus"].isin(
        ["Matched", "External Only"]
    )
    internal_present = expected["ReconciliationStatus"].isin(
        ["Matched", "Internal Only"]
    )

    expected["MissingDeadlineFlag"] = (
        (external_present & external_dates.isna())
        | (internal_present & internal_dates.isna())
    )

    expected["UnmatchedFlag"] = (
        expected["ReconciliationStatus"] != "Matched"
    )

    expected["IncludeInQueue"] = (
        expected["DaysRemaining"].le(5).fillna(False)
        | expected["ConflictFlag"]
        | expected["MissingDeadlineFlag"]
        | expected["UnmatchedFlag"]
    )

    priority = {
        "Overdue": 1,
        "Due Today": 2,
        "Immediate": 3,
        "Approaching": 4,
        "On Track": 5,
        "Undetermined": 6
    }

    expected["QueuePriority"] = expected[
        "DeadlineStatus"
    ].map(priority)

    expected = expected.sort_values(
        ["QueuePriority", "MonitoringDeadline", "WorkOrderID"],
        na_position="last"
    )

    expected["MonitoringDeadline"] = (
        expected["MonitoringDeadline"].dt.strftime("%Y-%m-%d")
    )

    return expected

def main():
    args = parse_arguments()
    random.seed(RANDOM_SEED)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Meridian Deadline Coordination")
    print(f"Report date: {args.report_date}")
    print(f"Sample records: {SAMPLE_RECORDS}")
    print(f"Output directory: {OUTPUT_DIR}")

    sample = generate_sample(args.report_date)

    print("\nSample deadline distribution:")
    print(sample[["WorkOrderID", "DueDate"]].to_string(index=False))

    external, internal = generate_source_exports(
        sample, args.report_date
    )

    external.to_csv(
        OUTPUT_DIR / "External_Deadlines.csv", index=False
    )
    internal.to_csv(
        OUTPUT_DIR / "Internal_Deadlines.csv", index=False
    )

    print("\nSource export counts:")
    print(f"External open: {len(external)}")
    print(f"Internal open: {len(internal)}")
    print(f"Unique active: {len(set(external['WorkOrderID']) | set(internal['WorkOrderID']))}")

    expected = calculate_expected(
        external, internal, args.report_date
    )

    expected.to_csv(
        OUTPUT_DIR / "Expected_Deadlines.csv",
        index=False
    )

    print("\nExpected deadline classifications:")
    print(
        expected["DeadlineStatus"]
        .value_counts()
        .to_string()
    )

    print(f"\nDeadline conflicts: {expected['ConflictFlag'].sum()}")
    print(f"Unmatched records: {expected['UnmatchedFlag'].sum()}")
    print(f"Action queue records: {expected['IncludeInQueue'].sum()}")

if __name__ == "__main__":
    main()
