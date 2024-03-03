from flask import Blueprint, render_template

reg = Blueprint('registro', __name__)

@reg.route('/Registro')
def registro():
    return render_template('registro.html')