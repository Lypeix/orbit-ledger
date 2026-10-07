# DEVLOG

# Dev Day 1 - 1.10.2026
- Planned Out the Project Scope
- Set Up Documentation
- Configured `.gitignore`
- Initialized the Virtual Environment
- Created the directories and package
- Configured `pyproject.toml`
- Updated pip
- Installed `httpx` and `pytest` dependencies

# Dev Day 2 - 2.10.2026
- Created `src/orbit_ledger/client.py`
    - Added fetch_close_approaches() for requesting JPL close-approach data
    - Added January 2025 Earth/NEO query parameters
    - Limited results to approaches within 0.05 AU
    - Requested optional diameter data
    - Added a project-specific User-Agent header
    - Added a 10-second request timeout
    - Added HTTP error handling with raise_for_status()
    - Return parsed JSON response data
    - Added main() as the script entry
    - Added handling for timeouts, HTTP errors, general request failures, and invalid JSON

# Dev Day 3 - 3.10.2026
- Inside `src/orbit_ledger/client.py`:
    - Implemented `save_capture()` for capturing raw JPL responses and assigning them unique `filename` + `metadata`
    - Added `load_capture()` for loading the saved JPL responses
    - Moved data inspection from `main()` to its own dedicated `print_summary()`

# Dev Day 4 - 4.10.2026
- Inside `src/orbit_ledger/client.py`:
    - Added `--replay` argument parsing to `main()`
    - Added OSError exception
    - Changed `fetch_close_approaches()` expected return type from `dict` to `httpx.Response`
    - Changed `request_params` return type inside `metadata` from `str` to `dict`
    - Removed `return 0` from `print_summary()` because it expects None

# Dev Day 5 - 7.10.2026
- Inside `tests/client.py`:
    - Set up fake JPL API response
    - Added pytest fixture for: creating temporary test paths and preventing tests from creating real API requests
    - Added helper that replaces future HTTP GET with a fake one