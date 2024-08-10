from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from scipy.fft import idctn
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
# //

# Anadir Comida <
@esp.route('/anadir_comida/<int:id>', methods=['GET','POST'])
def addFood(id):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id).first()
    get_ali = db.session.query(Alimento).all()

    get_pac = db.session.query(
        Paciente.id_paciente,
        Paciente.pri_nombre,
        Paciente.pri_apellido
    ).select_from(Comida)\
    .join(Paciente, Comida.id_paciente == Paciente.id_paciente)\
    .join(Especialista, Comida.id_espe == Especialista.id_espe)\
    .filter(
        Especialista.id_espe == id
    ).distinct().all()

    if get_esp is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('especialista.inicio', id=id))

    if request.method == "POST":
        try:
            tipo_comida = request.form['tipo-comida']
            id_paciente = request.form['id-paciente']
            fecha_ini = request.form['fecha-ini']
            fecha_fin = request.form['fecha-fin']
              # Verificar que todos los datos necesarios están presentes
            
            print(f"tipo_comida: {tipo_comida}")
            print(f"id_paciente: {id_paciente}")
            print(f"fecha_ini: {fecha_ini}")
            print(f"fecha_fin: {fecha_fin}")

            new_comida = Comida(
                id_paciente,
                get_esp.id_espe,
                fecha_ini,
                tipo_comida,
                fecha_fin
            )
            db.session.add(new_comida)
            db.session.commit()
            print("Comida agregada con exito")
            flash("Comida agregada correctamente", "success")

            _alimmento = request.form.getlist('alimentos[]')

            for alimento in _alimmento:
                if alimento:
                    new_ac = AC(
                        id_paciente,
                        get_esp.id_espe,
                        new_comida.fecha_ini,
                        alimento
                    )
                    db.session.add(new_ac)

                    print("Registro de alimento agregado con exito")
                    flash("Registro de alimento agregado con exito")
    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Ocurrio un error al agregar la comida", "danger")
            print(f"Error: {e}")      
        finally:
            db.session.close()

        return redirect(url_for('especialista.inicio', id=id))

    else:
        return render_template('e_add_comida.html', id=id, get_pac=get_pac, get_esp=get_esp, get_ali=get_ali)
# //

# Detalle Comida <
@esp.route('/detalles_comidas/<id_espe>/<id_pac>', methods=['GET'])
def foodDetail(id_espe, id_pac):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()
    datos = db.session.query(
        Alimento.nombre,
        Alimento.cantidad,
        Alimento.tipo.label('tipo_alimento'),
        Comida.fecha_ini,
        Comida.tipo,
        Comida.satisfaccion,
        Comida.comentario
    ).select_from(Comida).\
    join(AC, Comida.id_paciente == AC.id_paciente).\
    join(Alimento, Alimento.id_alimento == AC.id_alimento).\
    join(Especialista, Comida.id_espe == Especialista.id_espe).\
    join(Paciente, Comida.id_paciente == Paciente.id_paciente).\
    filter(
        Comida.id_espe == id_espe, 
        Comida.id_paciente == id_pac,
    ).distinct().all()

    return render_template('e_detalle_comida.html', get_esp=get_esp, get_pac=get_pac, datos=datos)
# //

# Modificar Comida
@esp.route('/modificar_comida/<id_espe>/<id_pac>/<fecha_ini>', methods=['GET','POST'])
def updateFood(id_espe, id_pac, fecha_ini):
    get_esp = db.session.query(Especialista).filter(Especialista.id_espe == id_espe).first()
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id_pac).first()
    get_comida = db.session.query(Comida).filter(Comida.id_paciente == id_pac, Comida.id_espe == id_espe, Comida.fecha_ini == fecha_ini).first()
    get_ac = db.session.query(AC).filter(AC.id_paciente == id_pac, AC.id_espe == id_espe, AC.fecha_ini == fecha_ini).all()
    get_ali = db.session.query(Alimento).all()

    if get_comida is None:
        flash("Comida no encontrada", "danger")
        return redirect(url_for('especialista.inicio', id=id_espe))

    if request.method == "POST":
        try:
            tipo_comida = request.form['tipo-comida']
            fecha_ini = request.form['fecha-ini']
            fecha_fin = request.form['fecha-fin']
            # Verificar que todos los datos necesarios están presentes
            get_comida.tipo_comida = tipo_comida
            get_comida.fecha_ini = fecha_ini
            get_comida.fecha_fin = fecha_fin

            db.session.commit()
            flash("Comida modificada correctamente", "success")

            _alimmento = request.form.getlist('alimentos[]')

            for alimento in _alimmento:
                if alimento:
                    new_ac = AC(
                        id_pac,
                        id_espe,
                        fecha_ini,
                        alimento
                    )
                    db.session.add(new_ac)
                    print("Registro de alimento agregado con exito")
                    flash("Registro de alimento agregado con exito")
    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Ocurrio un error al modificar la comida", "danger")
            print(f"Error: {e}")      
        finally:
            db.session.close()

        return redirect(url_for('especialista.inicio', id=id_espe))

    else:
        return render_template('e_modificar_comida.html', get_esp=get_esp, get_pac=get_pac, get_comida=get_comida)
