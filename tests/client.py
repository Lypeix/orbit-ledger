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


def test_successful_capture(isolated_client, monkeypatch, capsys):
    raw_dir = isolated_client
    mock_http_response(monkeypatch, SAMPLE_RESPONSE)
    before = datetime.now(timezone.utc)

    exit_code = client.main()

    assert exit_code == 0
    assert "Count: 1" in capsys.readouterr().out # 'in' to check Count value inside another string

    metadata_files = list(raw_dir.glob("*.metadata.json"))
    assert len(metadata_files) == 1

    metadata = json.loads(metadata_files[0].read_text(encoding="utf-8"))
    response_path = raw_dir / metadata["response_file"]

    assert response_path.read_bytes() == SAMPLE_RESPONSE
    assert len(list(raw_dir.iterdir())) == 2

    assert metadata["status_code"] == 200
    assert metadata["request_params"]["date-min"] == "2025-01-01"
    assert metadata["request_params"]["date-max"] == "2025-02-01"
    assert metadata["request_params"]["body"] == "Earth"
    assert metadata["request_params"]["dist-max"] == "0.05"

    retrieved_at = datetime.fromisoformat(metadata["retrieved_at_utc"]) # converts the timestamp inside metadata file from str into a Python datetime object
    assert before <= retrieved_at <= datetime.now(timezone.utc) # ensures the converted timestamp falls between the start of main() and current time


@pytest.mark.parametrize(
    ("failure", "expected_message"),
    [
        ("http", "HTTP 503"),
        ("timeout", "Request timed out"),
        ("json", "invalid JSON")
    ],
)
def test_failed_fetch(
    isolated_client,
    monkeypatch,
    capsys,
    failure,
    expected_message
):
    raw_dir = isolated_client

    if failure == "timeout":
        def fake_get(*args, **kwargs):
            raise httpx.ReadTimeout("Simulated timeout")

        monkeypatch.setattr(client.httpx, "get", fake_get)

    elif failure == "http":
        mock_http_response(monkeypatch, b"Unavailable", status_code=503)

    elif failure == "json":
        mock_http_response(monkeypatch, b"This isnt JSON")

    exit_code = client.main()

    assert exit_code == 1
    assert expected_message in capsys.readouterr().err

    assert not list(raw_dir.glob("*.json"))