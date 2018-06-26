
from sanic import Sanic
from sanic.response import text
from asyncio import sleep

app = Sanic()

@app.route('/')
async def test(request):
    await sleep(5)
    return text("Hello")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)
    