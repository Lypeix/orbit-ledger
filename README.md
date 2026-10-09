# OrbitLedger

ETL pipeline for NASA/JPL close-approach data, focused on reliable ingestion, validation, and transformation. Currently crawling

## Documentation

- [Roadmap](docs/ROADMAP.md)
- [Development log](docs/DEVLOG.md)

## Run

From the repository root, fetch and save a capture:

```powershell
.\.venv\Scripts\python.exe -m orbit_ledger.client
```

Responses and request metadata are saved in `data/raw/`.

To read a saved response without contacting JPL, replace `CAPTURE_ID` with its filename:

```powershell
.\.venv\Scripts\python.exe -m orbit_ledger.client --replay "data/raw/CAPTURE_ID.json"
```

## Tests

Run the offline tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```