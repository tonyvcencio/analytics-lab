import json
from pathlib import Path

import psycopg


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "observations.jsonl"

CONNECTION = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "health_metrics",
    "user": "health_collector",
}


def ingest_observations():
    """Load JSONL observations into PostgreSQL."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing data file: {DATA_FILE}")

    processed = 0
    inserted = 0

    insert_sql = """
        INSERT INTO public.system_observations (
            timestamp_utc,
            hostname,
            cpu_percent,
            memory_used_mb,
            memory_available_mb,
            disk_used_percent,
            uptime_seconds
        )
        VALUES (
            %(timestamp_utc)s,
            %(hostname)s,
            %(cpu_percent)s,
            %(memory_used_mb)s,
            %(memory_available_mb)s,
            %(disk_used_percent)s,
            %(uptime_seconds)s
        )
        ON CONFLICT (hostname, timestamp_utc) DO NOTHING
    """

    with psycopg.connect(**CONNECTION) as conn:
        with conn.cursor() as cur:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    if not line.strip():
                        continue

                    try:
                        observation = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(
                            f"Invalid JSON on line {line_number}"
                        ) from exc

                    cur.execute(insert_sql, observation)

                    processed += 1
                    inserted += cur.rowcount

    print(f"Observations processed: {processed}")
    print(f"New records inserted: {inserted}")
    print(f"Duplicates skipped: {processed - inserted}")


if __name__ == "__main__":
    ingest_observations()
