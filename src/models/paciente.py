from sqlalchemy import Column, String, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import NUMERIC
from src.database.db import db

class Paciente(db.Model):
  __tablename__ = 'pacientes'

  id_paciente = Column(NUMERIC(3), primary_key=True)
  pri_nombre = Column(String(40), nullable=False)
  pri_apellido = Column(String(40), nullable=False)
  seg_apellido = Column(String(40), nullable=False)
  sexo = Column(String(1), nullable=False)
  correo = Column(String(40), nullable=False, unique=True)
  telefono = Column(NUMERIC(17), nullable=False)
  clave = Column(String(255), nullable=False)
  fecha_nacimiento = Column(Date, nullable=False)
  seg_nombre = Column(String(40))

  __table_args__ = (
      CheckConstraint(sexo.in_(['F', 'M', 'O']), name='check_sexo_p'),
  )

  def __init__(self, pri_nombre, pri_apellido, seg_apellido, sexo, correo, telefono, clave, fecha_nacimiento, seg_nombre=None):
      self.pri_nombre = pri_nombre
      self.pri_apellido = pri_apellido
      self.seg_apellido = seg_apellido
      self.sexo = sexo
      self.correo = correo
      self.telefono = telefono
      self.clave = clave
      self.fecha_nacimiento = fecha_nacimiento
      self.seg_nombre = seg_nombre

