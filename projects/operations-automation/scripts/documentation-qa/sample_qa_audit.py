
"""Select a reproducible sample for Meridian's retrospective QA audit."""

import argparse
from pathlib import Path

import pandas as pd


SEED = 640
SAMPLE_SIZE = 100
AUDIT_START = "2026-10-01"
AUDIT_END = "2026-10-31"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "documentation-qa"


def select_audit_sample(
    work_orders: pd.DataFrame,
    seed: int = SEED,
    sample_size: int = SAMPLE_SIZE,
) -> pd.DataFrame:
    """Sample eligible October closures without replacement."""

    required = {"WorkOrderID", "Status", "CompletionDate"}
    missing = required - set(work_orders.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if work_orders["WorkOrderID"].isna().any():
        raise ValueError("WorkOrderID contains null values")

    if work_orders["WorkOrderID"].duplicated().any():
        raise ValueError("Duplicate WorkOrderIDs detected")

    eligible = work_orders.loc[
        (work_orders["Status"] == "Closed")
        & work_orders["CompletionDate"].between(
            AUDIT_START, AUDIT_END
        )
    ].copy()

    if len(eligible) < sample_size:
        raise ValueError(
            f"Insufficient eligible population: "
            f"{len(eligible)} available, {sample_size} required"
        )

    # Sort before sampling so input row order cannot change
    # the selected work orders.
    eligible = eligible.sort_values("WorkOrderID")

    sample = eligible.sample(
        n=sample_size,
        random_state=seed,
        replace=False,
    )

    return sample.sort_values("WorkOrderID").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a reproducible Meridian QA audit sample."
    )
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--size", type=int, default=SAMPLE_SIZE)
    args = parser.parse_args()

    if args.size < 1:
        parser.error("--size must be at least 1")

    source = DATA_DIR / "WorkOrders.csv"
    output = DATA_DIR / "AuditSample.csv"

    work_orders = pd.read_csv(source, dtype=str).fillna("")

    sample = select_audit_sample(
        work_orders,
        seed=args.seed,
        sample_size=args.size,
    )

    sample.to_csv(output, index=False)

    print("=== MERIDIAN QA AUDIT SAMPLING ===")
    print(f"Seed: {args.seed}")
    print(f"Sample size: {len(sample)}")
    print(f"Unique work orders: {sample['WorkOrderID'].nunique()}")
    print(f"Audit period: {AUDIT_START} through {AUDIT_END}")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
