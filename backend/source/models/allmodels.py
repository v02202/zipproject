from enum import unique
import sqlalchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import select, func, and_, or_, Integer, Column, String, DATE, inspect, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
metadata = sqlalchemy.MetaData()
# Base = declarative_base()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("users_id", sqlalchemy.Integer, primary_key=True, comment='使用者流水號'),
    sqlalchemy.Column("email", sqlalchemy.VARCHAR(228), nullable=True, comment='使用者信箱', unique=True),
    sqlalchemy.Column("password", sqlalchemy.VARCHAR(228), nullable=True, comment='使用者密碼'),
    sqlalchemy.Column("supplier_id", 
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('supplier.supplier_id', ondelete='CASCADE'), 
        nullable=True, 
        comment='供應商流水號',
        index=True
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
)

supplier = sqlalchemy.Table(
    "supplier",
    metadata,
    sqlalchemy.Column("supplier_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='供應商流水號'),
    sqlalchemy.Column("supplier_name", sqlalchemy.VARCHAR(228), nullable=True, comment='供應商名稱'),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
)

upload = sqlalchemy.Table(
    "upload",
    metadata,
    sqlalchemy.Column("upload_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='上傳流水號'),
    sqlalchemy.Column("upload_sid", sqlalchemy.VARCHAR(10), nullable=True, comment='上傳唯一碼'),
    sqlalchemy.Column("filename", sqlalchemy.Text, nullable=True, comment='上傳檔名稱'),
    sqlalchemy.Column("storage_path", sqlalchemy.Text, nullable=True, comment='存放位置'),
    sqlalchemy.Column("upload_by", 
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('users.users_id', ondelete='CASCADE'), 
        nullable=True, 
        comment='上傳者流水號',
        index=True
    ),
    sqlalchemy.Column("is_check", sqlalchemy.Boolean, nullable=True, comment='是否有誤'),
    sqlalchemy.Column("file_size", sqlalchemy.Integer, nullable=True, comment='檔案大小'),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
)

files = sqlalchemy.Table(
    "files",
    metadata,
    sqlalchemy.Column("files_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='檔案流水號'),
    sqlalchemy.Column("filename", sqlalchemy.Text, nullable=True, comment='檔案名稱'),
    sqlalchemy.Column("upload_id", 
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey('upload.upload_id', ondelete='CASCADE'), 
        nullable=True, 
        comment='上傳流水號',
        index=True
    ),
    sqlalchemy.Column("file_size", sqlalchemy.Integer, nullable=True, comment='檔案大小'),
    sqlalchemy.Column("file_type", sqlalchemy.VARCHAR(10), nullable=True, comment='檔案類型'),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
)

apikey = sqlalchemy.Table(
    "apikey",
    metadata,
    sqlalchemy.Column("apikey_id", sqlalchemy.Integer, primary_key=True, comment='api金鑰流水號'),
    sqlalchemy.Column("api_key", sqlalchemy.VARCHAR(12), nullable=True, comment='api金鑰'),
    sqlalchemy.Column("api_name", sqlalchemy.VARCHAR(10), nullable=True, comment='服務名稱'),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
)