from functools import lru_cache
from geopy.geocoders import Nominatim


class GeocodingConnector:
    # Initialisiere einen Cache für Adressen und Koordinaten
    address_cache = {}
    coord_cache = {}

    @classmethod
    def format_input(cls, input_str: str) -> str:
        # Umlaute und andere Sonderzeichen ersetzen
        replacements = {
            'ä': 'a',
            'ö': 'o',
            'ü': 'u',
            'Ä': 'A',
            'Ö': 'O',
            'Ü': 'U',
            'Str.': 'Straße',
            'str.': 'Straße'
        }

        for old, new in replacements.items():
            input_str = input_str.replace(old, new)

        # Erster Buchstabe groß, der Rest klein
        return input_str.capitalize()


    @classmethod
    @lru_cache(maxsize=256)
    def get_coordinates_from_address(cls, country, city, street_name, house_number):
        country = cls.format_input(country)
        city = cls.format_input(city)
        street_name = cls.format_input(street_name)

        # Generiere eine vollständige Adresse aus den übergebenen Argumenten
        address_key = f"{street_name} {house_number}, {city}, {country}"

        # Prüfe, ob die Adresse bereits im Cache ist
        if address_key in cls.address_cache:
            return cls.address_cache[address_key]

        geolocator = Nominatim(user_agent="solar_production_server")
        location = geolocator.geocode(address_key)

        if not location:
            raise ValueError("Adresse konnte nicht in Koordinaten umgewandelt werden")

        coords = (location.latitude, location.longitude)

        # Speichere die Koordinaten im Cache
        cls.address_cache[address_key] = coords

        return coords

    @classmethod
    @lru_cache(maxsize=256)
    def get_address_from_coordinates(cls, latitude, longitude):
        # Generiere einen eindeutigen Schlüssel für diese Koordinaten
        coord_key = f"{latitude},{longitude}"

        # Prüfe, ob die Koordinaten bereits im Cache sind
        if coord_key in cls.coord_cache:
            return cls.coord_cache[coord_key]

        geolocator = Nominatim(user_agent="solar_production_server_reverse")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if not location:
            raise ValueError("Koordinaten konnten nicht in eine Adresse umgewandelt werden")

        address = location.address

        # Speichere die Adresse im Cache
        cls.coord_cache[coord_key] = address

        return address
