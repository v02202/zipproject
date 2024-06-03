from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from source.auth import auth
from starlette_jwt import JWTAuthenticationBackend
from starlette_auth_toolkit.backends import MultiAuth
from starlette.responses import  Response
from starlette.requests import Request
from starlette.config import Config
config = Config(".env")
secret_key = config("JWT_SECRET_KEY", cast=str, default='')



middleware = [
    Middleware(AuthenticationMiddleware, 
        backend=MultiAuth(
            [
                auth.BasicAuth(),
                JWTAuthenticationBackend(secret_key=secret_key, prefix='JWT')
            ]
        ), on_error=auth.on_auth_error
    ),
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']),
]
