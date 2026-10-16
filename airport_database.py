import csv
import io
import logging
import threading
import time

import requests


logger = logging.getLogger(__name__)

AIRPORTS_URL = (
    "https://raw.githubusercontent.com/"
    "davidmegginson/ourairports-data/main/airports.csv"
)

CACHE_TTL_SECONDS = 24 * 60 * 60

# Small fallback for when the dataset cannot be downloaded
FALLBACK_AIRPORTS = [
    {
        "name": "Coimbatore International Airport",
        "city": "Coimbatore",
        "country": "India",
        "iata": "CJB",
        "icao": "VOCB",
    },
    {
        "name": "Chennai International Airport",
        "city": "Chennai",
        "country": "India",
        "iata": "MAA",
        "icao": "VOMM",
    },
    {
        "name": "Kempegowda International Airport",
        "city": "Bengaluru",
        "country": "India",
        "iata": "BLR",
        "icao": "VOBL",
    },
    {
        "name": "Chhatrapati Shivaji Maharaj International Airport",
        "city": "Mumbai",
        "country": "India",
        "iata": "BOM",
        "icao": "VABB",
    },
    {
        "name": "Indira Gandhi International Airport",
        "city": "Delhi",
        "country": "India",
        "iata": "DEL",
        "icao": "VIDP",
    },
]

_airport_cache = []
_last_fetched = 0
_cache_lock = threading.Lock()


def _download_airports():
    """Download and parse airports with scheduled airline service."""
    response = requests.get(AIRPORTS_URL, timeout=20)
    response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))
    airports = []

    for row in reader:
        airport_type = (row.get("type") or "").strip()
        scheduled_service = (
            row.get("scheduled_service") or ""
        ).strip().lower()

        iata = (row.get("iata_code") or "").strip().upper()
        icao = (row.get("icao_code") or "").strip().upper()
        country_code = (row.get("iso_country") or "").strip().upper()

        if country_code != "IN":
            continue

        # Keep useful airports with scheduled service and both codes.
        if (
            airport_type not in {
                "large_airport",
                "medium_airport",
                "small_airport",
            }
            or len(icao) != 4
        ):
            continue

        name = (row.get("name") or "").strip()
        city = (row.get("municipality") or "").strip()
         
        if not name:
            continue

        airports.append({
            "name": name,
            "city": city or name,
            # OurAirports provides ISO country codes, e.g. IN, US, GB.
            "country": "India",
            "iata": iata,
            "icao": icao,
            "_type": airport_type,
        })

    # Prioritize major airports when multiple results match.
    priority = {
        "large_airport": 0,
        "medium_airport": 1,
        "small_airport": 2,
    }

    airports.sort(
        key=lambda airport: (
            priority.get(airport["_type"], 3),
            airport["name"].lower(),
        )
    )

    # Keep the existing public response schema unchanged.
    for airport in airports:
        airport.pop("_type", None)

    if not airports:
        raise ValueError("The airport dataset contained no usable airports.")

    return airports


def get_airports():
    """Return cached airport data, refreshing it every 24 hours."""
    global _airport_cache, _last_fetched

    now = time.monotonic()

    if (
        _airport_cache
        and now - _last_fetched < CACHE_TTL_SECONDS
    ):
        return _airport_cache

    with _cache_lock:
        now = time.monotonic()

        if (
            _airport_cache
            and now - _last_fetched < CACHE_TTL_SECONDS
        ):
            return _airport_cache

        try:
            airports = _download_airports()
            _airport_cache = airports
            _last_fetched = time.monotonic()

            logger.info("Loaded %s airports.", len(airports))
            return _airport_cache

        except (requests.RequestException, ValueError, csv.Error) as exc:
            logger.warning("Could not refresh airport data: %s", exc)

            # Use previously downloaded data if available.
            if _airport_cache:
                return _airport_cache

            # Otherwise, keep basic airport search working.
            return FALLBACK_AIRPORTS
