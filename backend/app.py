from starlette.applications import Starlette
from starlette.config import Config
from settings import database, middleware
# from source.models.redis import redis_connect
from source.routes import routes
# from source.mq_receive import main
# from logs.middleware import init_jaeger_tracer
# from logs.logger import init_loggers
# from logs.exceptions.exception_handlers import HANDLERS

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)


app = Starlette(
    debug=DEBUG,
    routes=routes.routes,
    middleware=middleware.middleware,
    # exception_handlers=HANDLERS,
    on_startup=[
        database.CONNECTION.connect,
        # init_jaeger_tracer,
        # init_loggers,
        # redis_connect,
        # debugger.initialize_flask_server_debugger_if_needed,
    ],
    on_shutdown=[database.CONNECTION.disconnect],
)
#test5
