from asyncio import sleep
from dataclasses import dataclass
from random import randint
from uuid import uuid4, UUID

import aiohttp_cors
from aiohttp import web
from aiohttp.abc import Application

routes = web.RouteTableDef()

"""
https://docs.aiohttp.org/en/stable/web_quickstart.html#


query = req.match_info.get('query', '')  # for route-resolving, /{query}
query = req.rel_url.query['query']  # params; required; else .get('query','default')
"""


async def blah():
    await sleep(1.3)


@routes.get('/')
async def hello(request):
    await blah()
    return web.json_response({'comment': 'OK'})


@routes.get('/welcome')
async def hello(request):
    return web.json_response({'comment': 'Welcome!'})


@routes.get('/render')
async def render(request):
    # ciężka operacja -- wykorzystująca run_in_executor
    consumers.append(randint(1, 10))
    return web.json_response({'comment': f'Welcome {consumers}!'})


@routes.get('/square')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/square?x=12
    sx: str = request.rel_url.query['x']
    x = int(sx)
    xx = x ** 2
    return web.json_response({'result': xx})

@routes.get('/user')
async def hello(request):
    # odpalanie: http://0.0.0.0:4000/user?name=Radek
    name: str = request.rel_url.query['name']

    user = User(id=randint(1,100), name=name)
    return web.json_response(user.__dict__) # można zwrócić list[dict] etc..



@dataclass
class User:
    id: int
    name: str


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app, port=4000)
