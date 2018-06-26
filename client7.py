import asyncio
import aiohttp
import time

ev = asyncio.get_event_loop()

async def make_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/') as resp:
            print(time.strftime("%H:%M:%S"), await resp.text())

async def request_producer():
    while True:
        ev.create_task(make_request())
        await asyncio.sleep(1.0)

ev.create_task(request_producer())
ev.run_forever()