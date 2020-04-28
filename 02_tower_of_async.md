# Tower of async

1. corouties: `async def`, `async with`, `async for`, `await`
2. event-loop: `*.run()`, `BaseEventLoop`, `uvloop`
	`*.get_event_loop()`, `*.get_running_loop()`
3. futures: `*.Future`
4. tasks: `*.Task`, `*.create_task()`
5. process & threads: `*.run_in_executor()`, `*.subprocess`
6. tools: `*.Queue`
7. net-transport: `BaseTransport`
8. net-tcp-udp: `Protocol`
9. streams: `StreamReader`, `StreamWriter`, 
	`*.open_connection()`,` *.start_server()`
10. aiohttp & aiofiles:` *.ClinetSession`, `*.open()`. Maybe: `gevent`


## Cheatsheets
https://www.pythonsheets.com/notes/python-asyncio.html

## 1. Coroutine

`coroutine` - is an object that encapsulates the ability to resume and unerlying function that has been suspended before completion.

All coroutines will be executed either with `loop.create_task(coro)` or `await coro`.

### `async def(...`
Declares a *coroutine function* that returns *coro*.

### These are executed by the event-loop
- `coro.send(None)` - Start coro.
- `StopIteration` - end of coro.

### `await x` - x is `awaitable` parameter. One of:
- `coroutine` (i.e. resutls of call to `async def(...)` function)
- *Any* object implementing `__await__()` method that must `return` *iterator* (has: `__next__` & `__iter__`).



### Alternatives
`Curio` and `Trio` built on top of coroutines.

## 2. Event Loop
`Curio`, `Trio` have their own. 

`uvloop` is drop in faster replacement from nodejs project.
```python
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# OR

import asyncio
import uvloop
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)
```

## 3 & 4. Futures and Tasks
`Task` is subclass of `Future`. `Future` - represents some sort of ongoing action that will return a result via `notification` on the event loop. `Task` - represents a coro running on the event loop. `Future` is loop-aware, while `Task` is loop- and coro-aware. 

## 5. Processes ans Threads
- `Threads` - blocking non-asyncio-aware code.
- `Processess` - CPU bound work.

## 6. `asyncio.Queue`

## 7..9. Network IO

## 
