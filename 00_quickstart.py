import asyncio
import time

async def main():
    print(f"{time.ctime()}: Start.")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()}: Done.")

loop = asyncio.get_event_loop()
# use *.get_running_loop() inside coro

task = loop.create_task(main())
loop.run_until_complete(task)

pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()

