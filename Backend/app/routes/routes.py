from flask import Blueprint, render_template
from flask import request
from ..modules.calcular import simular_epidemia
import numpy as np
import time
import os
from werkzeug.utils import secure_filename
main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template("simulador_epidemias.html")

@main.route("/simular", methods=["POST"])
def simular():
    data = request.get_json()
    campos_requeridos = ['N', 'I0', 'p_vac', 'dias', 'beta', 'gamma',
                        'dia_intervencion', 'factor_intervencion']
    faltantes = [c for c in campos_requeridos if data.get(c) is None]
    if faltantes:
        return jsonify({'error': f'Faltan campos requeridos: {faltantes}'}), 400
    
    try:
        resultado = simular_epidemia(
			N                  = float(data['N']),
			I0                 = float(data['I0']),
			p_vac              = float(data['p_vac']),
			dias               = int(data['dias']),
			beta               = float(data['beta']),
			gamma              = float(data['gamma']),
			dia_intervencion   = int(data['dia_intervencion']),
			factor_intervencion= float(data['factor_intervencion']),
		)
        return resultado
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except RuntimeError as re:
        return jsonify({'error': str(re)}), 500