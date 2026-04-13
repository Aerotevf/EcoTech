import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client
import time

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech OS", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (ALTO CONTRASTE + ESTÉTICA TECH-GREEN)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

/* Fundo Escuro para Leitura Perfeita */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050a05 0%, #0d1a0d 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar com contraste */
[data-testid="stSidebar"] {
    background-color: #0d1a0d !important;
    border-right: 1px solid #22c55e;
}

/* Texto Branco em toda a aplicação */
h1, h2, h3, h4, h5, h6, p, li, span, label, .stMetric, [data-testid="stMarkdown"] {
    color: #ffffff !important;
}

/* Títulos em Verde Neon */
h1, h2, .logo-eco {
    font-family: 'Syne', sans-serif !important;
    color: #4ade80 !important;
    text-shadow: 0 0 10px rgba(74, 222, 128, 0.4);
}

/* Cards com transparência e borda neon */
.card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Botões Estilo Tecnologia */
.stButton > button {
    background: #166534 !important;
    color: white !important;
    border: 1px solid #4ade80 !important;
    width: 100%;
    border-radius: 8px !important;
    transition: 0.3s;
}

.stButton > button:hover {
    box-shadow: 0 0 15px rgba(74, 222, 128, 0.6) !important;
    background: #22c55e !important;
}

/* Ajuste das tabelas para fundo escuro */
[data-testid="stTable"] {
    background-color: rgba(255, 255, 255, 0.05);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
# Substitua com as suas credenciais reais
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DE NEGÓCIO ────────────────────────────────────────────────────────

def obter_emblema(pontos):
    if pontos >= 1000: return "👑 Guardião Master"
    elif pontos >= 500: return "✨ Eco Mestre"
    elif pontos >= 250: return "🌳 Árvore Jovem"
    elif pontos >= 100: return "🌿 Broto"
    return "🌱 Iniciante"

def carregar_ranking():
    res = supabase.table("usuarios").select("username, dados_json").execute()
    lista = []
    for u in res.data:
        pts = u['dados_json'].get('pontos_totais', 0)
        lista.append({"Emblema": obter_emblema(pts), "Usuário": u['username'], "Pontos": pts})
    return pd.DataFrame(lista).sort_values(by="Pontos", ascending=False)

def salvar_dados(username, dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", username).execute()

# ─── SISTEMA DE NAVEGAÇÃO & LOGIN ─────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🌿 ECOTECH OS")
    aba = st.tabs(["Login", "Criar Conta", "Recuperar Senha"])
    
    with aba[0]:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Acessar Painel"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else: st.error("Dados incorretos.")
            
    with aba[2]:
        user_reset = st.text_input("Seu Usuário para Reset")
        nova_pw = st.text_input("Nova Senha Temporária", type="password")
        if st.button("Redefinir Senha"):
            supabase.table("usuarios").update({"password": nova_pw}).eq("username", user_reset).execute()
            st.success("Senha atualizada com sucesso!")

else:
    # ─── INTERFACE LOGADA ───
    with st.sidebar:
        st.markdown(f"### 👾 Olá, {st.session_state.username}")
        st.write(f"Nível: {obter_emblema(st.session_state.user_data['pontos_totais'])}")
        st.divider()
        
        # Menu por botões visíveis (Abas)
        if st.button("📊 Meu Dashboard"): st.session_state.menu = "Dash"
        if st.button("🏆 Ranking Global"): st.session_state.menu = "Rank"
        if st.button("🚀 Jogo: Eco-Flappy"): st.session_state.menu = "Game"
        
        # Logout no final
        for _ in range(10): st.write("") # Espaçador
        if st.button("Sair / Logout", type="primary"):
            st.session_state.logged_in = False
            st.rerun()

    # Definir aba padrão
    if 'menu' not in st.session_state: st.session_state.menu = "Dash"

    if st.session_state.menu == "Dash":
        st.header("📊 Seu Impacto Real")
        col1, col2, col3 = st.columns(3)
        pts = st.session_state.user_data['pontos_totais']
        col1.metric("Pontos", f"{pts} pts")
        col2.metric("CO₂ Evitado", f"{pts*0.1:.1f} kg")
        col3.metric("Emblema", obter_emblema(pts))
        
        st.markdown('<div class="card"><h3>Ações Rápidas</h3>', unsafe_allow_html=True)
        if st.button("🚲 Fui de Bicicleta (+20 pts)"):
            st.session_state.user_data['pontos_totais'] += 20
            salvar_dados(st.session_state.username, st.session_state.user_data)
            st.toast("Pontos computados!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.menu == "Rank":
        st.header("🏆 Melhores do Mundo")
        df = carregar_ranking()
        st.table(df)

    elif st.session_state.menu == "Game":
        st.header("🚀 Eco-Flappy Bird")
        st.write("Desvie das nuvens de fumaça! (Versão Beta)")
        
        col_g1, col_g2 = st.columns([3, 1])
        with col_g1:
            # Lógica simples de voo para teste
            if 'score_local' not in st.session_state: st.session_state.score_local = 0
            st.code(f"Pontuação atual no jogo: {st.session_state.score_local}\n\n     🚀\n\n💨       💨")
            if st.button("VOAR! 🚀"):
                st.session_state.score_local += 1
                if st.session_state.score_local % 5 == 0:
                    st.session_state.user_data['pontos_totais'] += 1
                    salvar_dados(st.session_state.username, st.session_state.user_data)
                    st.toast("Você ganhou +1 ponto real por habilidade!")
        with col_g2:
            st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
            st.markdown(f"<h5>Pontos Ganhos</h5>", unsafe_allow_html=True)
            st.markdown(f"<h1>{st.session_state.score_local}</h1>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
