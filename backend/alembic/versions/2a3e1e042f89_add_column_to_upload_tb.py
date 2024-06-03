"""add column to upload tb

Revision ID: 2a3e1e042f89
Revises: eb939e07ec35
Create Date: 2024-06-02 13:17:52.984853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '2a3e1e042f89'
down_revision: Union[str, None] = 'eb939e07ec35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "upload",
        sqlalchemy.Column("storage_path", sqlalchemy.Text, nullable=True, comment='存放位置'),
    )


def downgrade():
    op.drop_column("upload", "storage_path")
