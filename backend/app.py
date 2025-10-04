from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app)  # Permite comunicação com o front-end

# Configuração do banco
def get_db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'seu_usuario',
        password = 'sua_senha',
        database = 'transporte_vcg'
    )

# Rotas da API
@app.route('/')
def home():
    return jsonify({"message": "Sistema de Ônibus VCG API"})

# Buscar todas as linhas
@app.route('/linhas', methods=['GET'])
def get_linhas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM linhas")
    linhas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(linhas)

# Buscar horários de uma linha
@app.route('/linhas/<int:linha_id>/horarios', methods=['GET'])
def get_horarios_linha(linha_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM horarios 
        WHERE linha_id = %s 
        ORDER BY dia_semana, horario
    """, (linha_id,))
    horarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(horarios)

# Buscar paradas
@app.route('/paradas', methods=['GET'])
def get_paradas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paradas")
    paradas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(paradas)

if __name__ == '_main_':
    app.run(debug=True)