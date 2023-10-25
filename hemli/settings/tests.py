from . import *

REDIS_URL = "redis://127.0.0.1:6379/9"
CACHES['default']['LOCATION'] = REDIS_URL


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "hemli.shrtnr": {
            "level": "DEBUG",
        },
    },
}
