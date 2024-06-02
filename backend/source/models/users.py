from pydantic import BaseModel, Field
from sqlalchemy.sql import text
from sqlalchemy import select, and_, func, exc
from settings import database, constance
from ..auth import auth
from ..modules import token
from .allmodels import (
    users
)

auth_ins = auth.BasicAuth()
class CheckCreateUsers(BaseModel):
    email: str = Field(max_length=228)
    password: str = Field(max_length=228)
    supplier_id: int

class CheckUsers(BaseModel):
    email: str = Field(max_length=228)
    password: str = Field(max_length=228)

async def createUser(args):
    # check exist
    exist_query = text(
        "SELECT EXISTS(SELECT 1 FROM users WHERE email = :x) "
    ).bindparams(
        x=auth_ins.do_encrypt(args.email)
    )
    exist = await database.CONNECTION.execute(exist_query)
    if exist:
        return 'user already exists'

    query = users.insert().values(
        email = auth_ins.do_encrypt(args.email),
        password = args.password,
        supplier_id = args.supplier_id
    ).returning(users.c.users_id)
    
    try:
        user_oid = await database.CONNECTION.execute(query)
    except:
        return False
    encode = dict()
    encode["user_oid"] = user_oid
    encode["expires"] = constance.EXPIRES
    acs_token, rfs_token = token.generateToken(**encode)
    res = {
        "acs_token": acs_token,
        "rfs_token": rfs_token
    }

    return res


async def loginUser(args):
    
    exist_query = (
        select(users.c.users_id).where(
        and_(
            users.c.email == auth_ins.do_encrypt(args.email),
            users.c.password == args.password,
        ))
    )
    records = await database.CONNECTION.fetch_one(exist_query)
    if not records:
        return 'email or password wrong'
    user_info = dict(records)
    user_info['expires'] = constance.EXPIRES
    
    acs_token, rfs_token = token.generateToken(**user_info)
    res = {
        "acs_token": acs_token,
        "rfs_token": rfs_token
    }

    return res


