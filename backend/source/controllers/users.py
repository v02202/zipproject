from math import ceil
# from ..models import users
from starlette.exceptions import HTTPException
from ..responses.responses import (
    success, successWithData,
    error4221, error406, error4033,
    error4001, error4063
)
from starlette.authentication import requires
# from starlette_core.paginator import Paginator
from starlette.config import Config
from pydantic import ValidationError
from settings.response import STATUS
import jwt
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)
secret_key = config("JWT_SECRET_KEY", cast=str, default='')
# from settings.constants import (
#     PER_PAGE,
#     USER_ALLOW_ADD_USER,
#     USER_ALLOW_EDIT_USER_SKILL,
#     USER_ALLOW_VIEW_USER_SKILL
# )


# async def createDevelopUser(request):
#     data = await request.json()
#     try:
#         args = users.CheckCreateUsers(**data)
#     except ValidationError as e:
#         return error4221(e.errors())
#     res = await users.createUser(args)
#     if res == False:
#         raise HTTPException(status_code=500, detail=STATUS['5000'])
#     elif res == 'user already exists':
#         return error4063(res)
#     else:
#         return successWithData(res)

@requires("authenticated", status_code=401)
async def createUser(request):
    # created_by = request.user.display_name['user_oid']
    # if request.user.display_name['user_role'] not in USER_ALLOW_ADD_USER:
    #     return error406()
    # data = await request.json()
    # try:
    #     args = users.CheckCreateUsers(**data)
    # except ValidationError as e:
    #     return error4221(e.errors())
    # res = await users.createUser(args, created_by)
    # if res == False:
    #     raise HTTPException(status_code=500, detail=STATUS['5000'])
    # elif res == 'user already exists':
    #     return error4063(res)
    # else:
    res = {"test"}
    return successWithData(res)