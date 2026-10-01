# ROADMAP

## Phase 1 — Project Setup and Source Capture

### Project Setup
- [ ] Create and connect `orbit-ledger` repository
- [ ] Create `README.md`, `DEVLOG.md`, `ROADMAP.md`
- [ ] Create `.gitignore`
- [ ] Create virtual environment
- [ ] Configure `pyproject.toml`
- [ ] Install `httpx` and `pytest`
- [ ] Create `src/orbit_ledger/` package
- [ ] Create `tests/` and `docs/` directories
- [ ] Create ignored `data/raw/` directory

### Understand the Data Source
- [ ] Read JPL Close-Approach API documentation and usage policy
- [ ] Define January 2025 as the first ingestion window
- [ ] Define explicit Earth, NEO and distance filters
- [ ] Request optional diameter information
- [ ] Identify what one source record represents
- [ ] Document required fields, units and nullable values
- [ ] Document the difference between source time in TDB and retrieval time in UTC
- [ ] Record findings in `docs/source-contract.md`

### Source Client
- [ ] Create an HTTP client for the JPL API
- [ ] Configure an application-specific `User-Agent`
- [ ] Add explicit request parameters and timeout
- [ ] Handle unsuccessful HTTP responses
- [ ] Handle invalid JSON responses
- [ ] Check the response API version
- [ ] Recognize valid empty results
- [ ] Keep requests sequential

### Raw Data Capture
- [ ] Fetch January 2025 data
- [ ] Preserve the original response without modifying it
- [ ] Assign a unique capture identifier
- [ ] Save request parameters and retrieval timestamp
- [ ] Calculate and save the response SHA-256 checksum
- [ ] Prevent existing captures from being overwritten
- [ ] Verify the saved response can be opened offline

### Testing
- [ ] Create a small attributed response fixture
- [ ] Test successful response capture using mocked HTTP
- [ ] Test HTTP errors and timeouts
- [ ] Test invalid JSON and unsupported API versions
- [ ] Test valid empty responses
- [ ] Verify saved metadata and checksum
- [ ] Ensure tests make no live API requests

### Finish
- [ ] Document setup and capture instructions in `README.md`
- [ ] Complete `docs/source-contract.md`
- [ ] Record decisions and findings in `DEVLOG.md`
- [ ] Run the test suite
- [ ] Commit phase 1
- [ ] Review the captured data before designing PostgreSQL tables