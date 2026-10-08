"""Print status from a configured Starship deployment service."""

from __future__ import annotations

import json
import os
from pathlib import Path
from configparser import ConfigParser
from urllib.request import Request, urlopen


def load_endpoint(path: Path = Path("starship.ini")) -> str:
    """Return the configured deployment-service endpoint."""
    if not path.exists():
        raise RuntimeError("ServiceEndpoint not configured.")
    value = ConfigParser()
    value.read_string(path.read_text(encoding="utf-8"))
    endpoint = value.get("service", "endpoint", fallback=None)
    if not isinstance(endpoint, str) or not endpoint.startswith("https://"):
        raise RuntimeError("ServiceEndpoint not configured.")
    return endpoint


def fetch_status(endpoint: str) -> dict[str, object]:
    """Fetch deployment status using the configured service credential."""
    request = Request(
        endpoint,
        data=json.dumps({"application": "starship-deployment-status"}).encode(
            "utf-8"
        ),
        headers={
            "Authorization": f"Bearer {os.environ.get('STARSHIP_API_KEY', '')}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=3) as response:
        return json.load(response)


def main() -> None:
    status = fetch_status(load_endpoint())
    print(f"Deployment: {status.get('deployment', 'unknown')}")
    print(f"Control plane: {status.get('control_plane', 'unknown')}")
    print(f"Release channel: {status.get('release_channel', 'unknown')}")


if __name__ == "__main__":
    main()
