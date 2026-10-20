# ROADMAP

Bulletpoints are not final and are bound to be changed.

## Phase 1 

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
- [x] Test successful capture with mocked HTTP
- [x] Test HTTP failure, timeout and invalid JSON
- [x] Test an empty response
- [x] Verify saved data can be read back correctly

### Finish
- [x] Add the command for running the capture to `README.md`
- [x] Run tests

Phase 2 version

Database Setup
- [ ] Add PostgreSQL to compose.yaml
- [ ] Configure database credentials through environment variables
- [ ] Create .env.example
- [ ] Install psycopg[binary]
- [ ] Create database.py with a connection function
- [ ] Verify the application can connect to PostgreSQL

Parse Saved Data
- [ ] Create parser.py
- [ ] Match response values to names from the fields list
- [ ] Check required fields and row lengths
- [ ] Convert numeric strings into appropriate Python types
- [ ] Preserve unknown diameters as None
- [ ] Preserve source times as TDB and retrieval times as UTC
- [ ] Handle a valid empty capture
- [ ] Reject malformed records with an error identifying the problem

Database Tables
- [ ] Create a SQL schema file
- [ ] Create captures table for capture ID, request parameters and retrieval time
- [ ] Create approaches table for parsed records
- [ ] Link each approach to its source capture
- [ ] Add primary keys, foreign keys and appropriate constraints
- [ ] Apply the schema to PostgreSQL

Load a Capture
- [ ] Create loader.py
- [ ] Read a saved response and its matching metadata file
- [ ] Parse and validate the complete capture before inserting
- [ ] Insert capture metadata and approach records in one transaction
- [ ] Roll back all inserts if loading fails
- [ ] Skip an already-loaded capture ID without duplicating rows
- [ ] Record valid empty captures successfully
- [ ] Add a command for loading a saved capture
- [ ] Print the number of records loaded or indicate that the capture was already loaded

Testing
- [ ] Test field mapping when source columns appear in a different order
- [ ] Test numeric conversion and missing diameters
- [ ] Test malformed rows and missing required fields
- [ ] Test empty captures
- [ ] Configure an isolated PostgreSQL test database
- [ ] Test successful loading and verify stored values
- [ ] Test loading the same capture twice
- [ ] Test rollback after an insert failure

Finish
- [ ] Load the January 2025 capture
- [ ] Query the stored records using SQL
- [ ] Verify the database record count matches the parsed capture
- [ ] Add database setup and loading commands to README.md
- [ ] Run tests
