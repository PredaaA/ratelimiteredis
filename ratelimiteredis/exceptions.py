class RateLimiterException(Exception):
    """Base exception of ratelimiter-redis package."""


class RedisConnectionFail(RateLimiterException):
    """Raised when connecting to the Redis DB failed."""


class RedisMissingConnection(RateLimiterException):
    """Raise when ratelimiter-redis is not connected to Redis."""
