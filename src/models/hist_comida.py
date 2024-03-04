from sqlalchemy import Column, Numeric, Date, ForeignKeyConstraint, String, CheckConstraint, PrimaryKeyConstraint
from src.database.db import db

class HistComida(db.Model):
    __tablename__ = 'hist_comida'

    id_paciente = Column(Numeric(3))
    id_espe = Column(Numeric(3))
    id_comida = Column(Numeric(3))
    fecha_ini = Column(Date)
    satisfaccion = Column(String(40), nullable=False)
    comentario = Column(String(40))
    fecha_fin = Column(Date)

    __table_args__ = (
        ForeignKeyConstraint(['id_paciente', 'id_espe', 'id_comida'], ['comidas.id_paciente', 'comidas.id_espe', 'comidas.id_comida'], ondelete='CASCADE'),
        PrimaryKeyConstraint('id_paciente', 'id_espe', 'id_comida', 'fecha_ini'),
        CheckConstraint(satisfaccion.in_(['Cansado', 'Mal', 'No muy bien', 'Normal', 'Bien', 'Super']), name='check_satisfaccion'),
    )

    def __init__(self, id_paciente, id_espe, id_comida, fecha_ini, satisfaccion, comentario=None, fecha_fin=None):
        self.id_paciente = id_paciente
        self.id_espe = id_espe
        self.id_comida = id_comida
        self.fecha_ini = fecha_ini
        self.satisfaccion = satisfaccion
        self.comentario = comentario
        self.fecha_fin = fecha_fin
