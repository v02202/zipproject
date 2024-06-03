from tempfile import NamedTemporaryFile
import zipfile, os, base64
from ..modules import aws, token
from ..auth import auth
from .allmodels import upload, files
from settings import database, constance
from starlette.config import Config
from starlette.exceptions import HTTPException
from sqlalchemy import select, and_, func, exc
from cryptography.fernet import Fernet
config = Config(".env")
bucket = config("AWS_S3_BUCKET", cast=str, default="")
encrypt_key = str.encode(config("ENCRYPT_KEY", cast=str))
auth_int = auth.BasicAuth()

def encodeFiles(origin_path, new_path):
    with zipfile.ZipFile(origin_path, 'r') as origin_path:
        with zipfile.ZipFile(new_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_path:
            for file_info in origin_path.infolist():
                with origin_path.open(file_info.filename) as file:
                    file_data = file.read()
                    encoded_data = base64.b64encode(file_data).decode('utf-8')
                    new_path.writestr(file_info.filename, encoded_data)

def decodeZip(encoded_path, decoded_path):
    with zipfile.ZipFile(encoded_path, 'r') as encoded_path:
        for file_info in encoded_path.infolist():
            with encoded_path.open(file_info.filename) as file:
                encoded_data = file.read().decode('utf-8')
                decoded_data = base64.b64decode(encoded_data)
                output_file_path = os.path.join(decoded_path, file_info.filename)
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)

async def uploadZip(upload_file, users_id):
    file_size = upload_file.size
    # Check file size
    if upload_file.size > 50000000:
        query = upload.insert().values(
            filename = upload_file.filename,
            upload_by = users_id,
            is_check = False,
            file_size = file_size
        )
        try:
            await database.CONNECTION.execute(query)
        except:
            raise HTTPException(status_code=500, detail='SQL error')
        error_message = "Size is too big"
        return False, error_message
    

    # Save uploaded file
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await upload_file.read())
        tmp_path = tmp.name
    print("tmp_path: ", tmp_path)

    # Validate ZIP
    with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
        required_files = {"A.txt", "B.txt"}
        zip_content = set(zip_ref.namelist())
        print("zip_content: ", zip_content)
        if not required_files.issubset(zip_content):
            query = upload.insert().values(
                filename = upload_file.filename,
                upload_by = users_id,
                is_check = False,
                file_size = file_size
            )
            try:
                await database.CONNECTION.execute(query)
            except:
                raise HTTPException(status_code=500, detail='SQL error')
            os.remove(tmp_path)
            error_message = "A.txt and B.txt are neccessary."
            return False, error_message
        
    new_path = tmp_path + ".encoded.zip"
    encodeFiles(tmp_path, new_path)

    # upload to AWS
    s3_path = f'upload/{os.path.basename(tmp_path)}'
    aws.s3_client.upload_file(new_path, bucket, s3_path)
    os.remove(tmp_path)

    query = upload.insert().values(
        filename = upload_file.filename,
        upload_by = users_id,
        is_check = True,
        file_size = file_size,
        storage_path = s3_path
    ).returning(upload.c.upload_id)
    try:
        upload_id = await database.CONNECTION.execute(query)
    except:
        raise HTTPException(status_code=500, detail='SQL error')

    insert_list = [
        {
            "filename":a,
            "upload_id":upload_id,
            "file_type":"txt"
        }
        for a in zip_content if not a.startswith('__MACOSX')
    ]
    print("insert_list: ",insert_list)
    insert_stmt = files.insert().values(insert_list)
    await database.CONNECTION.execute(insert_stmt)

    res = {
        "upload_id": upload_id,
        "filename": upload_file.filename,
        "storage_path": s3_path
    }
    return True, res


    
    