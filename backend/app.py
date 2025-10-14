from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client
import os

app = Flask(__name__)
CORS(app)

# Configuração do Supabase
SUPABASE_URL = "https://yhjxfyuwizullwyzbwpj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InloanhmeXV3aXp1bGx3eXpid3BqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTA1MjUsImV4cCI6MjA3NjAyNjUyNX0.ueA8KUm2EZnJ51EUaDut0Cd0EvJXzQ11Zulk8ScdVII"

# Inicializar cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("✅ Supabase configurado!")

@app.route('/')
def home():
    return jsonify({"message": "Sistema de Ônibus VCG API com Supabase!"})

@app.route('/linhas')
def get_linhas():
    try:
        # Buscar todas as linhas
        response = supabase.table('linhas').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/linhas/<int:linha_id>/horarios')
def get_horarios_linha(linha_id):
    try:
        # Buscar horários de uma linha específica
        response = supabase.table('horarios')\
            .select('*')\
            .eq('linha_id', linha_id)\
            .execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/paradas')
def get_paradas():
    try:
        # Buscar todas as paradas
        response = supabase.table('paradas').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor iniciando...")
    app.run(debug=True)