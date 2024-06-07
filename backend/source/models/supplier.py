from pydantic import BaseModel, Field
from sqlalchemy.sql import text
from sqlalchemy import select, and_, func, exc
from starlette.exceptions import HTTPException
from settings import database
from ..auth import auth
from .allmodels import (
    supplier
)

class CheckCreateSupplier(BaseModel):
    supplier_name: str = Field(max_length=228)

async def createSupplier(args):
    query = supplier.insert().values(
        supplier_name = args.supplier_name,
    ).returning(supplier.c.supplier_id)
    
    try:
        supplier_id = await database.CONNECTION.execute(query)
    except:
        raise HTTPException(status_code=500, detail='SQL error')
    
    res = {
        "supplier_id": supplier_id
    }

    return res

async def getSupplier(id):
    query = select(supplier.c.supplier_name).where(supplier.c.supplier_id == id)
    try:
        data = await database.CONNECTION.execute(query)
    except:
        raise HTTPException(status_code=500, detail='SQL error')
    return {"supplier_name": data}