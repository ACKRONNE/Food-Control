from flask import Flask
from src.database.db import db

# Objetos de las rutas
from src.routes.index import ind
from src.routes.paciente import pac
from src.routes.especialista import esp

# Librerias para el funcionamiento
from dotenv import load_dotenv
import os
# //

load_dotenv()

app = Flask(__name__)

# Settings de la DB
key = os.environ['SECRETKEY']
config = os.environ['MYSQLCONFIG']

app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# //

# inicializar la aplicacion con la base de datos
db.init_app(app)
# //

app.register_blueprint(ind)
app.register_blueprint(pac)
app.register_blueprint(esp)
