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


@pytest.fixture
def isolated_client(monkeypatch, tmp_path):
    raw_dir = tmp_path / "raw"

    monkeypatch.setattr(client, "RAW_DIR", raw_dir)

    monkeypatch.setattr(sys, "argv", ["orbit-ledger"])

    def unexpected_request(*args, **kwargs):
        pytest.fail("Unexpected HTTP request during test")

    monkeypatch.setattr(client.httpx, "get", unexpected_request)

    return raw_dir


def mock_http_response(monkeypatch, body, status_code=200):
    def fake_get(url, **kwargs):
        request = httpx.Request(
            "GET",
            url,
            params=kwargs.get("params"),
            headers=kwargs.get("headers")
        )

        return httpx.Response(
            status_code=status_code,
            content=body,
            request=request
        )

    monkeypatch.setattr(client.httpx, "get", fake_get)
