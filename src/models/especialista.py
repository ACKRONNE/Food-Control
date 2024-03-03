from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.dialects.postgresql import NUMERIC
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Especialista(db.Model):
  __tablename__ = 'especialistas'

  id_espe = Column(NUMERIC(3), primary_key=True)
  pri_nombre = Column(String(40), nullable=False)
  pri_apellido = Column(String(40), nullable=False)
  seg_apellido = Column(String(40), nullable=False)
  sexo = Column(String(1), nullable=False)
  correo = Column(String(40), nullable=False, unique=True)
  telefono = Column(NUMERIC(17), nullable=False)
  clave = Column(String(255), nullable=False)
  especialidad = Column(String(80), nullable=False)
  seg_nombre = Column(String(40))

  __table_args__ = (
      CheckConstraint(sexo.in_(['F', 'M', 'O']), name='check_sexo_e'),
  )

  def __init__(self, pri_nombre, pri_apellido, seg_apellido, sexo, correo, telefono, clave, especialidad, seg_nombre=None):
      self.pri_nombre = pri_nombre
      self.pri_apellido = pri_apellido
      self.seg_apellido = seg_apellido
      self.sexo = sexo
      self.correo = correo
      self.telefono = telefono
      self.clave = clave
      self.especialidad = especialidad
      self.seg_nombre = seg_nombre

