import random
import time
from typing import Tuple
import requests

use_cached_data = False

measured_latency_in_sec = [
    0.28844,
    0.334_694,
    0.33468,
    0.343_911,
    0.339_515,
    0.344_329,
    0.341_594,
    0.352_366,
    0.535_646,
    0.527_148,
    0.533_472,
    0.53351,
    0.523_462,
]


def get_lat_long(zip_code: str, country: str) -> Tuple[float, float]:
    key = f"{zip_code}, {country}"
    url = (
        f'http://www.datasciencetoolkit.org/street2coordinates/{key.replace(" ", "+")}'
    )

    if use_cached_data:
        time.sleep(random.choice(measured_latency_in_sec))
        return 45.50655, -122.733_888
    else:
        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()

        city_data = data.get(f"{zip_code}, {country}", dict())
        return city_data.get("latitude", 0.00), city_data.get("longitude", 0.00)
