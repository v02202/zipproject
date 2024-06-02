from starlette.exceptions import HTTPException
from ..responses.responses import (
    success, successWithData,
    error4221, error406, error4062
)
from starlette.config import Config
from pydantic import ValidationError
from ..models import (
    apikey
)
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)
secret_key = config("JWT_SECRET_KEY", cast=str, default='')

async def storeAPIkey(request):
    data = await request.json()
    try:
        args = apikey.CheckStoreAPIkey(**data)
    except ValidationError as e:
        return error4221(e.errors())
    store = await apikey.storeAPIkey(args)
    if store == False:
        raise HTTPException(status_code=500, detail='SQL error')
    elif store == 'existed':
        error_message = 'existed_api_name'
        return error4062(error_message)
    else:
        res = {"api_key": store}
        return successWithData(res)   

async def getApiToken(request):
    data = await request.json()
    try:
        args = apikey.CheckGetApiToken(**data)
    except ValidationError as e:
        return error4221(e.errors())
    res = await apikey.getApiToken(args)
    if res == 'invalid':
        return error406()
    else:
        return successWithData(res)