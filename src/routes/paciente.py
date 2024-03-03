from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from sqlalchemy import and_, or_
from src.database.db import db
from datetime import datetime

# Entidades
from src.models.paciente import Paciente
from src.models.comida import Comida
from src.models.hist_comida import HistComida
# //

pac = Blueprint('paciente', __name__)

# Registrar nuevo paciente >
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
# // 


# Inicio del paciente
@pac.route('/inicio/<id>', methods=['GET', 'POST'])
def inicio(id):

    id = db.session.query(Paciente).filter(Paciente.id_paciente == id).first()

    date = datetime.now()
    formatted_date = date.strftime("%b. %d")
    
    if request.method == "POST":
        fecha_str = request.form['pac-fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        formatted_fecha = fecha.strftime('%B, %d %Y')

        # Aqui va la consulta que me muestra las comidas

        db.session.close()
        
        return render_template('ini_paciente.html', id=id, formatted_fecha=formatted_fecha, formatted_date=formatted_date)

    return render_template("p_inicio.html", id=id, formatted_date=formatted_date)
# //


# Perfil del Paciente
@pac.route('/perfil/<id>', methods=["GET"])
def perfil(id):
    
    id = db.session.query(Paciente.id_paciente).filter(Paciente.id_paciente == id).first()

    return render_template("perfil_paciente.html", id=id)
# //