"""
Default constants for this project that are not related
to the project settings.
"""

import os.path

import googlemaps
from mapawish.settings import BASE_DIR, GOOGLE_API_KEY


DEFAULT_LOCATION_CONST = "City Center, Yekaterinburg, Sverdlovsk Oblast, Russia"


def default_avatar_path():
    return os.path.join(BASE_DIR, "mnotes/avt.jpg")


def default_location():
    """Default location for a map center the user sees when creating a new note."""
    gmap = googlemaps.Client(key=GOOGLE_API_KEY)
    map_default = gmap.geocode(DEFAULT_LOCATION_CONST)
    map_geo_cords = list(map_default[0]["geometry"]["location"].values())

    lat = map_geo_cords[0]
    lng = map_geo_cords[1]

    location = {"lat": lat, "lng": lng}
    return location
