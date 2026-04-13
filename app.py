import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (MIX ECO + TECH)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d1b11 0%, #1a2e1a 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Títulos com brilho tech */
h1, h2, h3, .logo-eco {
    font-family: 'Syne', sans-serif !important;
    color: #4ade80 !important;
    text-shadow: 0 0 15px rgba(74, 222, 128, 0.3);
}

.card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(74, 222, 128, 0.2);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* Botões Estilo Tech */
.stButton > button {
    background: linear-gradient(90deg, #2d7a3a, #1a4d2e) !important;
    color: white !important;
    border: 1px solid #4ade80 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: 0.3s all !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(74, 222, 128, 0.4);
}

/* Estilo para os Desafios que estava bugado */
.challenge-box {
    background: rgba(0,0,0,0.2);
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    border-left: 4px solid #4ade80;
}
</style>
""", unsafe_allow_html=True)

# ─── SUPABASE ──────────────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DE DADOS ──────────────────────────────────────────────────────────

def carregar_ranking():
    res = supabase.table("usuarios").select("username, dados_json").execute()
    lista = []
    for u in res.data:
        pontos = u['dados_json'].get('pontos_totais', 0)
        lista.append({"Usuário": u['username'], "Pontos": pontos})
    return pd.DataFrame(lista).sort_values(by="Pontos", ascending=False)

def redefinir_senha(user, nova_senha):
    res = supabase.table("usuarios").update({"password": nova_senha}).eq("username", user).execute()
    return len(res.data) > 0

# (Mantendo funções de carregar/salvar dados iguais às anteriores para não quebrar o banco)
def carregar_dados_usuario(username):
    res = supabase.table("usuarios").select("dados_json").eq("username", username).execute()
    return res.data[0]["dados_json"] if res.data else {"pontos_totais": 0, "historico": []}

def salvar_dados_usuario(username, user_data):
    supabase.table("usuarios").update({"dados_json": user_data}).eq("username", username).execute()

# ─── INTERFACE ────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🌿 ECOTECH OS")
    aba = st.radio("Selecione", ["Login", "Criar Conta", "Esqueci a Senha"], horizontal=True)
    
    if aba == "Login":
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Acessar Sistema"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else: st.error("Acesso negado.")

    elif aba == "Esqueci a Senha":
        u = st.text_input("Seu Usuário")
        nova = st.text_input("Nova Senha", type="password")
        if st.button("Atualizar Senha"):
            if redefinir_senha(u, nova): st.success("Senha alterada! Vá para Login.")
            else: st.error("Usuário não encontrado.")

else:
    # SISTEMA LOGADO
    st.sidebar.title(f"👾 {st.session_state.username}")
    menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Ranking Global", "Desafios"])
    
    if menu == "Dashboard":
        col1, col2, col3 = st.columns(3)
        col1.metric("Pontos", st.session_state.user_data.get('pontos_totais', 0))
        col2.metric("CO₂ Evitado", f"{st.session_state.user_data.get('pontos_totais', 0) * 0.1:.1f}kg")
        col3.metric("Nível", "Semente")
        
        st.markdown('<div class="card"><h3>⚡ Ações Rápidas</h3>', unsafe_allow_html=True)
        if st.button("🚲 Fui de Bike (+20 pts)"):
            st.session_state.user_data['pontos_totais'] += 20
            salvar_dados_usuario(st.session_state.username, st.session_state.user_state)
            st.toast("Ponto computado!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "Ranking Global":
        st.subheader("🏆 Leaderboard EcoTech")
        df = carregar_ranking()
        st.table(df)

    elif menu == "Desafios":
        st.subheader("🎯 Missões da Semana")
        st.markdown('<div class="challenge-box">✅ <b>Missão 1:</b> Registre 5 ações (50 pts)</div>', unsafe_allow_html=True)
        st.markdown('<div class="challenge-box">🔒 <b>Missão 2:</b> Convide um amigo (100 pts)</div>', unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
