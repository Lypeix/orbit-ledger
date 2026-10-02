import httpx

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

