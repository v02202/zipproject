from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from . import (
    users
)

async def homepage(request):
    return PlainTextResponse('Homepage')

routes = [
    Route('/', homepage), # just for test
    Mount('/api/users', routes=users.routes),
]