import asyncio

async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result("finished")

loop = asyncio.get_event_loop()

# new future
fut = asyncio.Future()
print(fut.done())

loop.create_task(main(fut))

result = loop.run_until_complete(fut) # notice we are waiting for future not task
print(result)

print(fut.done())
