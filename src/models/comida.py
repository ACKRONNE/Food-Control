from sqlalchemy import Column, Numeric, String, CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from src.database.db import db

class Comida(db.Model):
  __tablename__ = 'comidas'
  
  id_paciente = Column(Numeric(3))
  id_espe = Column(Numeric(3))
  id_comida = Column(Numeric(3))
  tipo = Column(String(1), nullable=False)

  __table_args__ = (
      CheckConstraint(tipo.in_(['D', 'A', 'C', 'M']), name='check_tipo'),
      ForeignKeyConstraint(['id_paciente'], ['pacientes.id_paciente'], ondelete='CASCADE'),
      ForeignKeyConstraint(['id_espe'], ['especialistas.id_espe'], ondelete='CASCADE'),
      PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida'),
  )
  
  def __init__(self, id_paciente, id_espe, tipo):
    self.id_paciente = id_paciente
    self.id_espe = id_espe
    self.tipo = tipo