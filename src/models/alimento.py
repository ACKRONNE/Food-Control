from sqlalchemy import Column, Numeric, String, CheckConstraint
from src.database.db import db

class Alimento(db.Model):
  __tablename__ = 'alimentos'
  
  id_alimento = Column(Numeric(3), primary_key=True)
  tipo = Column(String(15), nullable=False)
  nombre = Column(String(40), nullable=False)
  cantidad = Column(Numeric(10), nullable=False, default=1)

  __table_args__ = (
      CheckConstraint(tipo.in_(['Proteina','Carbohidrato','Grasa','Vegetal','Fruta','Bebida','Dulce','Otros']), name='check_tipo'),
  )

  def __init__(self, tipo, nombre, cantidad):
    self.tipo = tipo
    self.nombre = nombre
    self.cantidad = cantidad