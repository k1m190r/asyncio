import asyncio as aio
from asyncio import StreamReader, StreamWriter

async def send_event(msg: str):
    await aio.sleep(1)


async def echo(reader: StreamReader, writer: StreamWriter):
    print("new connection...")
    try:
        while data := await reader.readline():
            writer.write(data.upper())
            await writer.drain()
        print("connection done.")
    except aio.CancelledError:
        msg = "connection dropped ..."
        print(msg)

        # sending message ...
        # this will be missed by the aio.run() cleanup
        aio.create_task(send_event(msg))


async def main(host="127.0.0.1", port=9999):
    server = await aio.start_server(echo, host, port)
    async with server:
        print(server)
        await server.serve_forever()


try:
    aio.run(main())
except KeyboardInterrupt:
    print("bye, bye.")
