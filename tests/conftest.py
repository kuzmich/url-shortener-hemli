import pytest
from redis import Redis


@pytest.fixture
def redis(settings):
    client: Redis = Redis.from_url(settings.REDIS_URL)
    client.flushdb()
    yield client

    # client.flushdb()
    client.connection_pool.disconnect()
