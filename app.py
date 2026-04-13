import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS REFORÇADO (CONTRASTE EXTREMO)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Fundo de segurança caso a animação falhe */
[data-testid="stAppViewContainer"] {
    background-color: #050a05 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal */
[data-testid="stSidebar"] {
    background-color: #001a00 !important;
    border-right: 2px solid #39ff14;
}

/* Forçar Cor Branca e Contraste em tudo */
h1, h2, h3, p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #ffffff !important;
    text-shadow: 1px 1px 2px #000;
}

/* Logo GIGANTE Neon */
.logo-pixel-home {
    font-family: 'Press Start 2P', cursive !important;
    font-size: clamp(30px, 8vw, 80px);
    text-align: center;
    color: #39ff14 !important;
    padding: 40px 0;
    text-shadow: 0 0 20px #39ff14, 4px 4px #000;
}

/* Botões Arcade */
.stButton > button {
    background-color: #000 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 14px !important;
    box-shadow: 4px 4px 0px #052b05;
}

.card-pixel {
    background: rgba(0, 20, 0, 0.9);
    border: 2px solid #39ff14;
    padding: 25px;
    border-radius: 10px;
}

/* Mensagem de Erro Vermelha */
.error-msg {
    color: #ff3333;
    font-weight: bold;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─── ANIMAÇÃO DE FUNDO ────────────────────────────────────────────────────────
st.markdown("""
<canvas id="canvas" style="position:fixed; top:0; left:0; z-index:-1;"></canvas>
<script>
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;
    var texts = '01🌿'.split('');
    var fontSize = 16;
    var columns = canvas.width / fontSize;
    var drops = [];
    for (var x = 0; x < columns; x++) drops[x] = 1;
    function draw() {
        ctx.fillStyle = 'rgba(5, 10, 5, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#39ff14';
        ctx.font = fontSize + 'px arial';
        for (var i = 0; i < drops.length; i++) {
            var text = texts[Math.floor(Math.random() * texts.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 40);
</script>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'login_error' not in st.session_state: st.session_state.login_error = False

# TELA DE LOGIN
if not st.session_state.logged_in:
    st.markdown('<p class="logo-pixel-home">ECOTECH</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card-pixel"><h3>📖 MISSÃO</h3><p>Proteja a biosfera e ganhe XP.</p></div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("LOGIN")
        u = st.text_input("USER")
        p = st.text_input("PASS", type="password")
        if st.button("START →"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else:
                st.session_state.login_error = True
        
        if st.session_state.login_error:
            st.markdown('<p class="error-msg">LOGIN INVÁLIDO!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # SISTEMA LOGADO
    with st.sidebar:
        st.markdown(f"### 👾 PLAYER: {st.session_state.username}")
        pts = st.session_state.user_data['pontos_totais']
        st.write(f"Nível: {pts}")
        st.divider()
        menu = st.radio("SISTEMA:", ["PAINEL", "RANKING", "MAPA"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<p class="logo-pixel-home" style="font-size:40px; padding:10px;">ECOTECH</p>', unsafe_allow_html=True)

    if menu == "PAINEL":
        st.subheader("Missões e Status")
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            with st.expander("🚲 TRANSPORTE"):
                if st.button("BIKE/PÉ (+15 XP)"):
                    st.session_state.user_data['pontos_totais'] += 15
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.success("XP SALVO!")
                    st.rerun()
                if st.button("BUS/METRÔ (+10 XP)"):
                    st.session_state.user_data['pontos_totais'] += 10
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()
        
        with col_m2:
            with st.expander("🧠 QUIZ DIÁRIO"):
                st.write("Reciclar papel salva árvores?")
                if st.button("SIM (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()
