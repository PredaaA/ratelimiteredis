import asyncio
from ratelimiteredis import RedisInterface, RateLimit


async def get_interface():
    r = RedisInterface()
    await r.init_connection()
    return r


class Test:
    async def run(self):
        interface = await get_interface()
        while True:
            try:
                ratelimiter = RateLimit(interface)
                await ratelimiter.set(rate="60/m", key="John", value="Doe")
                # You can choose by how many you want to increment by adding incrby.
                # Example to increment by 50:
                # await ratelimiter.set(rate="60/m", key="John", value="Doe", incrby=50)

                ratelimit = await ratelimiter.get(rate="60/m", key="John", value="Doe")
                print(ratelimit)
            except KeyboardInterrupt:
                await interface.teardown()
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
