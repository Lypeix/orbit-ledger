# ROADMAP

## Phase 1 — Project Setup and Source Capture

### Project Setup
- [x] Create and connect `orbit-ledger` repository
- [x] Create `README.md`, `DEVLOG.md`, `ROADMAP.md`
- [x] Create `.gitignore`
- [x] Create virtual environment
- [x] Configure `pyproject.toml`
- [x] Install `httpx` and `pytest`
- [x] Create `src/orbit_ledger/` package
- [x] Create `tests/` and `docs/` directories
- [x] Create ignored `data/raw/` directory

### Fetch Data
- [x] Create a function that requests JPL close-approach data
- [x] Set January 2025, Earth, NEO and distance filters; include diameters
- [x] Configure a timeout and the User-Agent required by JPL
- [x] Handle HTTP failures, invalid JSON and valid empty results
- [x] Run one request and inspect the returned fields and values

### Save Data
- [x] Save the original response in `data/raw/`
- [x] Use a unique filename to avoid overwriting previous captures
- [x] Save request parameters and retrieval time alongside the response
- [x] Load the saved response without making another API request

### Testing
- [ ] Test successful capture with mocked HTTP
- [ ] Test HTTP failure, timeout and invalid JSON
- [ ] Test an empty response
- [ ] Verify saved data can be read back correctly

### Finish
- [ ] Add the command for running the capture to `README.md`
- [ ] Run tests
