// URL da API Flask
const API_URL = 'http://127.0.0.1:5000';

// Carregar linhas quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    carregarLinhas();
    carregarParadas();
});

// Função para carregar linhas de ônibus
async function carregarLinhas() {
    try {
        const response = await fetch(`${API_URL}/linhas`);
        const linhas = await response.json();
        
        const container = document.getElementById('linhas-container');
        container.innerHTML = '';
        
        linhas.forEach(linha => {
            const linhaCard = document.createElement('div');
            linhaCard.className = 'linha-card';
            linhaCard.onclick = () => mostrarHorarios(linha);
            
            linhaCard.innerHTML = `
                <div class="linha-numero">Linha ${linha.numero}</div>
                <div class="linha-nome">${linha.nome}</div>
                <div class="linha-rota">${linha.origem} → ${linha.destino}</div>
            `;
            
            container.appendChild(linhaCard);
        });
    } catch (error) {
        console.error('Erro ao carregar linhas:', error);
    }
}

// Função para mostrar horários de uma linha
async function mostrarHorarios(linha) {
    try {
        const response = await fetch(`${API_URL}/linhas/${linha.id}/horarios`);
        const horarios = await response.json();
        
        // Mostrar seção de horários
        document.getElementById('linhas-section').style.display = 'none';
        document.getElementById('horarios-section').style.display = 'block';
        document.getElementById('paradas-section').style.display = 'none';
        
        // Atualizar nome da linha
        document.getElementById('linha-nome').textContent = `${linha.numero} - ${linha.nome}`;
        
        // Agrupar horários por dia da semana
        const horariosPorDia = agruparHorariosPorDia(horarios);
        
        const container = document.getElementById('horarios-container');
        container.innerHTML = '';
        
        // Criar cards para cada dia
        for (const [dia, horariosDia] of Object.entries(horariosPorDia)) {
            const diaCard = document.createElement('div');
            diaCard.className = 'dia-card';
            diaCard.innerHTML = `
                <h3>${formatarDiaSemana(dia)}</h3>
                <div class="horarios-lista">
                    ${horariosDia.map(horario => `
                        <span class="horario-badge">${horario.horario}</span>
                    `).join('')}
                </div>
            `;
            container.appendChild(diaCard);
        }
    } catch (error) {
        console.error('Erro ao carregar horários:', error);
    }
}

// Função para carregar paradas
async function carregarParadas() {
    try {
        const response = await fetch(`${API_URL}/paradas`);
        const paradas = await response.json();
        
        const container = document.getElementById('paradas-container');
        container.innerHTML = '';
        
        paradas.forEach(parada => {
            const paradaItem = document.createElement('div');
            paradaItem.className = 'parada-item';
            paradaItem.innerHTML = `
                <strong>${parada.nome}</strong>
                <p>${parada.endereco || 'Endereço não informado'}</p>
            `;
            container.appendChild(paradaItem);
        });
    } catch (error) {
        console.error('Erro ao carregar paradas:', error);
    }
}

// Função para voltar para a lista de linhas
function voltarParaLinhas() {
    document.getElementById('linhas-section').style.display = 'block';
    document.getElementById('horarios-section').style.display = 'none';
    document.getElementById('paradas-section').style.display = 'block';
}

// Funções auxiliares
function agruparHorariosPorDia(horarios) {
    const agrupados = {};
    horarios.forEach(horario => {
        if (!agrupados[horario.dia_semana]) {
            agrupados[horario.dia_semana] = [];
        }
        agrupados[horario.dia_semana].push(horario);
    });
    return agrupados;
}

function formatarDiaSemana(dia) {
    const dias = {
        'segunda': 'Segunda-feira',
        'terca': 'Terça-feira',
        'quarta': 'Quarta-feira',
        'quinta': 'Quinta-feira',
        'sexta': 'Sexta-feira',
        'sabado': 'Sábado',
        'domingo': 'Domingo'
    };
    return dias[dias] || dia;
}