from aiohttp import web
from db_service import DbService
from uuid import UUID
from datetime import datetime

routes = web.RouteTableDef()
app = web.Application()

LIMIT = 500
DB_LITERAL = 'db'
DUMMY_UUID = UUID(int=0)
REQUEST_LOG = 'IP {} requested {} with query {}'

# https://docs.aiohttp.org/en/stable/web_quickstart.html#


@routes.get('/')
async def _():
    return web.json_response({'comment': 'OK'})


@routes.get('/get_lectures')
async def _(request):
    return await get_multiple(request, app[DB_LITERAL].get_lectures)


@routes.get('/get_lecture')
async def _(request):
    return await get_one(request, app[DB_LITERAL].get_lecture)


@routes.get('/delete_lecture')
async def _(request):
    return await get_one(request, app[DB_LITERAL].delete_lecture)


@routes.get('/get_lecturers')
async def _(request):
    return await get_multiple(request, app[DB_LITERAL].get_lecturers)


@routes.get('/get_lecturer')
async def _(request):
    return await get_one(request, app[DB_LITERAL].get_lecturer)


@routes.get('/delete_lecturer')
async def _(request):
    return await get_one(request, app[DB_LITERAL].delete_lecturer)


@routes.get('/get_semesters')
async def _(request):
    return await get_multiple(request, app[DB_LITERAL].get_semesters)


@routes.get('/get_semester')
async def _(request):
    return await get_one(request, app[DB_LITERAL].get_semester)


@routes.get('/delete_semester')
async def _(request):
    return await get_one(request, app[DB_LITERAL].delete_semester)


@routes.get('/get_syllabuses')
async def _(request):
    return await get_multiple(request, app[DB_LITERAL].get_syllabuses)


@routes.get('/get_syllabus')
async def _(request):
    return await get_one(request, app[DB_LITERAL].get_syllabus)


@routes.get('/delete_syllabus')
async def _(request):
    return await get_one(request, app[DB_LITERAL].delete_syllabus)


@routes.get('/get_lectures_content')
async def _(request):
    return await get_multiple(request, app[DB_LITERAL].get_lectures_content)


@routes.get('/get_lecture_content')
async def _(request):
    return await get_one(request, app[DB_LITERAL].get_lecture_content)


@routes.get('/delete_lecture_content')
async def _(request):
    return await get_one(request, app[DB_LITERAL].delete_lecture_content)


async def app_factory():
    db = DbService()
    await db.initialize()
    app.add_routes(routes)
    app[DB_LITERAL] = db
    return app


async def get_multiple(request, function):
    try:
        await log(REQUEST_LOG.format(request.remote, request.rel_url.path, request.rel_url.query))
        offset = int(request.rel_url.query.get('offset', 0))
        array = await function(offset, LIMIT)
        json = [a.model_dump_json() for a in array]
        return web.json_response(json)
    except Exception:
        return web.json_response({'error': 'invalid offset'})


async def get_one(request, function):
    try:
        await log(REQUEST_LOG.format(request.remote, request.rel_url.path, request.rel_url.query))
        uuid = UUID(request.rel_url.query.get('id', DUMMY_UUID.hex))
        row = await function(uuid)
        return web.json_response(text=row.model_dump_json())
    except Exception:
        return web.json_response({'error': 'invalid id'})


async def log(message: str):
    print(f'[{datetime.now()}]: {message}')

if __name__ == '__main__':
    web.run_app(app_factory(), host='localhost', port=4000)
