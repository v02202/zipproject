from starlette.routing import Route, Mount
from source.controllers import (
    apikey
)

routes=[
    Route("/store", endpoint=apikey.storeAPIkey,
        methods=["POST"], name="storeAPIkey"),
    Route("/token", endpoint=apikey.getApiToken,
        methods=["POST"], name="getApiToken"),
]