from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from src.database.db import db


# Entidades
from src.models.models import Paciente, Especialista, Alimento, Comida, AC
# //

ind = Blueprint('index', __name__)

# Pagina principal <
@ind.route('/')
def index():
    return render_template('index.html')
# // >

# Tipo de usuario <
@ind.route('/registro')
def registro():
    return render_template('registro.html')
# // >

# Iniciar sesion <
@ind.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        _correo = request.form['ind-correo']
        _clave = request.form['ind-clave']

        # Check if the user exists in the database
        account = db.session.query(Paciente.id_paciente, Paciente.clave).filter(Paciente.correo == _correo).first()
        
        # if account and check_password_hash(account.clave, _clave):
        #     session['logueado'] = True
        #     session['id'] = account.id_paciente
        #     _id = session['id']
            
        #     return redirect(url_for('paciente.inicio', id=_id))
        if account: # Temporal para hacer pruebas sin seguridad
            session['logueado'] = True
            session['id'] = account.id_paciente
            _id = session['id']
        
            return redirect(url_for('paciente.inicio', id=_id))


        else:    
            account = db.session.query(Especialista.id_espe, Especialista.clave).filter(Especialista.correo == _correo).first()

            # if account and check_password_hash(account.clave, _clave):
            #     session['logueado'] = True
            #     session['id'] = account.id_empleado
            #     _id = session['id']
            #     return redirect(url_for('especialista.inicio', id=_id))
            if account: # Temporal para hacer pruebas sin seguridad
                session['logueado'] = True
                session['id'] = account.id_espe
                _id = session['id']
            
                return redirect(url_for('especialista.inicio', id=_id))            
            else:
                return render_template('login.html', mensaje = 'El usuario no se encuentra registrado o la contraseña es incorrecta')

    else:
        return render_template('login.html')
# // >

# Cerrar sesion del usuario <
@ind.route('/logout/<id>', methods=['GET'])
def logout(id):
    
    user = Paciente.query.get(id)

    if user is None:
        return "Usuario no encontrado"

    if (user.id_paciente == int(id) or user.id_empleado == int(id)):
        session.pop('id', None)
        session.clear()
        return redirect(url_for('index.index'))
    else:
        return "Error 404, No se pudo cerrar la sesion"
# // >


# TODO: Falta recuperar contraseña

