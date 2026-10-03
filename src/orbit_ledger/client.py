import sys
import httpx
import argparse
import json

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def fetch_close_approaches() -> dict:
    url = "https://ssd-api.jpl.nasa.gov/cad.api"

    params = {
        "date-min": "2025-01-01",
        "date-max": "2025-02-01",
        "body": "Earth",
        "neo": "true",
        "dist-max": "0.05",
        "diameter": "true"
    }

    headers = {"User-Agent": "orbit-ledger/0.1 (https://github.com/Lypeix/orbit-ledger)"}

    response = httpx.get(
        url, 
        params=params,
        headers=headers,
        timeout=10.0
        )

    response.raise_for_status()
    return response.json()


def save_capture(
    response: httpx.Response,
    retrieved_at: datetime,
) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    capture_id = uuid4().hex # generates random id
    response_path = RAW_DIR / f"{capture_id}.json"
    metadata_path = RAW_DIR / f"{capture_id}.metadata.json"

    metadata = {
        "capture_id": capture_id,
        "retrieved_at_utc": retrieved_at.isoformat(),
        "request_url": str(response.request.url),
        "request_params": str(response.request.url.params),
        "status_code": response.status_code,
        "response_file": response_path.name
    }

    with response_path.open("xb") as file:
        file.write(response.content)

    with metadata_path.open("x", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    return response_path


def load_capture(path: Path) -> dict:
    with path.open("rb") as file:
        return json.load(file)


def main() -> int:
    try: 
        data = fetch_close_approaches()

    except httpx.TimeoutException:
        print("Request timed out", file=sys.stderr)
        return 1 

    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        print(f"JPL returned HTTP {status}", file=sys.stderr)
        return 1 

    except httpx.RequestError as error:
        print(f"Request failed: {error}", file=sys.stderr)
        return 1

    print("Count:", data["count"])

    if data["count"] == 0:
        print("No close approaches fitted the filter")
        return 0

    print("Fields:", data["fields"])
    print("First row:", data["data"][0])

    return 0

if __name__ == "__main__":
    raise SystemExit(main())