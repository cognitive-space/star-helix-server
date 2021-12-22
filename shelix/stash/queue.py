from django.conf import settings

import redis


class LogQueue:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = redis.from_url(settings.REDIS_CLIENT_URL)

        return self._client


log_queue = LogQueue()
