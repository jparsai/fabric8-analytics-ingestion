"""Initial Migration.

Revision ID: 0194c3a2332e
Revises:
Create Date: 2018-05-29 09:49:36.153016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0194c3a2332e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database to a newer revision."""
    ecosystems = op.create_table('ecosystems',
                                 sa.Column('id', sa.Integer(), nullable=False),
                                 sa.Column('name', sa.String(length=255), nullable=True),
                                 sa.Column('url', sa.String(length=255), nullable=True),
                                 sa.Column('_backend', sa.Enum('none', 'npm', 'maven', 'pypi',
                                           'rubygems', 'scm', 'crates', 'nuget',
                                                               name='ecosystem_backend_enum'),
                                           nullable=True),
                                 sa.PrimaryKeyConstraint('id'),
                                 sa.UniqueConstraint('name'))
    op.bulk_insert(ecosystems,
                   [
                       {'name': 'rubygems', '_backend': 'rubygems',
                        'url': 'https://rubygems.org/api/v1'},
                       {'name': 'npm', '_backend': 'npm',
                        'url': 'https://registry.npmjs.org/'},
                       {'name': 'maven', '_backend': 'maven',
                        'url': 'https://repo1.maven.org/maven2/'},
                       {'name': 'pypi', '_backend': 'pypi',
                        'url': 'https://pypi.python.org/pypi'},
                       {'name': 'go', '_backend': 'scm', 'url': None},
                       {'name': 'crates', '_backend': 'crates',
                        'url': 'https://crates.io/'}, ])
    op.create_table('packages',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('ecosystem_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['ecosystem_id'], ['ecosystems.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('ecosystem_id', 'name', name='ep_unique'))
    op.create_index(op.f('ix_packages_name'), 'packages', ['name'], unique=False)
    op.create_table('versions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('package_id', sa.Integer(), nullable=True),
                    sa.Column('identifier', sa.String(length=255), nullable=True),
                    sa.ForeignKeyConstraint(['package_id'], ['packages.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('package_id', 'identifier', name='pv_unique'))
    op.create_index(op.f('ix_versions_identifier'), 'versions', ['identifier'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    """Downgrade the database to an older revision."""
    op.drop_index(op.f('ix_versions_identifier'), table_name='versions')
    op.drop_table('versions')
    op.drop_index(op.f('ix_packages_name'), table_name='packages')
    op.drop_table('packages')
    op.drop_table('ecosystems')
    # ### end Alembic commands ###
