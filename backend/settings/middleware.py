from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from source.auth import auth
from starlette_jwt import JWTAuthenticationBackend
from starlette_auth_toolkit.backends import MultiAuth
from starlette.responses import  Response
from starlette.requests import Request
from starlette.config import Config
# from .base import settings
# from logs.middleware import OpentraceMiddleware, LoggingMiddleware, TimedOutMiddleware, HandleRequestStateMiddleware
config = Config(".env")
secret_key = config("JWT_SECRET_KEY", cast=str, default='')

# def log_opentracing(request: Request, response: Response):
    
#     status_code = response.status_code
#     span, scope = getattr(request.state, 'opentracing_span', None), getattr(request.state, 'opentracing_scope', None)

#     if span == None or scope == None:
#         return

#     if 600 > status_code >= 500: # error code 5XX
#         span.set_tag('error', True)
#     span.set_tag('status_code', status_code)
#     scope.close()



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
    # Middleware(OpentraceMiddleware), #open_trace
    # Middleware(HandleRequestStateMiddleware), # Request state
    # Middleware(LoggingMiddleware), # Logging
    # Middleware(TimedOutMiddleware, request_timeout_seconds=settings.request_timeout_seconds), # Timeout
]
