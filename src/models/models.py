from sqlalchemy import Column, String, Date, CheckConstraint, PrimaryKeyConstraint, ForeignKey, Integer, ForeignKeyConstraint
from src.database.db import db

# 1
class Paciente(db.Model):
  __tablename__ = 'pacientes'

  id_paciente = Column(Integer, primary_key=True)
  pri_nombre = Column(String(40), nullable=False)
  pri_apellido = Column(String(40), nullable=False)
  seg_apellido = Column(String(40), nullable=False)
  sexo = Column(String(1), nullable=False)
  correo = Column(String(40), nullable=False, unique=True)
  telefono = Column(String(17), nullable=False)
  clave = Column(String(255), nullable=False)
  fecha_nacimiento = Column(Date, nullable=False)
  seg_nombre = Column(String(40))

  __table_args__ = (
      CheckConstraint("sexo IN ('F', 'M', 'O')", name='check_sexo_p'),
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
# //

# 2
class Especialista(db.Model):
    __tablename__ = 'especialistas'
    
    id_espe = Column(Integer, primary_key=True)
    pri_nombre = Column(String(40), nullable=False)
    pri_apellido = Column(String(40), nullable=False)
    seg_apellido = Column(String(40), nullable=False)
    sexo = Column(String(1), nullable=False)
    correo = Column(String(40), nullable=False, unique=True)
    telefono = Column(String(17), nullable=False)
    clave = Column(String(255), nullable=False)
    especialidad = Column(String(80), nullable=False)
    seg_nombre = Column(String(40))

    __table_args__ = (
        CheckConstraint("sexo IN ('F', 'M', 'O')", name='check_sexo'),
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
# //

# 3
class Alimento(db.Model):
  __tablename__ = 'alimentos'
  
  id_alimento = Column(Integer, primary_key=True)
  tipo = Column(String(15), nullable=False)
  nombre = Column(String(40), nullable=False)
  cantidad = Column(Integer, nullable=False, server_default='1')

  __table_args__ = (
      CheckConstraint("tipo IN ('Proteina','Carbohidrato','Grasa','Vegetal','Fruta','Bebida','Dulce','Otros')", name='check_tipo'),
  )

  def __init__(self, tipo, nombre, cantidad):
    self.tipo = tipo
    self.nombre = nombre
    self.cantidad = cantidad
# //

# 4
class Comida(db.Model):
    __tablename__ = 'comidas'

    id_paciente = Column(Integer, ForeignKey('pacientes.id_paciente'), nullable=False)
    id_espe = Column(Integer, ForeignKey('especialistas.id_espe'), nullable=False)
    id_comida = Column(Integer, nullable=False, autoincrement=True)
    tipo = Column(String(1), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida'),
        CheckConstraint("tipo IN ('D', 'A', 'C', 'M')", name='check_tipo'),
    )

    def __init__(self, id_paciente, id_espe, tipo):
        self.id_paciente = id_paciente
        self.id_espe = id_espe
        self.tipo = tipo
# //

# 5
class HistComida(db.Model):
    __tablename__ = 'hist_comida'

    id_paciente = Column(Integer)
    id_espe = Column(Integer)
    id_comida = Column(Integer)
    fecha_ini = Column(Date)
    satisfaccion = Column(String(40), nullable=False)
    comentario = Column(String(40))
    fecha_fin = Column(Date)

    __table_args__ = (
        ForeignKeyConstraint(['id_paciente', 'id_espe', 'id_comida'], ['comidas.id_paciente', 'comidas.id_espe', 'comidas.id_comida'], ondelete='CASCADE'),
        PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida', 'fecha_ini'),
        CheckConstraint("satisfaccion IN ('Cansado', 'Mal', 'No muy bien', 'Normal', 'Bien', 'Super')", name='check_satisfaccion'),
    )

    def __init__(self, id_paciente, id_espe, id_comida, fecha_ini, satisfaccion, comentario=None, fecha_fin=None):
        self.id_paciente = id_paciente
        self.id_espe = id_espe
        self.id_comida = id_comida
        self.fecha_ini = fecha_ini
        self.satisfaccion = satisfaccion
        self.comentario = comentario
        self.fecha_fin = fecha_fin
# //

# 6
class AC(db.Model):
  __tablename__ = 'a_c'
  
  id_paciente = Column(Integer)
  id_espe = Column(Integer)
  id_comida = Column(Integer)
  id_alimento = Column(Integer)

  __table_args__ = (
      ForeignKeyConstraint(['id_paciente', 'id_espe', 'id_comida'], ['comidas.id_paciente', 'comidas.id_espe', 'comidas.id_comida'], ondelete='CASCADE'),
      ForeignKeyConstraint(['id_alimento'], ['alimentos.id_alimento'], ondelete='CASCADE'),
      PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida', 'id_alimento'),
  )
  
  def __init__(self, id_paciente, id_espe, id_comida, id_alimento):
    self.id_paciente = id_paciente
    self.id_espe = id_espe
    self.id_comida = id_comida
    self.id_alimento = id_alimento
# //