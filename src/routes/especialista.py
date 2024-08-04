from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash
from src.database.db import db

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