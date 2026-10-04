import sys
import httpx
import argparse
import json

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def fetch_close_approaches() -> httpx.Response:
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
    return response


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
        "request_params": dict(response.request.url.params),
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


def print_summary(data: dict) -> None:
    print("Count:", data["count"])

    if data["count"] == 0:
        print("No close approaches fitted the filter")
        return

    print("Fields:", data["fields"])
    print("First row:", data["data"][0])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch or replay JPL close approach data"
    )
    parser.add_argument(
        "--replay",
        type=Path,
        help="Read a saved response rather than making an API request"
    )
    args = parser.parse_args()

    try:
        if args.replay is not None:
            data = load_capture(args.replay)
            print(f"Loaded: {args.replay}")
        else:
            response = fetch_close_approaches()
            retrieved_at = datetime.now(timezone.utc)

            data = response.json()

            saved_path = save_capture(response, retrieved_at)
            print(f"Saved: {saved_path}")

        print_summary(data)
        return 0

    except httpx.TimeoutException:
        print("Request timed out", file=sys.stderr) # tells human what failed
        return 1 # tells the computer it failed

    except httpx.HTTPStatusError as error:
        print(
            f"JPL returned HTTP {error.response.status_code}",
            file=sys.stderr
        )
        return 1

    except httpx.RequestError as error:
        print(
            f"The request has failed: {error}", file=sys.stderr
        )
        return 1

    except json.JSONDecodeError:
        print(
            f"The API response or saved file contains invalid JSON"
        )
        return 1

    except OSError as error:
        print(f"File operation failed: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())