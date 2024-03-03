
from sqlalchemy import Column, Numeric, PrimaryKeyConstraint, ForeignKeyConstraint
from src.database.db import db

class A_C(db.Model):
  __tablename__ = 'a_c'
  
  id_paciente = Column(Numeric(3))
  id_espe = Column(Numeric(3))
  id_comida = Column(Numeric(3))
  id_alimento = Column(Numeric(3))

  __table_args__ = (
      ForeignKeyConstraint(['id_paciente', 'id_espe', 'id_comida'], ['comidas.id_paciente', 'comidas.id_espe', 'comidas.id_comida']),
      ForeignKeyConstraint(['id_alimento'], ['alimentos.id_alimento']),
      PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida', 'id_alimento'),
  )
  
  def __init__(self, id_paciente, id_espe, id_comida, id_alimento):
    self.id_paciente = id_paciente
    self.id_espe = id_espe
    self.id_comida = id_comida
    self.id_alimento = id_alimento