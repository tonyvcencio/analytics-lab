
"""Generate synthetic work orders for Meridian QA auditing."""

import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


SEED = 640
TOTAL_WORK_ORDERS = 500

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "documentation-qa"

CATEGORIES = [
    "Plumbing",
    "Electrical",
    "HVAC",
    "General Maintenance",
    "Safety",
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
TECHNICIANS = [f"TECH-{i:03d}" for i in range(1, 16)]


def generate_work_orders(seed: int = SEED) -> pd.DataFrame:
    """Generate reproducible synthetic work orders."""
    rng = random.Random(seed)
    records = []

    for number in range(1, TOTAL_WORK_ORDERS + 1):
        work_order_id = f"WO-QA-{number:05d}"

        category = rng.choice(CATEGORIES)
        priority = rng.choices(
            PRIORITIES,
            weights=[25, 45, 25, 5],
            k=1,
        )[0]

        # Ensure the audit population includes October closures.
        if number <= 300:
            completion_date = date(2026, 10, 1) + timedelta(
                days=rng.randrange(31)
            )
            status = "Closed"
        else:
            completion_date = date(2026, 9, 1) + timedelta(
                days=rng.randrange(61)
            )
            status = rng.choice(["Closed", "Open"])

        open_date = completion_date - timedelta(
            days=rng.randint(1, 14)
        )

        completed_at = (
            f"{completion_date.isoformat()}T15:00:00"
            if status == "Closed"
            else ""
        )


        records.append(
            {
                "WorkOrderID": work_order_id,
                "PropertyID": f"PROP-{rng.randint(1, 30):03d}",
                "Category": category,
                "Priority": priority,
                "AssignedTo": rng.choice(TECHNICIANS),
                "OpenDate": open_date.isoformat(),
                "CompletionDate": (
                    completion_date.isoformat()
                    if status == "Closed"
                    else ""
                ),
                "CompletedAt": completed_at,
                "Status": status,
                "ResolutionCode": rng.choice(
                    ["Repaired", "Replaced", "Inspected"]
                ),
            }
        )

    return pd.DataFrame(records)


def generate_work_order_notes(
    work_orders: pd.DataFrame,
    seed: int = SEED,
) -> pd.DataFrame:
    """Generate synthetic notes with controlled QA deficiencies."""
    from datetime import datetime, time

    rng = random.Random(seed + 1)
    records = []
    note_number = 1

    for order in work_orders.to_dict("records"):
        work_order_id = order["WorkOrderID"]
        open_date = date.fromisoformat(order["OpenDate"])

        # Every work order receives an initial progress note.
        records.append({
            "NoteID": f"NOTE-{note_number:06d}",
            "WorkOrderID": work_order_id,
            "NoteType": "Progress",
            "NoteText": "Initial work order assessment completed.",
            "CreatedAt": datetime.combine(
                open_date, time(9, 0)
            ).isoformat(timespec="seconds"),
        })
        note_number += 1

        if order["Status"] != "Closed":
            continue

        completion_date = date.fromisoformat(
            order["CompletionDate"]
        )
        
        completion_time = datetime.fromisoformat(
            order["CompletedAt"]
        )


        # Controlled deficiency scenarios.
        scenario = rng.choices(
            ["Normal", "Missing", "Late", "Duplicate"],
            weights=[70, 10, 12, 8],
            k=1,
        )[0]

        if scenario == "Missing":
            continue

        created_at = completion_time + timedelta(
            hours=30 if scenario == "Late" else 2
        )

        note_text = (
            f"Work completed. Resolution: {order['ResolutionCode']}."
        )

        records.append({
            "NoteID": f"NOTE-{note_number:06d}",
            "WorkOrderID": work_order_id,
            "NoteType": "Completion",
            "NoteText": note_text,
            "CreatedAt": created_at.isoformat(timespec="seconds"),
        })
        note_number += 1

        if scenario == "Duplicate":
            records.append({
                "NoteID": f"NOTE-{note_number:06d}",
                "WorkOrderID": work_order_id,
                "NoteType": "Completion",
                "NoteText": note_text,
                "CreatedAt": created_at.isoformat(timespec="seconds"),
            })
            note_number += 1

    return pd.DataFrame(records)

def generate_work_order_attachments(
    work_orders: pd.DataFrame,
    seed: int = SEED,
) -> pd.DataFrame:
    """Generate synthetic attachments with controlled deficiencies."""
    from datetime import datetime

    rng = random.Random(seed + 2)
    records = []
    attachment_number = 1

    for order in work_orders.to_dict("records"):
        if order["Status"] != "Closed":
            continue

        completed_at = datetime.fromisoformat(
            order["CompletedAt"]
        )

        # Most closed work orders have completion photographs.
        if rng.random() < 0.85:
            records.append({
                "AttachmentID": f"ATT-{attachment_number:06d}",
                "WorkOrderID": order["WorkOrderID"],
                "AttachmentType": "CompletionPhoto",
                "UploadedAt": (
                    completed_at + timedelta(hours=1)
                ).isoformat(timespec="seconds"),
            })
            attachment_number += 1

        # Safety work orders require an additional checklist.
        if order["Category"] == "Safety" and rng.random() < 0.80:
            records.append({
                "AttachmentID": f"ATT-{attachment_number:06d}",
                "WorkOrderID": order["WorkOrderID"],
                "AttachmentType": "SafetyChecklist",
                "UploadedAt": (
                    completed_at + timedelta(hours=2)
                ).isoformat(timespec="seconds"),
            })
            attachment_number += 1

        # Optional supporting documentation.
        if rng.random() < 0.30:
            records.append({
                "AttachmentID": f"ATT-{attachment_number:06d}",
                "WorkOrderID": order["WorkOrderID"],
                "AttachmentType": "InspectionReport",
                "UploadedAt": (
                    completed_at + timedelta(hours=3)
                ).isoformat(timespec="seconds"),
            })
            attachment_number += 1

    return pd.DataFrame(records)


def generate_qa_reviews(
    work_orders: pd.DataFrame,
    seed: int = SEED,
) -> pd.DataFrame:
    """Generate supervisor approvals and prior deficiency reviews."""
    from datetime import datetime

    rng = random.Random(seed + 3)
    records = []
    review_number = 1

    for order in work_orders.to_dict("records"):
        if order["Status"] != "Closed":
            continue

        completed_at = datetime.fromisoformat(
            order["CompletedAt"]
        )
        work_order_id = order["WorkOrderID"]

        # High and Critical work orders require supervisor approval.
        if order["Priority"] in ("High", "Critical"):
            # Some approvals are deliberately absent.
            if rng.random() < 0.85:
                records.append({
                    "ReviewID": f"REV-{review_number:06d}",
                    "WorkOrderID": work_order_id,
                    "ReviewType": "SupervisorApproval",
                    "ReviewStatus": rng.choices(
                        ["Approved", "Pending"],
                        weights=[90, 10],
                        k=1,
                    )[0],
                    "ReviewedAt": (
                        completed_at + timedelta(hours=4)
                    ).isoformat(timespec="seconds"),
                    "ResolvedAt": "",
                    "ReviewerID": f"SUP-{rng.randint(1, 5):03d}",
                })
                review_number += 1

        # Some orders have a previously identified QA deficiency.
        if rng.random() < 0.20:
            status = rng.choices(
                ["Resolved", "Unresolved"],
                weights=[65, 35],
                k=1,
            )[0]

            reviewed_at = completed_at + timedelta(hours=6)

            records.append({
                "ReviewID": f"REV-{review_number:06d}",
                "WorkOrderID": work_order_id,
                "ReviewType": "DeficiencyFollowUp",
                "ReviewStatus": status,
                "ReviewedAt": reviewed_at.isoformat(
                    timespec="seconds"
                ),
                "ResolvedAt": (
                    (reviewed_at + timedelta(days=2)).isoformat(
                        timespec="seconds"
                    )
                    if status == "Resolved"
                    else ""
                ),
                "ReviewerID": f"QA-{rng.randint(1, 5):03d}",
            })
            review_number += 1

    return pd.DataFrame(records)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Meridian QA synthetic data."
    )
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    work_orders = generate_work_orders(args.seed)
    notes = generate_work_order_notes(work_orders, args.seed)
    reviews = generate_qa_reviews(work_orders, args.seed)
    attachments = generate_work_order_attachments(
    work_orders, args.seed
)

    output_file = OUTPUT_DIR / "WorkOrders.csv"
    work_orders.to_csv(output_file, index=False)

    notes_file = OUTPUT_DIR / "WorkOrderNotes.csv"
    notes.to_csv(notes_file, index=False)

    attachments_file = OUTPUT_DIR / "WorkOrderAttachments.csv"
    attachments.to_csv(attachments_file, index=False)

    reviews_file = OUTPUT_DIR / "QAReviews.csv"
    reviews.to_csv(reviews_file, index=False)

    eligible = work_orders[
        (work_orders["Status"] == "Closed")
        & work_orders["CompletionDate"].between(
            "2026-10-01", "2026-10-31"
        )
    ]

    print("Meridian Documentation & QA Automation")
    print(f"Seed: {args.seed}")
    print(f"Total work orders: {len(work_orders)}")
    print(f"Eligible October closures: {len(eligible)}")
    print(f"Output: {output_file}")
    print(f"Total notes: {len(notes)}")
    print(f"Completion notes: {(notes['NoteType'] == 'Completion').sum()}")
    print(f"Notes output: {notes_file}")
    print(f"Total attachments: {len(attachments)}")
    print(f"Attachments output: {attachments_file}")
    print(f"Total QA reviews: {len(reviews)}")
    print(f"QA Reviews output: {reviews_file}")

if __name__ == "__main__":
    main()
