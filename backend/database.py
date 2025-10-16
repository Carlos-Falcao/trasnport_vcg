from supabase import create_client
import os

# Configurações do Supabase
SUPABASE_URL = "https://yhjxfyuwizullwyzbwpj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InloanhmeXV3aXp1bGx3eXpid3BqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NTA1MjUsImV4cCI6MjA3NjAyNjUyNX0.ueA8KUm2EZnJ51EUaDut0Cd0EvJXzQ11Zulk8ScdVII"

# Cliente Supabase global
_supabase_client = None

def get_supabase_client():
    """Retorna o cliente Supabase (singleton)"""
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Cliente Supabase inicializado!")
        except Exception as e:
            print(f"❌ Erro ao conectar com Supabase: {e}")
            raise
    return _supabase_client

def test_connection():
    """Testa a conexão com o Supabase"""
    try:
        client = get_supabase_client()
        # Testa com uma consulta simples
        result = client.table('linhas').select('id').limit(1).execute()
        print("✅ Conexão com Supabase está funcionando!")
        return True
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        return False