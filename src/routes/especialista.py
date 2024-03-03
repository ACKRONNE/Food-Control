from flask import Blueprint, render_template

esp = Blueprint('especialista', __name__)

@esp.route('/Regisro_Especialista')
def registro():
    return render_template('e_registro.html')