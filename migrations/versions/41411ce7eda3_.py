"""empty message

Revision ID: 41411ce7eda3
Revises: 443e34a2cdd8
Create Date: 2017-02-20 20:26:25.103998

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision = '41411ce7eda3'
down_revision = '443e34a2cdd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ambientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('tipo', sa.String(length=64), nullable=True),
    sa.Column('detalhe_localizacao', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ambientes_nome'), 'ambientes', ['nome'], unique=False)
    op.create_index(op.f('ix_ambientes_tipo'), 'ambientes', ['tipo'], unique=False)
    op.create_table('instituicoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instituicoes_nome'), 'instituicoes', ['nome'], unique=True)
    op.create_table('campi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('id_instituicao', sa.Integer(), nullable=True),
    sa.Column('mapeamento', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON'), nullable=True),
    sa.ForeignKeyConstraint(['id_instituicao'], ['instituicoes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mapeamento')
    )
    op.create_index(op.f('ix_campi_nome'), 'campi', ['nome'], unique=True)
    op.create_table('equipamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tombamento', sa.Integer(), nullable=True),
    sa.Column('id_ambiente', sa.Integer(), nullable=True),
    sa.Column('categoria_equipamento', sa.String(length=64), nullable=True),
    sa.Column('tipo_equipamento', sa.String(length=64), nullable=True),
    sa.Column('fabricante', sa.String(length=64), nullable=True),
    sa.Column('intervalo_manutencao', sa.Integer(), nullable=True),
    sa.Column('proxima_manutencao', sa.Date(), nullable=True),
    sa.Column('info_adicional', sa.Text(), nullable=True),
    sa.Column('em_uso', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_ambiente'], ['ambientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_equipamentos_categoria_equipamento'), 'equipamentos', ['categoria_equipamento'], unique=False)
    op.create_index(op.f('ix_equipamentos_em_uso'), 'equipamentos', ['em_uso'], unique=False)
    op.create_index(op.f('ix_equipamentos_fabricante'), 'equipamentos', ['fabricante'], unique=False)
    op.create_index(op.f('ix_equipamentos_proxima_manutencao'), 'equipamentos', ['proxima_manutencao'], unique=False)
    op.create_index(op.f('ix_equipamentos_tipo_equipamento'), 'equipamentos', ['tipo_equipamento'], unique=False)
    op.create_table('centros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('id_campus', sa.Integer(), nullable=True),
    sa.Column('mapeamento', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON'), nullable=True),
    sa.ForeignKeyConstraint(['id_campus'], ['campi.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mapeamento')
    )
    op.create_index(op.f('ix_centros_nome'), 'centros', ['nome'], unique=False)
    op.create_table('extintores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classificacao', sa.String(length=64), nullable=True),
    sa.Column('carga_nominal', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['equipamentos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('manutencoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num_ordem_servico', sa.Integer(), nullable=False),
    sa.Column('id_equipamento', sa.Integer(), nullable=True),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('tipo_manutencao', sa.String(length=64), nullable=True),
    sa.Column('descricao_servico', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['id_equipamento'], ['equipamentos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manutencoes_data'), 'manutencoes', ['data'], unique=False)
    op.create_index(op.f('ix_manutencoes_status'), 'manutencoes', ['status'], unique=False)
    op.create_index(op.f('ix_manutencoes_tipo_manutencao'), 'manutencoes', ['tipo_manutencao'], unique=False)
    op.create_table('subestacoes_abrigadas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_campus', sa.Integer(), nullable=True),
    sa.Column('localizacao', geoalchemy2.types.Geometry(geometry_type='POINT'), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['id_campus'], ['campi.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('localizacao')
    )
    op.create_table('subestacoes_aereas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_campus', sa.Integer(), nullable=True),
    sa.Column('localizacao', geoalchemy2.types.Geometry(geometry_type='POINT'), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['id_campus'], ['campi.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('localizacao')
    )
    op.create_table('departamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('id_centro', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_centro'], ['centros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departamentos_nome'), 'departamentos', ['nome'], unique=False)
    op.create_table('blocos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('localizacao', geoalchemy2.types.Geometry(geometry_type='POINT'), nullable=True),
    sa.Column('id_departamento', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_departamento'], ['departamentos.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('localizacao')
    )
    op.create_index(op.f('ix_blocos_nome'), 'blocos', ['nome'], unique=False)
    op.create_table('ambientes_externos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_bloco', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['id_bloco'], ['blocos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ambientes_internos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_bloco', sa.Integer(), nullable=True),
    sa.Column('andar', sa.String(length=15), nullable=True),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('populacao', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['ambientes.id'], ),
    sa.ForeignKeyConstraint(['id_bloco'], ['blocos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint(u'(srid > 0) AND (srid <= 998999)', name=u'spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name=u'spatial_ref_sys_pkey')
    )
    op.drop_table('ambientes_internos')
    op.drop_table('ambientes_externos')
    op.drop_index(op.f('ix_blocos_nome'), table_name='blocos')
    op.drop_table('blocos')
    op.drop_index(op.f('ix_departamentos_nome'), table_name='departamentos')
    op.drop_table('departamentos')
    op.drop_table('subestacoes_aereas')
    op.drop_table('subestacoes_abrigadas')
    op.drop_index(op.f('ix_manutencoes_tipo_manutencao'), table_name='manutencoes')
    op.drop_index(op.f('ix_manutencoes_status'), table_name='manutencoes')
    op.drop_index(op.f('ix_manutencoes_data'), table_name='manutencoes')
    op.drop_table('manutencoes')
    op.drop_table('extintores')
    op.drop_index(op.f('ix_centros_nome'), table_name='centros')
    op.drop_table('centros')
    op.drop_index(op.f('ix_equipamentos_tipo_equipamento'), table_name='equipamentos')
    op.drop_index(op.f('ix_equipamentos_proxima_manutencao'), table_name='equipamentos')
    op.drop_index(op.f('ix_equipamentos_fabricante'), table_name='equipamentos')
    op.drop_index(op.f('ix_equipamentos_em_uso'), table_name='equipamentos')
    op.drop_index(op.f('ix_equipamentos_categoria_equipamento'), table_name='equipamentos')
    op.drop_table('equipamentos')
    op.drop_index(op.f('ix_campi_nome'), table_name='campi')
    op.drop_table('campi')
    op.drop_index(op.f('ix_instituicoes_nome'), table_name='instituicoes')
    op.drop_table('instituicoes')
    op.drop_index(op.f('ix_ambientes_tipo'), table_name='ambientes')
    op.drop_index(op.f('ix_ambientes_nome'), table_name='ambientes')
    op.drop_table('ambientes')
    # ### end Alembic commands ###
