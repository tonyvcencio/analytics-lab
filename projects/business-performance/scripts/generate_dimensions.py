"""
Northstar Home & Tech
Portfolio Project 002 — Business Performance Analytics

Generate foundational synthetic dimension tables.

Initial scope:
    - DimDate
    - DimLocation
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data"

START_DATE = "2025-01-01"
END_DATE = "2026-12-31"


def generate_dates() -> pd.DataFrame:
    """Generate the Northstar calendar dimension."""

    dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
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


def validate_dimensions(
    dates: pd.DataFrame,
    locations: pd.DataFrame,
) -> None:
    """Validate foundational dimension integrity."""

    assert len(dates) == 730, "Unexpected calendar row count."
    assert dates["DateKey"].is_unique, "Duplicate DateKey detected."
    assert dates["FullDate"].is_unique, "Duplicate FullDate detected."

    assert len(locations) == 3, "Unexpected location count."
    assert locations["LocationKey"].is_unique, (
        "Duplicate LocationKey detected."
    )

    print("Dimension validation passed.")


def main() -> None:
    """Generate, validate, and export dimensions."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dates = generate_dates()
    locations = generate_locations()

    validate_dimensions(dates, locations)

    dates.to_csv(OUTPUT_DIR / "DimDate.csv", index=False)
    locations.to_csv(OUTPUT_DIR / "DimLocation.csv", index=False)

    print(f"DimDate: {len(dates):,} records")
    print(f"DimLocation: {len(locations):,} records")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()