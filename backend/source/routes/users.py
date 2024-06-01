from starlette.routing import Route, Mount
from source.controllers import (
    users
)

routes=[
    Route('/create', endpoint=users.createUser,
        methods=['POST'], name='createData'),
    # Route('/update/{user_oid:int}', endpoint=users.updateUser,
    #     methods=['POST'], name='updateUser'),
    # Route('/login', endpoint=users.loginUser,
    #     methods=['POST'], name='loginUser'),
    # Route('/refresh/token', endpoint=users.refreshToken,
    #     methods=['GET'], name='refreshToken'),
    # Route('/login/auth', endpoint=users.loginAuth,
    #     methods=['POST'], name='loginAuth'),
    # Route('/logout', endpoint=users.logout,
    #     methods=['GET'], name='logout'),
]