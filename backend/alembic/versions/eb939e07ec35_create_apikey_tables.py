"""create apikey tables

Revision ID: eb939e07ec35
Revises: bb958d47f52d
Create Date: 2024-06-01 16:19:26.627278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision: str = 'eb939e07ec35'
down_revision: Union[str, None] = 'bb958d47f52d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "apikey",
        sqlalchemy.Column("apikey_id", sqlalchemy.Integer, primary_key=True, comment='api金鑰流水號'),
        sqlalchemy.Column("api_key", sqlalchemy.VARCHAR(12), nullable=True, comment='api金鑰'),
        sqlalchemy.Column("api_name", sqlalchemy.VARCHAR(10), nullable=True, comment='服務名稱'),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), comment='建立時間'),
        sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now(), comment='更新時間'),
    )


def downgrade() -> None:
    op.drop_table("apikey")
