from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy import cast, Date
from src.database.db import db
from datetime import datetime

# Entidades
from src.models.models import Especialista, Paciente, Comida, AC, Alimento
# //

# FIXME: Hay que agregar los try-catch en todos los metodos

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
    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()

    if get_pac is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 
    # //

    # Consulta de las comidas del paciente
    tipo = (
        db.session.query(Comida.tipo, Comida.fecha_ini)
        .filter(Comida.id_paciente == id)
    ).all()
    # //

    # Fecha Actual
    date = datetime.now()
    formatted_date = date.strftime("%b. %d")
    # //
    
    if request.method == "POST":

        # Extraigo la fecha del buscador
        fecha_str = request.form['pac-fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        # //

        date = fecha.strftime('%B, %d %Y') # Formateo de la fecha de la consulta

        # Consulta de las comidas del paciente
        tipo = (
            db.session.query(Comida.tipo, Comida.fecha_ini)
            .filter(cast(Comida.fecha_ini, Date) == fecha.date())
            .filter(Comida.id_paciente == id)
        ).all()
        # //

        db.session.close()
        
        return render_template('p_inicio.html', get_pac=get_pac, formatted_date=formatted_date, date=date, tipo=tipo, fecha=fecha)

    return render_template("p_inicio.html", get_pac=get_pac, formatted_date=formatted_date)
# // >

# Perfil <
@pac.route('/perfil/<id>', methods=["GET"])
def perfil(id):
    paciente = Paciente.query.get(id)

    if paciente is None:
        flash("Paciente no encontrado", "danger")
        return redirect(url_for('index.index'))
    
    return render_template("p_perfil.html", id=id, paciente=paciente)
# // >

# Modificar Perfil <
@pac.route('/editar_perfil/<id>', methods=['GET', 'POST'])
def updateProfile(id):

    paciente = Paciente.query.get(id)

    if paciente is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

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
        db.session.close()

        flash("Perfil actualizado correctamente", "success")
        return render_template('p_editar_perfil.html', paciente=paciente)
    
    return render_template('p_editar_perfil.html', paciente=paciente)
# // >

# Eliminar Cuenta <
@pac.route('/eliminar_cuenta/<id>', methods=['POST'])
def deleteAccount(id):
    paciente = Paciente.query.get(id)


    if paciente:
        db.session.delete(paciente)
        db.session.commit()
        db.session.close()
        flash("Cuenta eliminada correctamente", "success")
        return redirect(url_for('index.index'))
    else:
        flash("Especialista no encontrado", "danger")
        return redirect(url_for('index.index'))
# // >

# FIXME: Agregar una validacion que si o consigue a ningun especialista muestre un mensaje que diga, usted no tienen un especialista asignado por favor contacte a la fundacion para mas informacion
# Agregar Comida < 
@pac.route('/agregar_comida/<id>', methods=['GET', 'POST'])
def addFood(id):     

    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    get_ali = db.session.query(Alimento).all()

    if get_pac is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

    if request.method == 'POST':
        try:
            tipo_comida = request.form['tipo-comida']
            satisfaccion = request.form['satisfaccion']
            comentario = request.form['comentario']
            fecha_ini = request.form['fecha-ini']

            id_espe = 1  # FIXME: Reemplazar esto con el ID correcto del especialista

            new_comida = Comida(
                get_pac.id_paciente,
                id_espe,
                fecha_ini,
                tipo_comida,
                satisfaccion,
                comentario
            )
            db.session.add(new_comida)
            db.session.commit()

            print("Comida Agregada con exito")
            flash("Comida Agregada con exito")

            _alimento = request.form.getlist('alimentos[]')

            for alimento in _alimento:
                if alimento:
                    new_ac = AC(
                        get_pac.id_paciente,
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
            flash("Ocurrió un error al agregar la comida.", "danger")
            print(f"Error: {e}")
        finally:
            db.session.close()

        return redirect(url_for('paciente.inicio', id=id))
    
    return render_template('p_add_comida.html', id=id, get_pac=get_pac, get_ali=get_ali)
# // >

# Detalle de comida <
@pac.route('/detalle_comida/<id>/<date>', methods=["GET"])
def foodDetail(id, date):
    try:
        get_pac = db.session.query(Paciente.id_paciente).filter(Paciente.id_paciente == id).first()
    
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
        filter(
            Comida.fecha_ini == date, 
            Comida.id_paciente == id,
            AC.fecha_ini == Comida.fecha_ini
        ).distinct().all()
       
        db.session.close()

        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_formatted = date_obj.strftime("%B, %d %Y a las %H:%M")

        return render_template("p_detalle_comida.html", get_pac=get_pac, datos=datos, date=date, date_formatted=date_formatted)
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error en el Detalle de Comida: {e}")
        return render_template(url_for('paciente.inicio', id=id))
# // >

# Modificar Comida <
@pac.route('/editar_comida/<id>/<date>', methods=['GET', 'POST'])
def updateFood(id, date):

    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    get_ali = db.session.query(Alimento).all()

    if get_pac is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 
    
    date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_formatted = date_obj.strftime("%B, %d %Y a las %H:%M")

    datos = db.session.query(
        Alimento.nombre,
        Alimento.cantidad,
        Alimento.id_alimento,
        Alimento.tipo.label('tipo_alimento'),
        Comida.fecha_ini,
        Comida.tipo,
        Comida.satisfaccion,
        Comida.comentario
    ).select_from(Comida).\
    join(AC, Comida.id_paciente == AC.id_paciente).\
    join(Alimento, Alimento.id_alimento == AC.id_alimento).\
    filter(
        Comida.fecha_ini == date, 
        Comida.id_paciente == id,
        AC.fecha_ini == Comida.fecha_ini
    ).distinct().all()       
             
    if request.method == 'POST':
        try:

            tipo_comida = request.form['tipo-comida']
            satisfaccion = request.form['satisfaccion']
            comentario = request.form['comentario']

            comida = db.session.query(Comida).filter(
                Comida.id_paciente == id,
                Comida.fecha_ini == date
            ).first()

            comida.tipo = tipo_comida
            comida.satisfaccion = satisfaccion
            comida.comentario = comentario

            db.session.commit()

            _alimento = request.form.getlist('alimentos[]')

            for alimento in _alimento:
                if alimento:
                    # Verificar si el alimento ya existe
                    existing_ac = db.session.query(AC).filter(
                        AC.id_paciente == get_pac.id_paciente,
                        AC.id_espe == comida.id_espe,
                        AC.fecha_ini == date,
                        AC.id_alimento == alimento
                    ).first()

                    if existing_ac is None:
                        new_ac = AC(
                            get_pac.id_paciente,
                            comida.id_espe,
                            date,
                            alimento
                        )
                        db.session.add(new_ac)
                        print("Registro de alimento agregado con exito")
                        flash("Registro de alimento agregado con exito")
                    else:
                        print("El alimento ya ha sido agregado anteriormente")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error al modificar la comida.", "danger")
            print(f"Error: {e}")
        finally:
            db.session.close()

        return redirect(url_for('paciente.inicio', id=id))
    
    return render_template('p_editar_comida.html', id=id, get_pac=get_pac, get_ali=get_ali, date=date, datos=datos, date_formatted=date_formatted)

# Funcion para eliminar un alimento dentro de la comida
@pac.route('/eliminar_alimento/<int:id_alimento>/<date>/<int:id>', methods=['DELETE'])
def eliminar_alimento(id_alimento, date, id):
    try:
        print(id_alimento, date, id)
        ac_record = db.session.query(AC).filter(
            AC.id_alimento == id_alimento,
            AC.id_paciente == id,
            AC.fecha_ini == date
        ).first()
        if ac_record:
            db.session.delete(ac_record)
            db.session.commit()
            return jsonify({'message': 'Alimento eliminado con éxito.'}), 200
        else:
            return jsonify({'message': 'Alimento no encontrado.'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el alimento: {e}'}), 500
    finally:
        db.session.close()
# // >
# >

# Eliminar Comida <
@pac.route('/eliminar_comida/<id>/<date>', methods=['GET', 'POST'])
def deleteFood(id, date):
    try:
        comida = db.session.query(Comida).filter(
            Comida.id_paciente == id,
            Comida.fecha_ini == date
        ).first()
        if comida:
            db.session.delete(comida)
            db.session.commit()
            return redirect(url_for('paciente.inicio', id=id))
        else:
            flash("Comida no encontrada", "danger")
            return redirect(url_for('paciente.inicio', id=id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar la comida: {e}", "danger")
        return redirect(url_for('paciente.inicio', id=id))
    finally:
        db.session.close()
# // >

# Ver Especialistas <
@pac.route('/ver_especialistas/<id>', methods=['GET'])
def especialistas(id):
    
    date = datetime.now()
    date = date.strftime("%b, %d %Y")

    comida_alias = aliased(Comida)
    espe_alias = aliased(Especialista)

    result = db.session.query(
        espe_alias.pri_nombre, 
        espe_alias.pri_apellido, 
        espe_alias.especialidad,
        espe_alias.id_espe
    ).join(
        comida_alias, espe_alias.id_espe == comida_alias.id_espe
    ).filter(
        comida_alias.id_paciente == id
    ).distinct()

    return render_template('p_ver_especialistas.html', id=id, result=result, date=date)
# // >

# Detalle especialistas <
@pac.route('/detalle_especialista/<id>/<espe>', methods=['GET'])
def detalleEspecialista(id, espe):

    paciente = Paciente.query.get(id)
    especialista = db.session.query(Especialista).filter(Especialista.id_espe == espe).first()

    # FIXME: Estas haciendo que funcione el filtro para tener el menu de las comidas del especialista

    db.session.close()

    return render_template('p_detalle_especialista.html', especialista=especialista, paciente=paciente)
# // >