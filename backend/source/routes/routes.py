from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from . import (
    users,
    supplier,
    apikey,
    upload
)

async def homepage(request):
    return PlainTextResponse('Homepage')

routes = [
    Route('/', homepage), # just for test
    Mount('/api/users', routes=users.routes),
    Mount('/api/supplier', routes=supplier.routes),
    Mount('/api/apikey', routes=apikey.routes),
    Mount('/api/upload', routes=upload.routes),
]