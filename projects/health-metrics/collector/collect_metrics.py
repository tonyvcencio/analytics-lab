from datetime import datetime, timezone
import socket
import json
from pathlib import Path

import psutil


def collect_metrics():
    """Collect a system-health observation."""

    observation = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_used_mb": round(psutil.virtual_memory().used / 1_000_000, 2),
        "memory_available_mb": round(psutil.virtual_memory().available / 1_000_000, 2),
        "disk_used_percent": psutil.disk_usage("/").percent,
        "uptime_seconds": int(datetime.now().timestamp() - psutil.boot_time()),
    }

    return observation

def save_observation(observation):
    """Append one observation to a JSON Lines file."""

    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / "data"

    data_dir.mkdir(parents=True, exist_ok=True)

    output_file = data_dir / "observations.jsonl"

    with output_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(observation) + "\n")

    return output_file


if __name__ == "__main__":
    observation = collect_metrics()
    output_file = save_observation(observation)

    print(json.dumps(observation, indent=4))
    print(f"\nObservation saved to: {output_file}")