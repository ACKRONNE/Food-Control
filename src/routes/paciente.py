from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased
from sqlalchemy import and_, or_
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
    result = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    # //

    if result is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

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
            HistComida.fecha_ini == fecha.date() 
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

# Eliminar Cuenta <
@pac.route('/eliminar_cuenta/<id>', methods=['POST'])
def deleteAccount(id):
    paciente = Paciente.query.get(id)
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
        return redirect(url_for('index.index'))
    else:
        return "Paciente no encontrado", 404
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

        return render_template('p_editar_perfil.html', paciente=paciente)
    
    return render_template('p_editar_perfil.html', paciente=paciente)
# // >

# FIXME: Agregar una validacion que si o consigue a ningun especialista muestre un mensaje que diga, usted no tienen un especialista asignado por favor contacte a la fundacion para mas informacion

# Agregar Comida < 
@pac.route('/agregar_comida/<id>', methods=['GET', 'POST'])
def addFood(id):     

    get_pac = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()
    get_prot = db.session.query(Alimento).filter(Alimento.tipo == 'Proteina').all()

    if get_pac is None:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('index.index')) 

    if request.method == 'POST':

        tipo_comida = request.form['tipo-comida']
        satisfaccion = request.form['satisfaccion']
        comentario = request.form['comentario']
        fecha_ini = request.form['fecha-ini']

        id_espe = 1  # Reemplaza esto con el ID correcto del especialista

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
        # //

        _alimento = request.form.getlist('proteinas[]')

        print(_alimento)

        # FIXME: No está funcionando
        for alimento in _alimento:
            new_ac = AC(
                get_pac.id_paciente,
                id_espe,
                fecha_ini,
                alimento
            )
            db.session.add(new_ac)

            print("Registro de alimento agregado con exito")
            flash("Registro de alimento agregado con exito")
        # //

        db.session.commit()
        db.session.close()

        return redirect(url_for('paciente.inicio', id=id))
    
    return render_template('p_add_comida.html', id=id, get_pac=get_pac, get_prot=get_prot)
# // >

# Detalle de comida < FIXME:
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
# // > FIXME:



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