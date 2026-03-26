"""add candidate problems and update attempts

Revision ID: 8f0a2e1b3c4d
Revises: 516d5e15a7c9
Create Date: 2026-03-26 10:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8f0a2e1b3c4d'
down_revision: Union[str, None] = '516d5e15a7c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Update AttemptStatus enum (Postgres special case)
    # op.execute is used because ALTER TYPE cannot run in a transaction easily in older PG versions, 
    # but Alembic handles this better with op.execute and autocommit if configured.
    # For simplicity and reliability, we'll try op.execute first.
    op.execute("ALTER TYPE attemptstatus ADD VALUE IF NOT EXISTS 'waiting'")

    # 2. Create candidate_problems table
    op.create_table('candidate_problems',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('attempt_id', sa.UUID(), nullable=False),
        sa.Column('problem_id', sa.String(length=10), nullable=False),
        sa.Column('status', sa.Enum('assigned', 'started', 'submitted', name='problemstatus'), nullable=False),
        sa.Column('submitted_code', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=20), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('passed_cases', sa.Integer(), nullable=True),
        sa.Column('total_cases', sa.Integer(), nullable=True),
        sa.Column('test_results', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['attempt_id'], ['candidate_attempts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # 3. Update candidate_attempts table
    op.add_column('candidate_attempts', sa.Column('time_limit_minutes', sa.Integer(), server_default='45', nullable=False))
    op.add_column('candidate_attempts', sa.Column('admin_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'candidate_attempts', 'admins', ['admin_id'], ['id'])
    
    # Make session_id and assigned_problem_id nullable
    op.alter_column('candidate_attempts', 'session_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('candidate_attempts', 'assigned_problem_id',
               existing_type=sa.String(length=10),
               nullable=True)

def downgrade() -> None:
    # Note: Downgrading enums in Postgres is complex and rarely needed for this project context.
    op.drop_constraint(None, 'candidate_attempts', type_='foreignkey')
    op.drop_column('candidate_attempts', 'admin_id')
    op.drop_column('candidate_attempts', 'time_limit_minutes')
    op.alter_column('candidate_attempts', 'assigned_problem_id',
               existing_type=sa.String(length=10),
               nullable=False)
    op.alter_column('candidate_attempts', 'session_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_table('candidate_problems')
    # Enum value removal is not straightforward in PG, so we skip it for safety.
