from flask import Flask, jsonify
from flask_cors import CORS
from database import test_connection
from models import LinhaService, HorarioService, ParadaService

app = Flask(__name__)
CORS(app)

# Inicializar serviços
linha_service = LinhaService()
horario_service = HorarioService()
parada_service = ParadaService()

print("🚀 Inicializando Sistema de Ônibus VCG...")

# Testar conexão ao iniciar
if test_connection():
    print("✅ Tudo pronto! Servidor iniciando...")
else:
    print("❌ Problema na conexão com o banco!")

@app.route('/')
def home():
    return jsonify({
        "message": "🚍 Sistema de Ônibus VCG API",
        "status": "online",
        "rotas_disponiveis": [
            "/linhas",
            "/linhas/<id>/horarios", 
            "/paradas"
        ]
    })

@app.route('/linhas')
def get_linhas():
    """Retorna todas as linhas de ônibus"""
    try:
        linhas = linha_service.get_todas_linhas()
        return jsonify([linha.to_dict() for linha in linhas])
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar linhas: {str(e)}"}), 500

@app.route('/linhas/<int:linha_id>/horarios')
def get_horarios_linha(linha_id):
    """Retorna horários de uma linha específica"""
    try:
        # Verifica se a linha existe
        linha = linha_service.get_linha_por_id(linha_id)
        if not linha:
            return jsonify({"error": f"Linha {linha_id} não encontrada"}), 404
        
        horarios = horario_service.get_horarios_por_linha(linha_id)
        return jsonify([horario.to_dict() for horario in horarios])
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar horários: {str(e)}"}), 500

@app.route('/paradas')
def get_paradas():
    """Retorna todas as paradas"""
    try:
        paradas = parada_service.get_todas_paradas()
        return jsonify([parada.to_dict() for parada in paradas])
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar paradas: {str(e)}"}), 500

@app.route('/status')
def status():
    """Rota para verificar status do sistema"""
    linhas_count = len(linha_service.get_todas_linhas())
    paradas_count = len(parada_service.get_todas_paradas())
    
    return jsonify({
        "status": "online",
        "database": "connected" if test_connection() else "disconnected",
        "linhas_cadastradas": linhas_count,
        "paradas_cadastradas": paradas_count
    })

if __name__ == '__main__':
    print("=" * 50)
    print("📍 Servidor disponível em: http://127.0.0.1:5000")
    print("📍 Rotas disponíveis:")
    print("   - GET /          → Status da API")
    print("   - GET /linhas    → Lista de linhas")
    print("   - GET /linhas/1/horarios → Horários da linha 1")
    print("   - GET /paradas   → Lista de paradas")
    print("   - GET /status    → Status do sistema")
    print("=" * 50)
    app.run(debug=True)