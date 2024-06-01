"""create tables

Revision ID: bb958d47f52d
Revises: 
Create Date: 2024-06-01 14:49:01.143529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision: str = 'bb958d47f52d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "supplier",
        sqlalchemy.Column("supplier_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='供應商流水號'),
        sqlalchemy.Column("supplier_name", sqlalchemy.VARCHAR(228), nullable=True, comment='供應商名稱'),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
    )
    op.create_table_comment('supplier', '供應商表')

    op.create_table(
        "users",
        sqlalchemy.Column("users_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='使用者流水號'),
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
    op.create_table_comment('users', '使用者表')

    op.create_table(
        "upload",
        sqlalchemy.Column("upload_id", sqlalchemy.Integer, autoincrement=True, primary_key=True, comment='上傳流水號'),
        sqlalchemy.Column("upload_sid", sqlalchemy.VARCHAR(10), nullable=True, comment='上傳唯一碼'),
        sqlalchemy.Column("filename", sqlalchemy.Text, nullable=True, comment='上傳檔名稱'),
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
    op.create_table_comment('upload', '上傳紀錄表')

    op.create_table(
        "files",
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
    op.create_table_comment('files', '檔案紀錄表')


def downgrade():
    op.drop_table('files')
    op.drop_table('upload')
    op.drop_table('users')
    op.drop_table('supplier')
