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

def validate_dimensions(
    dates: pd.DataFrame,
    locations: pd.DataFrame,
    products: pd.DataFrame,
) -> None:
    """Validate foundational dimension integrity."""

    if len(dates) != 730:
        raise ValueError("Unexpected calendar row count.")

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

    print("Dimension validation passed.")


def main() -> None:
    """Generate, validate, and export dimensions."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    dates = generate_dates()
    locations = generate_locations()
    products = generate_products()

    validate_dimensions(dates, locations, products)

    dates.to_csv(OUTPUT_DIR / "DimDate.csv", index=False)
    locations.to_csv(OUTPUT_DIR / "DimLocation.csv", index=False)
    products.to_csv(OUTPUT_DIR / "DimProduct.csv", index=False)
    
    print(f"DimDate: {len(dates):,} records")
    print(f"DimLocation: {len(locations):,} records")
    print(f"DimProduct: {len(products):,} records")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()