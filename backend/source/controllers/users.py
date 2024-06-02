from math import ceil
from ..models import users
from ..modules import token
from starlette.config import Config
from starlette.exceptions import HTTPException
from ..responses.responses import (
    success, successWithData,
    error4221, error406, error4033,
    error4001, error4063
)
from starlette.authentication import requires
from pydantic import ValidationError
from settings.response import STATUS
import jwt
config = Config(".env")
secret_key = config("JWT_SECRET_KEY", cast=str, default='')



async def createUser(request):
    data = await request.json()
    try:
        args = users.CheckCreateUsers(**data)
    except ValidationError as e:
        return error4221(e.errors())
    res = await users.createUser(args)
    if res == False:
        raise HTTPException(status_code=500, detail=STATUS['5000'])
    elif res == 'user already exists':
        return error4063(res)
    else:
        return successWithData(res)
    
async def loginUser(request):
    data = await request.json()
    try:
        args = users.CheckUsers(**data)
    except ValidationError as e:
        return error4221(e.errors())
    res = await users.loginUser(args)
    if res == False:
        raise HTTPException(status_code=500, detail=STATUS['5000'])
    elif res == 'email or password wrong':
        return error4063(res)
    else:
        return successWithData(res)
    
@requires("authenticated", status_code=401)
async def userAccessToken(request):
    auth = request.headers["authorization"]
    scheme, credentials = auth.split()
    try:
        json = jwt.decode(credentials, secret_key, algorithms=["HS256"])
    except:
        error_message = 'Access token JWT secret is invalid'
        return error4033(error_message)
    print("token: ", json)
    if 'token' not in json:
        print('Invalid refresh token')
        error_message = 'Forbidden'
        return error4033(error_message)
    else:
        if json['token'] != 'refresh-token':
            print('Invalid refresh token')
            error_message = 'Forbidden'
            return error4033(error_message)
    json.pop('expired_time')
    json.pop('token')
    access_token, refresh_token  = token.generateToken(**json)
    res = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return successWithData(res)