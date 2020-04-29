import asyncio as aio

async def f(x): # coro
    await aio.sleep(0.1)
    return x + 100

async def factory(n): # async generator
    for x in range(n):
        await aio.sleep(0.1)
        yield f, x

async def main():
    res = [await f(x) async for f, x in factory(3)]
    print("res: ", res)

aio.run(main())
