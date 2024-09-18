"""Change task_id type to UUID

Revision ID: 3f6d6a6f1659
Revises: 1b97fa90f827
Create Date: 2024-09-17 22:19:35.014942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6d6a6f1659'
down_revision: Union[str, None] = '1b97fa90f827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Explicitly cast the task_id to UUID using the USING clause
    op.execute("""
        ALTER TABLE analysis 
        ALTER COLUMN task_id TYPE UUID 
        USING task_id::uuid
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # Explicitly cast the task_id from UUID back to VARCHAR using the USING clause
    op.execute("""
        ALTER TABLE analysis 
        ALTER COLUMN task_id TYPE VARCHAR 
        USING task_id::text
    """)
    # ### end Alembic commands ###
