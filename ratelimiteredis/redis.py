import aioredis
from typing import Optional, NoReturn
from .exceptions import RedisConnectionFail, RedisMissingConnection


class RedisPool:
    """Represents an Redis pool.

    Parameters
    ----------
    address: Optional[str] = None
        The Redis address
    host: Optional[str] = "localhost"
        The Redis host. Will be ignored if address is not None.
    port: Optional[int] = 6379
        The Redis port. Will be ignored if address is not None.
    db: Optional[int] = 0
        The Redis db. Will be ignored if address is not None.
    password: Optional[str] = None
        The Redis password.
    encoding: str = "utf-8"
        The encoding used.
    maxsize: int = 50
        The maximum of DBs of that pool.
    """

    __slots__ = ("_address", "_host", "_port", "_db", "_password", "_encoding", "_maxsize")

    def __init__(
        self,
        address: Optional[str] = None,
        host: Optional[str] = "localhost",
        port: Optional[int] = 6379,
        db: Optional[int] = 0,
        password: Optional[str] = None,
        encoding: str = "utf-8",
        maxsize: int = 50,
    ):
        self._address = address
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._encoding = encoding
        self._maxsize = maxsize

    def __repr__(self):
        return f"<RedisPool _address={self._address} _host={self._host} _port={self._port} _db={self._db} _encoding={self._encoding} _maxsize={self._maxsize}>"


class RedisInterface(RedisPool):
    """Represents the Redis interface to proceed ratelimits.

    Parameters
    ----------
    address: Optional[str] = None
        The Redis address
    host: Optional[str] = "localhost"
        The Redis host. Will be ignored if address is not None.
    port: Optional[int] = 6379
        The Redis port. Will be ignored if address is not None.
    db: Optional[int] = 0
        The Redis db. Will be ignored if address is not None.
    password: Optional[str] = None
        The Redis password.
    encoding: str = "utf-8"
        The encoding used.
    maxsize: int = 50
        The maximum of DBs of that pool.
    """

    __slots__ = ("__redis",)

    def __init__(self, **kwargs):
        self.__redis = None
        super().__init__(**kwargs)

    async def init_connection(self) -> None:
        if self._address is None and any(
            (self._host is None, self._port is None, self._db is None)
        ):
            raise RedisConnectionFail(
                "If address argument is not provided, any of host, port, or db must be passed."
            )

        try:
            address = self._address or f"redis://{self._host}:{self._port}"
            self.__redis = await aioredis.create_redis_pool(
                address=address,
                db=self._db if self._address is None else None,
                password=self._password,
                encoding=self._encoding,
                maxsize=self._maxsize,
            )
        except Exception:
            raise RedisConnectionFail(
                "Something went wrong while trying to connect to this Redis DB."
            )

    async def teardown(self) -> None:
        if self.__redis:
            self.__redis.close()

    @property
    def pool(self) -> aioredis.Redis:
        if self.__redis is None:
            raise RedisMissingConnection(
                "You need to have an valid Redis connection to use that property."
            )
        return self.__redis

    @pool.setter
    async def pool(self, val) -> NoReturn:
        raise RuntimeError()


redisinterface = RedisInterface()
