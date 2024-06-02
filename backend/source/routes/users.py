from starlette.routing import Route, Mount
from source.controllers import (
    users
)

routes=[
    Route('/create', endpoint=users.createUser,
        methods=['POST'], name='createData'),
    Route('/login', endpoint=users.loginUser,
        methods=['POST'], name='loginUser'),
    Route('/refresh/token', endpoint=users.userAccessToken,
        methods=['GET'], name='userAccessToken'),
]