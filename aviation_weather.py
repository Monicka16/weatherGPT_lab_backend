import os

import requests

from dotenv import load_dotenv
load_dotenv()


AVIATION_API_BASE = os.environ.get("AVIATION_API_BASE")

if not AVIATION_API_BASE:
    raise RuntimeError(
        "AVIATION_API_BASE is missing from environment variables."
    )


def fetch_metar(icao: str):
    """Fetch the latest METAR for an ICAO airport code."""

    icao = icao.strip().upper()

    if len(icao) != 4:
        raise ValueError("ICAO code must contain exactly 4 characters.")

    url = f"{AVIATION_API_BASE}/metar"

    response = requests.get(
        url,
        params={
            "ids": icao,
            "format": "json",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return data[0]
