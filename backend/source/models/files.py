from sqlalchemy.sql import text
from sqlalchemy import select, and_, func, exc
from starlette.exceptions import HTTPException
from starlette.config import Config
from ..modules import aws
from settings import database, constance
from .upload import decodeZip
import os
config = Config(".env")
bucket = config("AWS_S3_BUCKET", cast=str, default="")
encrypt_key = str.encode(config("ENCRYPT_KEY", cast=str))

from .allmodels import (
    files,
    upload
)



async def getFiles(user_id, upload_id):
    
    query = select(
        upload.c.filename.label('upload_filename'),
        files.c.files_id,
        files.c.filename.label('file_filename'),
    ).join(
        upload, upload.c.upload_id == files.c.upload_id
    ).where(
        and_(
            upload.c.upload_id == upload_id,
            upload.c.upload_by == user_id
        )
    )

    try:
        records = await database.CONNECTION.fetch_all(query)
    except:
        raise HTTPException(status_code=500, detail='SQL error')
    if not records or len(records) == 0:
        return False, 'Invalid user or upload_id'
    
    return True, {"files": [dict(record) for record in records]}


async def readFiles(files_id):

    query = select(
        files.c.filename.label('files_filename'),
        upload.c.filename.label('upload_filename'),
        upload.c.storage_path
    ).join(
        upload, upload.c.upload_id == files.c.upload_id
    ).where(
        files.c.files_id == files_id
    )

    try:
        upload_dict = await database.CONNECTION.fetch_one(query)
    except:
        raise HTTPException(status_code=500, detail='SQL error')
    if not upload_dict:
        return False, "wrong users_id or upload_id"
    
    # Decode file
    encoded_zip_path = "temp.encoded.zip"
    aws.s3_client.download_file(bucket, upload_dict.storage_path, encoded_zip_path)
    
    extract_to = './tmp/decoded_files'
    decodeZip(encoded_zip_path, extract_to)
    os.remove(encoded_zip_path)
    # Return file contents (example for one file)
    file_to_return = os.path.join(extract_to, upload_dict.files_filename)
    with open(file_to_return, "rb") as file:
        content = file.read()

    # Clean up extracted files
    for root, dirs, extracted_files in os.walk(extract_to, topdown=False):
        for name in extracted_files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(extract_to)
    return True, content