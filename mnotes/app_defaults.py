import os.path

from mapawish.settings import BASE_DIR


def default_avatar_path():
    return os.path.join(BASE_DIR, "mnotes/avt.jpg")


default_location = {
        "lat": 56.8315958,
        "lng": 60.6076281
}
