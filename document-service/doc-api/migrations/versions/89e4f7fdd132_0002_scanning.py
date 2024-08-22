"""0002_scanning

Revision ID: 89e4f7fdd132
Revises: 17113bea3f32
Create Date: 2024-08-20 16:46:53.218573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence  # Added manually.


# revision identifiers, used by Alembic.
revision = '89e4f7fdd132'
down_revision = '17113bea3f32'
branch_labels = None
depends_on = None


def upgrade():
    # ### Manually create sequences and add them to pk columns. ###
    op.execute(CreateSequence(Sequence('doc_scanning_id_seq', start=1, increment=1)))

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_scanning',
    sa.Column('id', sa.Integer(), sa.Sequence('doc_scanning_id_seq'), nullable=False),
    sa.Column('consumer_document_id', sa.String(length=20), nullable=False),
    sa.Column('scan_date', sa.DateTime(), nullable=False),
    sa.Column('accession_number', sa.String(length=20), nullable=True),
    sa.Column('batch_id', sa.String(length=20), nullable=True),
    sa.Column('author', sa.String(length=1000), nullable=True),
    sa.Column('page_count', sa.Integer(), nullable=True),
    # Manually added create_type=False
    sa.Column('document_class', postgresql.ENUM('COOP', 'CORP', 'FIRM', 'MHR', 'NR', 'OTHER', 'PPR', 'SOCIETY', name='documentclass', create_type=False), nullable=False),

    sa.ForeignKeyConstraint(['document_class'], ['document_classes.document_class'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('consumer_document_id', 'document_class', name='scanning_cons_id_class_uc')
    )
    with op.batch_alter_table('document_scanning', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_document_scanning_consumer_document_id'), ['consumer_document_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_document_scanning_document_class'), ['document_class'], unique=False)
        batch_op.create_index(batch_op.f('ix_document_scanning_scan_date'), ['scan_date'], unique=False)

    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.drop_column('scan_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scan_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    with op.batch_alter_table('document_scanning', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_document_scanning_scan_date'))
        batch_op.drop_index(batch_op.f('ix_document_scanning_document_class'))
        batch_op.drop_index(batch_op.f('ix_document_scanning_consumer_document_id'))

    op.drop_table('document_scanning')

    # Manually added drop sequence commands ###
    op.execute(DropSequence(Sequence('doc_scanning_id_seq')))

    # ### end Alembic commands ###
