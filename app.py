import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS ESTABILIZADO (MÁXIMO CONTRASTE)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Fundo Verde-Escuro Fixo (Sem JavaScript para não dar erro) */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #051a05 0%, #000000 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 2px solid #39ff14;
}

/* Forçar Texto Branco em tudo */
h1, h2, h3, p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #ffffff !important;
}

/* Logo GIGANTE Neon Pixel */
.logo-pixel-home {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 70px;
    text-align: center;
    color: #39ff14 !important;
    padding: 50px 0;
    text-shadow: 0 0 20px #39ff14, 4px 4px #000;
}

.logo-interno {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 30px;
    color: #39ff14 !important;
    text-align: center;
    padding: 20px;
}

/* Botões Arcade */
.stButton > button {
    background-color: #001a00 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 12px !important;
    width: 100%;
    margin-bottom: 10px;
}

.stButton > button:hover {
    background-color: #39ff14 !important;
    color: #000 !important;
}

/* Cards de Informação */
.card-pixel {
    background: rgba(0, 30, 0, 0.8);
    border: 2px solid #39ff14;
    padding: 25px;
    border-radius: 10px;
}

/* Mensagem de Erro Vermelha */
.error-msg {
    color: #ff4b4b !important;
    font-weight: bold;
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DO SISTEMA ────────────────────────────────────────────────────────
def obter_nivel(p):
    if p >= 500: return "👑 Guardião"
    if p >= 250: return "🌳 Árvore"
    return "🌱 Semente"

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'login_err' not in st.session_state: st.session_state.login_err = False

# ─── TELA DE ACESSO ───────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown('<p class="logo-pixel-home">ECOTECH</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="card-pixel">
        <h3 style="color:#39ff14 !important;">O QUE É O ECOTECH? 🌍</h3>
        <p>Somos uma plataforma que usa tecnologia para monitorar seu impacto ambiental.</p>
        <p><b>Missões:</b> Registre suas atividades de transporte sustentável e descarte de eletrônicos para ganhar XP e subir de nível!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("PLAYER LOGIN")
        u = st.text_input("USUÁRIO", key="user_in")
        p = st.text_input("SENHA", type="password", key="pass_in")
        if st.button("START →"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else:
                st.session_state.login_err = True
        
        if st.session_state.login_err:
            st.markdown('<p class="error-msg">DADOS INCORRETOS!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ─── INTERFACE INTERNA ───
    with st.sidebar:
        st.markdown(f"### 👾 PLAYER: {st.session_state.username}")
        pts = st.session_state.user_data['pontos_totais']
        st.write(f"Nível: {obter_nivel(pts)} ({pts} XP)")
        st.divider()
        menu = st.radio("SELECIONE A FASE:", ["PAINEL DE IMPACTO", "RANKING GLOBAL", "ONDE DESCARTAR"])
        if st.button("SAIR DO SISTEMA"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<p class="logo-interno">ECOTECH</p>', unsafe_allow_html=True)

    if menu == "PAINEL DE IMPACTO":
        st.subheader("Suas Estatísticas e Missões")
        pts = st.session_state.user_data['pontos_totais']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("XP ATUAL", f"{pts} pts")
        c2.metric("CO2 EVITADO", f"{pts*0.1:.1f} kg")
        c3.metric("PATENTE", obter_nivel(pts))

        st.markdown("---")
        st.subheader("🏃 MISSÕES DISPONÍVEIS")
        
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🚲 TRANSPORTE SUSTENTÁVEL"):
                st.write("Registre como você se locomoveu hoje:")
                if st.button("Fui de Bike/A pé (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.success("XP SALVO!")
                    st.rerun()
                if st.button("Ônibus/Metrô (+10 XP)"):
                    st.session_state.user_data['pontos_totais'] += 10
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()

        with col_b:
            with st.expander("🧠 DESAFIO QUIZ"):
                st.write("Reciclar eletrônicos evita contaminação do solo?")
                if st.button("SIM! (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()

    elif menu == "RANKING GLOBAL":
        st.subheader("Hall da Fama")
        res = supabase.table("usuarios").select("username, dados_json").execute()
        data = [{"Player": u['username'], "XP": u['dados_json']['pontos_totais']} for u in res.data]
        st.table(pd.DataFrame(data).sort_values("XP", ascending=False))

    elif menu == "ONDE DESCARTAR":
        st.subheader("Mapa de Descarte")
        st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}))
