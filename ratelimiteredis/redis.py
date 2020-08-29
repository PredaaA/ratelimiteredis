import aioredis
from typing import NoReturn
from .exceptions import RedisConnectionFail, RedisMissingConnection


class RedisPool:
    """Represent an Redis pool.

    Attributes
    ----------
    host: str = "localhost"
        The Redis host.
    port: int = 6379
        The Redis port.
    db: int = 0
        The Redis db.
    encoding: str = "utf-8"
        The encoding used.
    """

    __slots__ = ("_host", "_port", "_db", "_encoding")

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0, encoding: str = "utf-8"
    ):
        self._host = host
        self._port = port
        self._db = db
        self._encoding = encoding

    def __repr__(self):
        return f"<RedisPool _host={self._host} _port={self._port} _db={self._db} _encoding={self._encoding}>"


class RedisInterface(RedisPool):

    __slots__ = ("_redis",)

    def __init__(self, **kwargs):
        self._redis = None
        super().__init__(**kwargs)

    async def init_connection(self) -> None:
        try:
            self._redis = await aioredis.create_redis_pool(
                address=f"redis://{self._host}:{self._port}",
                db=self._db,
                encoding=self._encoding,
                maxsize=50,
            )
        except Exception:
            raise RedisConnectionFail(
                "Something went wrong while trying to connect to this Redis DB."
            )

    async def teardown(self) -> None:
        if self._redis:
            self._redis.close()

    @property
    def pool(self) -> aioredis.Redis:
        if self._redis is None:
            raise RedisMissingConnection(
                "You need to have an valid Redis connection to use that property."
            )
        return self._redis

    @pool.setter
    async def pool(self, val) -> NoReturn:
        raise RuntimeError()


redisinterface = RedisInterface()
