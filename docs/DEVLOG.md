# DEVLOG

# Day 1 - 1.10.2026
- Planned Out the Project Scope
- Set Up Documentation
- Configured `.gitignore`
- Initialized the Virtual Environment
- Created the directories and package
- Configured `pyproject.toml`
- Updated pip
- Installed `httpx` and `pytest` dependencies

# Day 2 - 2.10.2026
- Created `src/orbit_ledger/client.py`
    - Added fetch_close_approaches() for requesting JPL close-approach data
    - Added January 2025 Earth/NEO query parameters
    - Limited results to approaches within 0.05 AU
    - Requested optional diameter data
    - Added a project-specific User-Agent header
    - Added a 10-second request timeout
    - Added HTTP error handling with raise_for_status()
    - Return parsed JSON response data