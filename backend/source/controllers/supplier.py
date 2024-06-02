from ..models import supplier
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


async def createSupplier(request):
    data = await request.json()
    try:
        args = supplier.CheckCreateSupplier(**data)
    except ValidationError as e:
        return error4221(e.errors())
    res = await supplier.createSupplier(args)
    if res == False:
        raise HTTPException(status_code=500, detail=STATUS['5000'])
    else:
        return successWithData(res)

@requires("authenticated", status_code=401)   
async def getSupplier(request):
    supplier_id = int(request.path_params["supplier_id"])
    res = await supplier.getSupplier(supplier_id)
    return successWithData(res)