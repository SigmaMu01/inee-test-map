from .debug import *  # noqa: F401,F403


DEBUG = False

ALLOWED_HOSTS = ["localhost", "p01--web--4cqtxswnrj4s.code.run"]

CSRF_TRUSTED_ORIGINS = ["https://p01--web--4cqtxswnrj4s.code.run"]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"  # Allauth constant for prod server
