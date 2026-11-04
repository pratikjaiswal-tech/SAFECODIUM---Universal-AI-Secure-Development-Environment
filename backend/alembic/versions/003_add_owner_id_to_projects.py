"""003_add_owner_id_to_projects — Safe migration to add owner_id to projects

Revision ID: 003_add_owner_id_to_projects
Revises: 002_add_analysis_jobs
Create Date: 2026-11-04 18:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '003_add_owner_id_to_projects'
down_revision: Union[str, Sequence[str], None] = '002_add_analysis_jobs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('projects')]
    
    # If owner_id is not already present, add it via standard DDL
    if 'owner_id' not in columns:
        op.add_column('projects', sa.Column('owner_id', sa.String(length=36), nullable=True))
        try:
            op.create_index('ix_projects_owner_id', 'projects', ['owner_id'], unique=False)
        except Exception:
            pass


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('projects')]
    if 'owner_id' in columns:
        try:
            op.drop_index('ix_projects_owner_id', table_name='projects')
        except Exception:
            pass
        # Note: SQLite does not support DROP COLUMN in older engines without table rewrite,
        # but modern SQLite 3.35+ supports ALTER TABLE DROP COLUMN
        try:
            op.drop_column('projects', 'owner_id')
        except Exception:
            pass
