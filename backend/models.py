class Linha:
    def __init__(self, id, numero, nome, origem, destino):
        self.id = id
        self.numero = numero
        self.nome = nome
        self.origem = origem
        self.destino = destino
    
    def to_dict(self):
        """Converte para dicionário (JSON)"""
        return {
            'id': self.id,
            'numero': self.numero,
            'nome': self.nome,
            'origem': self.origem,
            'destino': self.destino
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria Linha a partir de dicionário do Supabase"""
        return cls(
            id=data['id'],
            numero=data['numero'],
            nome=data['nome'],
            origem=data['origem'],
            destino=data['destino']
        )
    
    def __repr__(self):
        return f"Linha({self.numero}: {self.origem} → {self.destino})"

class Horario:
    def __init__(self, id, linha_id, dia_semana, horario):
        self.id = id
        self.linha_id = linha_id
        self.dia_semana = dia_semana
        self.horario = horario
    
    def to_dict(self):
        return {
            'id': self.id,
            'linha_id': self.linha_id,
            'dia_semana': self.dia_semana,
            'horario': self.horario
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            linha_id=data['linha_id'],
            dia_semana=data['dia_semana'],
            horario=data['horario']
        )
    
    def __repr__(self):
        return f"Horario({self.dia_semana} {self.horario})"

class Parada:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco or 'Endereço não informado'
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            nome=data['nome'],
            endereco=data.get('endereco')  # .get() para evitar erro se não existir
        )
    
    def __repr__(self):
        return f"Parada({self.nome})"

# Serviços de banco de dados
class LinhaService:
    def __init__(self):
        from database import get_supabase_client
        self.supabase = get_supabase_client()
    
    def get_todas_linhas(self):
        """Busca todas as linhas do banco"""
        try:
            response = self.supabase.table('linhas').select('*').execute()
            return [Linha.from_dict(linha) for linha in response.data]
        except Exception as e:
            print(f"❌ Erro ao buscar linhas: {e}")
            return []
    
    def get_linha_por_id(self, linha_id):
        """Busca uma linha específica por ID"""
        try:
            response = self.supabase.table('linhas').select('*').eq('id', linha_id).execute()
            if response.data:
                return Linha.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar linha {linha_id}: {e}")
            return None

class HorarioService:
    def __init__(self):
        from database import get_supabase_client
        self.supabase = get_supabase_client()
    
    def get_horarios_por_linha(self, linha_id):
        """Busca horários de uma linha específica"""
        try:
            response = self.supabase.table('horarios')\
                .select('*')\
                .eq('linha_id', linha_id)\
                .execute()
            return [Horario.from_dict(horario) for horario in response.data]
        except Exception as e:
            print(f"❌ Erro ao buscar horários da linha {linha_id}: {e}")
            return []

class ParadaService:
    def __init__(self):
        from database import get_supabase_client
        self.supabase = get_supabase_client()
    
    def get_todas_paradas(self):
        """Busca todas as paradas"""
        try:
            response = self.supabase.table('paradas').select('*').execute()
            return [Parada.from_dict(parada) for parada in response.data]
        except Exception as e:
            print(f"❌ Erro ao buscar paradas: {e}")
            return []