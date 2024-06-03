from starlette.authentication import requires
from starlette.exceptions import HTTPException
from ..responses.responses import (
    success, successWithData,
    error4221, error406, error4033,
    error4001, error4063, responseWithBytes
)
from ..models import files



@requires("authenticated", status_code=401)
async def getFiles(request):
    user_id = request.user.display_name['users_id']
    upload_id = int(request.path_params["upload_id"])
    code, res = await files.getFiles(user_id, upload_id)
    if code == False:
        return error4063(res)
    return successWithData(res)


@requires("authenticated", status_code=401)
async def readFiles(request):
    files_id = int(request.path_params["files_id"])
    code, res = await files.readFiles(files_id)
    if code == False:
        return error4063(res)
    return responseWithBytes(res)

