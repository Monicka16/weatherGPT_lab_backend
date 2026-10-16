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

    # Handle empty API responses
    if not response.text or not response.text.strip():
        logger.warning(f"Empty METAR response for {icao}")
        return None

    # Handle invalid JSON responses
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        logger.warning(f"Invalid JSON returned for METAR {icao}")
        return None
    except ValueError:
        logger.warning(f"Could not parse METAR response for {icao}")
        return None

    # Handle missing or unexpected data
    if not isinstance(data, list) or not data:
        logger.info(f"No METAR data available for {icao}")
        return None

    return data[0]