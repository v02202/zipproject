from starlette.authentication import requires
from starlette.exceptions import HTTPException
from ..responses.responses import (
    success, successWithData,
    error4221, error406, error4033,
    error4001, error4063, responseWithBytes
)
from ..modules import ratelimit
from ..models import upload


@requires("authenticated", status_code=401)
async def uploadZip(request):
    try:
        ratelimit.rateLimit()
    except:
        error_message = "Rate limit exceeded"
        return error4063(error_message)

    user_id = request.user.display_name['users_id']
    form = await request.form(max_files=1)
    upload_file = form["upload_file"]
    if not upload_file.filename.endswith('.zip'):
        error_message = "Only accept zip file"
        return error4063(error_message)
    res, message = await upload.uploadZip(upload_file, user_id)
    if res == False:
        return error4063(message)
    return successWithData(message)


@requires("authenticated", status_code=401)
async def uploadHistory(request):
    users_id = request.user.display_name['users_id']
    res, message = await upload.uploadHistory(users_id)
    if res == False:
        return error4063(message)
    return successWithData(message)


