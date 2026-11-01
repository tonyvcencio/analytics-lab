
from pathlib import Path
import duckdb

# Locate the database relative to this repository.
project_root = Path(__file__).resolve().parent.parent
database_path = project_root / "data" / "hopper_lab.duckdb"

if not database_path.is_file():
    raise FileNotFoundError(f"Database not found: {database_path}")

con = duckdb.connect(str(database_path), read_only=True)

try:
    result = con.execute("""
        SELECT
            department,
            SUM(cases) AS total_cases
        FROM department_cases
        GROUP BY department
        ORDER BY total_cases DESC
    """).fetchdf()

    print(result)
finally:
    con.close()
