import asyncio

async def f():
    try:
        while True: await asyncio.sleep(0) # forever
    except asyncio.CancelledError:
        print("cancelled")
    else:
        # would run if ever try is done without exception
        return 111 # this never happens

coro = f()
coro.send(None) # start coro
coro.send(None) # run again
coro.throw(asyncio.CancelledError)
# coro cancelled
# coro spits out StopIteration

