import asyncio
from ratelimiteredis import RedisInterface, RateLimit


async def get_interface():
    r = RedisInterface()
    await r._init_connection()
    return r


class Test:
    async def run(self):
        interface = await get_interface()
        while True:
            try:
                ratelimiter = RateLimit(interface)
                ratelimit = await ratelimiter.get("60/m", "John", "Doe")
                print(ratelimit)
            except KeyboardInterrupt:
                await interface._teardown()
                break
            else:
                await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Test().run())
        loop.close()
    except KeyboardInterrupt:
        pass
