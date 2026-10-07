import json
import sys
from datetime import datetime, timezone

import httpx
import pytest

from orbit_ledger import client

# fake jpl response setup
SAMPLE_RESPONSE = b"""
{
    "count": 1,
    "fields": ["des", "dist", "diameter"],
    "data": [["TEST-OBJECT", "0.01", null]]
}
"""
