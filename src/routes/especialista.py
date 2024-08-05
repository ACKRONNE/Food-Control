from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy import cast, Date, distinct, select
from src.database.db import db
from datetime import datetime

# Entidades
from src.models.models import Especialista, Paciente, Comida, AC, Alimento
# //

esp = Blueprint('especialista', __name__)

# Registro <
@esp.route('/registro_especialista', methods=['GET','POST'])
def registro():
    if request.method == "POST":
        pri_nombre = request.form['esp-pri-nombre']
        pri_apellido = request.form['esp-pri-apellido']
        seg_apellido = request.form['esp-seg-apellido']
        sexo = request.form['esp-sexo']
        correo = request.form['esp-correo']
        telefono = request.form['esp-telefono']
        clave = request.form['esp-clave']
        especialidad = request.form['esp-especialidad']
        seg_nombre = request.form['esp-seg-nombre']

        # Hacer la contraseña segura
        hashed_clave = generate_password_hash(clave)   
        # //

        # Se inserta el especialista en la tabla
        new_esp = Especialista (
            pri_nombre,
            pri_apellido,
            seg_apellido,
            sexo,
            correo,
            telefono,
            hashed_clave,
            especialidad,
            seg_nombre
        )

        db.session.add(new_esp)
        db.session.commit()
        db.session.close()

        flash("Especialista agregado correctamente", "success")
        # //

        return redirect(url_for('index.index'))
    else:
        return render_template('e_registro.html')
# // >

# Inicio <
@esp.route('/inicio_especialista/<int:id>')
def inicio(id):

    # Consulta todos los datos del especialista
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
    # //

    # Consulta todos los pacientes del especialista
    pacientes = select(distinct(Comida.id_paciente)).where(Comida.id_espe == id)
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente.in_(pacientes)).all()
    # //

    # Fecha Actual
    date = datetime.now()
    formatted_date = date.strftime("%b. %d")
    # //    

    return render_template('e_inicio.html', get_esp=get_esp, get_pac=get_pac, formatted_date=formatted_date)
# // >

# Perfil <
@esp.route('/perfil_especialista/<int:id>', methods=['GET'])
def perfil(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
    
    return render_template('e_perfil.html', get_esp=get_esp)
# //

# Modificar perfil <
@esp.route('/modificar_especialista/<int:id>', methods=['GET','POST'])
def updateProfile(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp is None:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))

    if request.method == "POST":
        get_esp.pri_nombre = request.form['esp-pri-nombre']
        get_esp.pri_apellido = request.form['esp-pri-apellido']
        get_esp.seg_apellido = request.form['esp-seg-apellido']
        get_esp.sexo = request.form['esp-sexo']
        get_esp.correo = request.form['esp-correo']
        get_esp.telefono = request.form['esp-telefono']
        clave = request.form['esp-clave']
        # Hacer la contraseña segura
        get_esp.clave = generate_password_hash(clave)   
        # //        
        get_esp.especialidad = request.form['esp-especialidad']
        get_esp.seg_nombre = request.form['esp-seg-nombre']

        db.session.commit()
        db.session.close()

        flash("Perfil modificado correctamente", "success")
        return redirect(url_for('especialista.perfil', id=id))
    else:
        return render_template('e_editar_perfil.html', get_esp=get_esp)
    
# Eliminar cuenta <
@esp.route('/eliminar_especialista/<int:id>', methods=['POST'])
def deleteAccount(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()

    if get_esp:
        db.session.delete(get_esp)
        db.session.commit()
        db.session.close()
        flash("Cuenta eliminada correctamente", "success")
        return redirect(url_for('index.index'))
    else:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
# //

# Detalle Paciente <
@esp.route('/detalle_paciente/<int:id_espe>/<int:id_pac>', methods=['GET'])
def detallePaciente(id_espe, id_pac):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()

    if get_pac is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('especialista.inicio', id=id_espe))
    
    return render_template('e_detalle_paciente.html', get_pac=get_pac, get_esp=get_esp)
