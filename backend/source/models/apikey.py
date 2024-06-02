from pydantic import BaseModel, Field
from starlette.config import Config
from sqlalchemy.sql import text
from settings import database, constance
from ..auth import auth
from .allmodels import (
    apikey
)
from ..modules import token
import secrets
auth = auth.BasicAuth()
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)


class CheckStoreAPIkey(BaseModel):
    api_name: str = Field(max_length=10)

class CheckGetApiToken(BaseModel):
    api_name: str
    api_key: str

async def storeAPIkey(args):
    generated_key = secrets.token_urlsafe(8)
    check_query = text(
        "SELECT EXISTS(SELECT 1 FROM apikey WHERE api_name = :a) "
    ).bindparams(
        a=args.api_name
    )
    exist = await database.CONNECTION.execute(check_query)
    if exist:
        return 'existed'
    query = apikey.insert().values(
        api_key = generated_key,
        api_name = args.api_name
    ).returning(apikey.c.api_key)
    api_key = await database.CONNECTION.execute(query)
    try:
        api_key = await database.CONNECTION.execute(query)
        return api_key
    except :
        return False

async def getApiToken(args):
    exist_query = text(
        "SELECT EXISTS(SELECT 1 FROM apikey WHERE api_name = :x AND api_key = :y) "
    ).bindparams(
        x=args.api_name,
        y=args.api_key
    )
    exist = await database.CONNECTION.execute(exist_query)
    if exist == False:
        return 'invalid'
    else:
        api_data = dict()
        api_data['expires'] = constance.EXPIRES
        api_data['api_name'] = args.api_name
        acs_token, rfs_token = token.generateToken(**api_data)
        res = {
           "access_token":acs_token,
        }
        return res
