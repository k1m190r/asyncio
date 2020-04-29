import asyncio as aio

async def f(delay):
    await aio.sleep(delay)


loop = aio.get_event_loop()

t1 = loop.create_task(f(1))
t2 = loop.create_task(f(2))

loop.run_until_complete(t1)

loop.close() # will fail since t2 is still pending
