import asyncio as aio

async def main():
    while True:
        print("running ...")
        await aio.sleep(1)


loop = aio.get_event_loop()
task = loop.create_task(main())
try:
    loop.run_until_complete(task)
except KeyboardInterrupt:
    print("SIGINT")

tasks = aio.all_tasks(loop)
for t in tasks:
    t.cancel()
group = aio.gather(*tasks, return_exceptions=True)
res = loop.run_until_complete(group)
print(res)
for r in res:
    print(type(r))
loop.close()


