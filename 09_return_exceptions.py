import asyncio as aio

async def f(delay):
    await aio.sleep(1/delay)
    return delay

loop = aio.get_event_loop()

for i in range(10):
    loop.create_task(f(i))

pending = aio.all_tasks(loop) 

group = aio.gather(*pending, return_exceptions=True)

results = loop.run_until_complete(group)

print(f"Results: {results}")

loop.close()
