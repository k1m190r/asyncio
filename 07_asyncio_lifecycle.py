import asyncio as aio
from asyncio import StreamReader, StreamWriter

async def echo(reader: StreamReader, writer: StreamWriter):
    print("new connection...")
    try:
        while data := await reader.readline():
            print(f"received: {data}")
            writer.write(data.upper())
            await writer.drain()
        print("connection done.")
    except aio.CancelledError:
        print("connection dropped ...")


async def main(host="127.0.0.1", port=9999):
    server = await aio.start_server(echo, host, port)
    async with server:
        print(server)
        await server.serve_forever()


try:
    aio.run(main())
except KeyboardInterrupt:
    print("bye, bye.")
