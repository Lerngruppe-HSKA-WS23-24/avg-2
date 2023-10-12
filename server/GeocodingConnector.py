import time
from geopy.geocoders import Nominatim
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Address:
    country: str
    city: str
    street_name: str
    house_number: str


class GeocodingConnector:

    @classmethod
    @lru_cache(maxsize=512)
    def get_coordinates_from_address(cls, country: str, city: str, street_name: str, house_number: str):
        time.sleep(1)  # Fügt eine Verzögerung von 1 Sekunde zwischen den Anfragen hinzu

        # Generiere eine vollständige Adresse aus den übergebenen Argumenten
        address_key = f"{street_name}, {house_number}, {city}, {country}"

        geolocator = Nominatim(user_agent="solar_production_server")
        location = geolocator.geocode(address_key)

        if not location:
            raise ValueError("Adresse konnte nicht in Koordinaten umgewandelt werden")

        coords = (location.latitude, location.longitude)
        return coords

    @classmethod
    @lru_cache(maxsize=512)
    def get_address_from_coordinates(cls, latitude: float, longitude: float):
        time.sleep(1)  # Fügt eine Verzögerung von 1 Sekunde zwischen den Anfragen hinzu

        geolocator = Nominatim(user_agent="solar_production_server_reverse")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if not location:
            raise ValueError("Koordinaten konnten nicht in eine Adresse umgewandelt werden")

        address = location.address
        return address
