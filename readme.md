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

### Exceptions
Most common `task.cancel()`. Corotine body `async def(...)` can catch `try: ... ; except asyncio.CancelledError: ...` to do necessary cleanup.

[ex: cancellation](02_cancellation.py)

### `async with` - context managers

```python 
class Connection:
	def __init__(self, host, port):
		self.host = host
		self.port = port

	async def __aenter__(self):
		self.conn = await get_conn(
			self.host, self.port)
		return conn

	async def __aexit__(self):
		await self.conn.close()


async with Connection("localhost", 9001) as conn:
	<do some work with connection>
```

### `conextlib`

Blocking
```python
from contextlib import contextmanager

@contextmanager
def web_page(url):
	try:
		data = download_page(url)
		yield data

	finally:
		update_stats(url)


with web_page('google.com') as data:
	process(data)

```

`asyncio` aware
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def web_page(url):
	try:
		data = await download_webpage(url) # dowload... is now a coro
		yield data

	finally:
		await update_stats(url) # now a coro


async with web_page("google.com") as data:
	process(data)

```

Use `executor` to use blocking `asyncio` UN-aware code.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def web_page(url):
	try:
		loop = asyncio.get_running_loop()
		data = await loop.run_in_executor(
			None, download_webpage, url)
		yield data

	finally:
		await loop.run_in_executor(
			None, update_stats, url)

```

### `async for` async iterators

Traditional non async
```python 
class A:
	def __iter__(self):
		self.x = 0
		return self # return iterator
	
	def __next__(self):
		if self.x > 5:
			raise StopIteration

		else:
			self.x += 1
			return self.x


for i in A():
	print(i)
```

`asyc for` OOP version
```python
import asyncio
from aioredis import create_redis

class OneAtATime:
	def __init__(self, redis, keys):
		self.redis = redis
		self.keys = keys

	def __aiter__(self): # ! regular def NOT async def
		self.ikeys = iter(self.keys)
		return self

	async def __anext__(self):
		try:
			k = next(self.ikeys)

		except StopIteration:
			raise StopAsyncIteration

		value = await redis.get(k)
		return value

async def main():
	redis = await create_redis(("localhost", 6379))
	keys = ["Americas", "Africa", "Europe", "Asia"]

	async for value in OneAtATime(redis, keys):
		await do_something_with_value(value)

await main()

```

### `async` generator
```python
import asyncio as aio
from aioredis import create_redis

# async generator function
# when run returns async generator
async def one_at_a_time(redis, keys):
	for k in keys:
		value = await redis.get(k)
		yield value

async def main():
	redis = await create_redis(("locahost", 6379))
	keys = ["Americas", "Africa", "Europe", "Asia"]

	async for value in one_at_a_time(redis, keys):
		await do_something_with(value)

await main()

```

### `async` list, dict and set comprehension
```python
import asyncio as aio

async def double(n):
	for in range(n):
		yield i, i * 2
		await aio.sleep(0.1)

async def main():
	print( [x async for x in double(3)] )
	print( {x: y async for x, y in double(3)} )
	print( {x async for x in doubble(3)} )

	# this will return async generator so 
	# must use async for to iter over it
	print( (x async for x in doubble(3)) )

await main()
```

### `async` goodies all together
```python
import asyncio as aio

async def f(x): # coro
	await aio.sleep(0.1)
	return x + 100

async def factory(n): # async generator
	for x in range(n):
		await aio.sleep(0.1)
		yield f, x

async def main():
	# factory(3) returns async generator so need async for
	# f(x) returns a coro so need to await it
	res = [await f(x) async for f, x in factory(3)]
	print("res: ", res)

# aio.run(main())
await main()
```

### Start Up and Gracefull Shutdown

#### Startup `main()`
`aio.run(main())` - run `main()` coro.

#### Shutdown
1. `<pending> = aio.all_tasks(loop=loop)` - collect all pending tasks.
2. `for <task> in <pending>: <task>.cancel()` - cancel each task.
	- inside coro catch `aio.CancelledError` and cleanup.
3. `<group> = aio.gather(*<pending>)` - gather completing tasks.
4. `<loop>.run_until_comple(<group>)` - final wait.

#### Rule of thumb:
Don't create tasks in `aio.CancelledError` exception handler.

[ex: hanging pending tasks](06_pending_tasks.py)

[ex: asyncio life cycle](07_asyncio_lifecycle.py)

[ex: asyncio life cycle with pending task](08_asyncio_lifecycle_pending.py)

### `return_exceptions=True` in `aio.gather()`



### **??? Exception handling**

### Alternatives
`Curio` and `Trio` built on top of coroutines.

## 2. Event Loop

`*.get_running_loop()` - recommended, must be run from inside a coro.

`*.get_event_loop()` - discouraged. Works only with the same thread. Or need to `new_event_loop() -> set_event_loop()`


### Alternatives
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

`Curio`, `Trio` have their own. 


## 3 & 4. Futures and Tasks
`Task` is subclass of `Future`.

`Future` is loop-aware, while `Task` is loop- and coro-aware. 

`Future` - represents **_some_** activity that will return a result via `notification` on the event loop.

`Task` - represents specifically **_coroutine_** running on the event loop.

`Future.done()` - is future done?

`*.set_result(value)`

`*.result()` - return value of result

[ex: interaction with future](./04_interaction_with_future.py)

Don't use `*.ensure_future()`.

Only use `*.create_task()`.



## 5. Processes ans Threads
- `Threads` - blocking non-asyncio-aware code.
- `Processess` - CPU bound work.

## 6. `asyncio.Queue`

## 7..9. Network IO

## 
