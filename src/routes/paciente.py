from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from sqlalchemy import and_, or_
from src.database.db import db
from datetime import datetime

# Entidades
from src.models.especialista import Especialista
from src.models.hist_comida import HistComida
from src.models.alimento import Alimento
from src.models.paciente import Paciente
from src.models.comida import Comida
from src.models.a_c import AC
# //

pac = Blueprint('paciente', __name__)

# Registrar <
@pac.route('/registro_paciente', methods=['GET','POST'])
def registro():
  if request.method == "POST":
    pri_nombre = request.form['pac-pri-nombre']
    pri_apellido = request.form['pac-pri-apellido']
    seg_apellido = request.form['pac-seg-apellido']
    sexo = request.form['pac-sexo']
    correo = request.form['pac-correo']
    telefono = request.form['pac-telefono']
    clave = request.form['pac-clave']
    fecha_nacimiento = (request.form['pac-fecha-nacimiento'])
    seg_nombre = request.form['pac-seg-nombre']

    # Hacer la contraseña segura
    hashed_clave = generate_password_hash(clave)   
    # //

    # Se inserta el paciente en la tabla
    new_pac = Paciente (
        pri_nombre,
        pri_apellido,
        seg_apellido,
        sexo,
        correo,
        telefono,
        hashed_clave,
        fecha_nacimiento,
        seg_nombre
    )

    db.session.add(new_pac)
    db.session.commit()
    db.session.close()

    flash("Paciente agregado correctamente", "success")
    # //

    return redirect(url_for('index.index'))
  
  else:
      return render_template('p_registro.html')
# // >


# Inicio <
@pac.route('/inicio/<id>', methods=['GET', 'POST'])
def inicio(id):

    # Consulta de todos los datos del paciente
    result = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    # //

    # Fecha Actual
    date = datetime.now()
    formatted_date = date.strftime("%b. %d")
    # //
    
    if request.method == "POST":

        # Extraigo la fecha del buscador
        fecha_str = request.form['pac-fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        date = fecha.strftime('%B, %d %Y')
        # //

        # Consulta de las comidas de los pacientes
        tipo = db.session.query(Comida.tipo, Comida.id_comida).join(
            HistComida, 
            and_(
                Comida.id_paciente == HistComida.id_paciente,
                Comida.id_espe == HistComida.id_espe,
                Comida.id_comida == HistComida.id_comida
            )
        ).filter(
            Comida.id_paciente == result.id_paciente,
            HistComida.fecha_ini == fecha
        ).all()      
        # //

        db.session.close()
        
        return render_template('p_inicio.html', result=result, date=date, formatted_date=formatted_date, tipo=tipo, fecha=fecha)

    return render_template("p_inicio.html", result=result, formatted_date=formatted_date)
# // >

# Perfil <
@pac.route('/perfil/<id>', methods=["GET"])
def perfil(id):
    paciente = Paciente.query.get(id)
    return render_template("p_perfil.html", id=id, paciente=paciente)
# // >

# Detalle de comida <
@pac.route('/detalle_comida/<id>/<date>/<comida>', methods=["GET"])
def detalleComida(id, date, comida):

    result = db.session.query(Paciente.id_paciente).filter(Paciente.id_paciente == id).first()
    
    # Consulta de SQLAlchemy 
    datos = db.session.query(
        Alimento.tipo.label('tipo_alimento'),
        Comida.tipo.label('tipo_comida'),
        HistComida.satisfaccion,
        HistComida.comentario,
        Alimento.nombre,
        Alimento.cantidad
    ).join(
        AC, and_(
            Comida.id_paciente == AC.id_paciente,
            Comida.id_espe == AC.id_espe,
            Comida.id_comida == AC.id_comida
        )
    ).join(
        HistComida, and_(
            HistComida.id_paciente == Comida.id_paciente,
            HistComida.id_espe == Comida.id_espe,
            HistComida.id_comida == Comida.id_comida
        )
    ).join(
        Alimento, Alimento.id_alimento == AC.id_alimento
    ).filter(
        HistComida.fecha_ini == date,
        Comida.id_paciente == result.id_paciente,
        Comida.id_comida == comida
    ).all()
   
    db.session.close()

    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_formatted = date_obj.strftime("%B, %d %Y")

    return render_template("p_detalle.html", result=result, datos=datos, date=date, comida=comida, date_formatted=date_formatted)
# // >

@pac.route('/eliminar_cuenta/<id>', methods=['POST'])
def deleteAccount(id):
    paciente = Paciente.query.get(id)
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
        return redirect(url_for('index.index')) # Redirige al usuario a la página de inicio
    else:
        return "Paciente no encontrado", 404

# Modificar Perfil <
@pac.route('/editar_perfil/<id>', methods=['GET', 'POST'])
def updateProfile(id):

    paciente = Paciente.query.get(id)

    if request.method == 'POST':

        paciente.pri_nombre = request.form['pac-pri-nombre']
        paciente.pri_apellido = request.form['pac-pri-apellido']
        paciente.seg_apellido = request.form['pac-seg-apellido']
        paciente.sexo = request.form['pac-sexo']
        paciente.correo = request.form['pac-correo']
        paciente.telefono = request.form['pac-telefono']
        clave = request.form['pac-clave']
        # Hacer la contraseña segura
        paciente.clave = generate_password_hash(clave)   
        # //
        paciente.fecha_nacimiento = request.form['pac-fecha-nacimiento']
        paciente.seg_nombre = request.form['pac-seg-nombre']

        db.session.commit()

        return render_template('p_editar_perfil.html', paciente=paciente)
    
    return render_template('p_editar_perfil.html', paciente=paciente)
# // >

# Agregar Comida < FIXME:
@pac.route('/agregar_comida/<id>/<date>', methods=['GET', 'POST'])
def addFood(id, date):

    paciente = Paciente.query.get(id)
    
    if request.method == 'POST':
        tipo_comida = request.form['tipo_comida']
        satisfaccion = request.form['satisfaccion']
        comentario = request.form['comentario']
        alimentos = request.form.getlist('alimentos')

        # Se inserta la comida en la tabla
        new_comida = Comida (
            result.id_paciente,
            1,
            tipo_comida
        )

        db.session.add(new_comida)
        db.session.commit()

        # Se insertan los alimentos en la tabla
        for alimento in alimentos:
            new_ac = AC (
                result.id_paciente,
                1,
                new_comida.id_comida,
                alimento
            )
            db.session.add(new_ac)
            db.session.commit()

        # Se inserta el historial de la comida
        new_hist_comida = HistComida (
            result.id_paciente,
            1,
            new_comida.id_comida,
            satisfaccion,
            comentario,
            date
        )

        db.session.add(new_hist_comida)
        db.session.commit()
        db.session.close()

        return redirect(url_for('paciente.inicio', id=id))
    
    return render_template('p_agregar_comida.html', id=id, date=date)
# // >

# Ver Especialistas <
@pac.route('/ver_especialistas/<id>', methods=['GET'])
def especialistas(id):
    
    date = datetime.now()
    date = date.strftime("%b, %d %Y")

    result = db.session.query(
        Especialista.pri_nombre, 
        Especialista.pri_apellido, 
        Especialista.especialidad,
    ).join(
        Comida, Especialista.id_espe == Comida.id_espe
    ).filter(
        Comida.id_paciente == id
    ).distinct()

    return render_template('p_especialistas.html', id=id, result=result, date=date)
# // >