import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client
import time

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech OS", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (SUPER CONSTRASTE + TECH-GREEN)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

/* Fundo Escuro para Máximo Contraste */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0f0a 0%, #1a2e1a 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Clara e Limpa */
[data-testid="stSidebar"] {
    background-color: #f0f7f0 !important;
    border-right: 1px solid #d1e7d1;
}

/* Tipografia Geral - Branca para Leitura Perfeita */
h1, h2, h3, h4, h5, h6, p, li, span, label, .stMetric, [data-testid="stMarkdown"] {
    font-family: 'DM Sans', sans-serif !important;
    color: #ffffff !important;
}

/* Títulos com Brilho Neon Green */
h1, h2, .logo-eco {
    font-family: 'Syne', sans-serif !important;
    color: #4ade80 !important;
    text-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
}

/* Texto de Descrição em Verde Mais Suave */
[data-testid="stMarkdown"] p, .stCaption {
    color: #a7f3d0 !important;
}

/* Cards com Efeito de Vidro */
.card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(5px);
}

/* Botões Estilo Tech com Glow */
.stButton > button {
    background: linear-gradient(90deg, #166534, #14532d) !important;
    color: white !important;
    border: 1px solid #4ade80 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: 0.3s all !important;
    text-shadow: 0 0 5px rgba(255,255,255,0.5);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 15px rgba(74, 222, 128, 0.4) !important;
    border-color: #ffffff !important;
}

/* Inputs com Contraste Alto */
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] select {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #ffffff !important;
    border: 1px solid #a7f3d0 !important;
    border-radius: 8px !important;
}

/* Ajuste das Abas de Navegação Visíveis */
[data-testid="stHorizontalBlock"] button {
    background-color: #f0f7f0 !important;
    color: #1a2e1a !important;
    border: 1px solid #d1e7d1 !important;
    border-radius: 8px !important;
    margin: 5px !important;
}
[data-testid="stHorizontalBlock"] button[aria-selected="true"] {
    background-color: #22c55e !important;
    color: white !important;
    border-color: #22c55e !important;
}

/* Tabela de Ranking com Letras Brancas */
[data-testid="stTable"] table {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    border-radius: 10px;
}
[data-testid="stTable"] thead tr th {
    color: #4ade80 !important;
    border-bottom: 2px solid #4ade80 !important;
}
[data-testid="stTable"] tbody tr td {
    border-bottom: 1px solid rgba(74, 222, 128, 0.1) !important;
}

/* Esconder elementos padrões */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── SUPABASE ──────────────────────────────────────────────────────────────────
# ADICIONE SUAS CHAVES AQUI
URL_DB = "SUA_URL_DO_SUPABASE"
KEY_DB = "SUA_KEY_DO_SUPABASE"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DE DADOS & JOGO ───────────────────────────────────────────────────

# Configuração de Emblemas baseados em pontos
def obter_emblema(pontos):
    if pontos >= 1000: return "👑 Guardião Master"
    elif pontos >= 500: return "✨ Eco Mestre"
    elif pontos >= 250: return "🌳 Árvore Jovem"
    elif pontos >= 100: return "🌿 Broto"
    return "🌱 Iniciante"

def carregar_ranking_com_emblemas():
    try:
        res = supabase.table("usuarios").select("username, dados_json").execute()
        lista = []
        for u in res.data:
            pontos = u['dados_json'].get('pontos_totais', 0)
            emblema = obter_emblema(pontos)
            lista.append({"Emblema": emblema, "Usuário": u['username'], "Pontos": pontos})
        return pd.DataFrame(lista).sort_values(by="Pontos", ascending=False)
    except: return pd.DataFrame(columns=["Emblema", "Usuário", "Pontos"])

def salvar_dados_usuario(username, user_data):
    try:
        supabase.table("usuarios").update({"dados_json": user_data}).eq("username", username).execute()
    except: st.error("Erro ao salvar dados.")

# Inicializar variáveis do Jogo Eco-Flappy
def inicializar_jogo():
    if 'game_active' not in st.session_state: st.session_state.game_active = False
    if 'game_score' not in st.session_state: st.session_state.game_score = 0
    if 'player_y' not in st.session_state: st.session_state.player_y = 50
    if 'obstacles' not in st.session_state: st.session_state.obstacles = []

# Lógica principal do Jogo Eco-Flappy
def run_eco_flappy():
    inicializar_jogo()
    
    col_j1, col_j2 = st.columns([3, 1])
    
    with col_j1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚀 Eco-Flappy Bird")
        st.caption("Clique no botão 'VOAR' para desviar das nuvens de poluição (💨). Cada nuvem que passar vale +1 ponto real!")
        
        game_area = st.empty()
        
        if not st.session_state.game_active:
            game_area.info("Pressione 'INICIAR JOGO' para começar.")
            if st.button("INICIAR JOGO →", use_container_width=True):
                st.session_state.game_active = True
                st.session_state.game_score = 0
                st.session_state.player_y = 50
                st.session_state.obstacles = []
                st.rerun()
        else:
            # Mecânica do Jogo (Simplificada para Streamlit)
            st.session_state.player_y = max(0, st.session_state.player_y + 8) # Gravidade
            
            # Adicionar obstáculos
            if random.random() < 0.1: # 10% de chance de gerar nuvem
                gap_y = random.randint(10, 80)
                st.session_state.obstacles.append({'x': 100, 'gap_y': gap_y})
                
            # Mover obstáculos e checar colisão/pontuação
            new_obstacles = []
            scored_this_frame = False
            for obs in st.session_state.obstacles:
                obs['x'] -= 10 # Velocidade do obstáculo
                if obs['x'] > -10:
                    new_obstacles.append(obs)
                
                # Checar Colisão
                if 10 < obs['x'] < 25: # Posição X do jogador
                    player_y = st.session_state.player_y
                    if not (obs['gap_y'] - 15 < player_y < obs['gap_y'] + 15):
                        st.session_state.game_active = False
                        # Registrar pontos ganhos no Supabase
                        if st.session_state.game_score > 0:
                            st.session_state.user_data['pontos_totais'] += st.session_state.game_score
                            st.session_state.user_data['historico'].append({
                                "Ação": f"Eco-Flappy 🚀 (Score: {st.session_state.game_score})",
                                "Pontos": st.session_state.game_score,
                                "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M")
                            })
                            salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
                            st.success(f"🎮 Jogo finalizado! Você ganhou +{st.session_state.game_score} pontos reais.")
                        game_area.error(f"💥 Bateu na poluição! Pontuação final do jogo: {st.session_state.game_score}")
                        st.rerun()

                # Checar Pontuação
                if obs['x'] == 10 and not scored_this_frame:
                    st.session_state.game_score += 1
                    scored_this_frame = True
            
            st.session_state.obstacles = new_obstacles
            
            # Renderizar Jogo (Texto Art 8-bit)
            game_text = ""
            for y in range(0, 101, 10):
                line = ""
                for x in range(0, 101, 5):
                    is_player = (x == 15 and y == st.session_state.player_y)
                    is_obs = False
                    for obs in st.session_state.obstacles:
                        if x == obs['x'] and not (obs['gap_y'] - 15 < y < obs['gap_y'] + 15):
                            is_obs = True
                    
                    if is_player: line += "🚀"
                    elif is_obs: line += "💨"
                    else: line += "░░"
                game_text += line + "\n"
            game_area.code(game_text, language=None)
            time.sleep(0.3) # Controle de velocidade
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col_j2:
        st.markdown(f'<div class="card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(f"<h5>Score do Jogo</h5>",
