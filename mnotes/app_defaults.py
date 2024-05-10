import os.path

from mapawish.settings import BASE_DIR


def default_avatar_path():
    return os.path.join(BASE_DIR, "mnotes/avt.jpg")
