import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS REFORÇADO (CONTRASTE ALTO E CORES ECO-TECH)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Fundo Eco-Tech: Verde Floresta para Azul Petróleo */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0a2412 0%, #020c1a 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal */
[data-testid="stSidebar"] {
    background-color: #051405 !important;
    border-right: 2px solid #39ff14;
}

/* Forçar Texto Branco em tudo */
h1, h2, h3, p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #ffffff !important;
}

/* Logo GIGANTE Neon Pixel */
.logo-pixel-home {
    font-family: 'Press Start 2P', cursive !important;
    font-size: clamp(40px, 8vw, 70px);
    text-align: center;
    color: #39ff14 !important;
    padding: 40px 0;
    text-shadow: 0 0 20px #39ff14, 4px 4px #000;
}

.logo-interno {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 30px;
    color: #39ff14 !important;
    text-align: center;
    padding: 15px;
}

/* Botões Arcade */
.stButton > button {
    background-color: #000 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 12px !important;
    border-radius: 0px !important;
}

.stButton > button:hover {
    background-color: #39ff14 !important;
    color: #000 !important;
}

/* Cards de Informação */
.card-pixel {
    background: rgba(0, 0, 0, 0.7);
    border: 2px solid #39ff14;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Mensagem de Erro Vermelha */
.error-msg {
    color: #ff4b4b !important;
    font-weight: bold;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
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
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        <div class="card-pixel">
            <h2 style="color:#39ff14 !important; font-family:'Press Start 2P'; font-size:18px;">SOBRE A MISSÃO 🌍</h2>
            <p>O <b>EcoTech</b> é uma plataforma de tecnologia sustentável. Aqui, suas ações no mundo real viram progresso digital.</p>
            <p><b>O que você pode fazer:</b></p>
            <ul>
                <li>🚲 <b>Mobilidade:</b> Ganhe XP ao usar transporte sem emissão.</li>
                <li>📱 <b>Reciclagem:</b> Descarte eletrônicos e proteja o solo.</li>
                <li>🧠 <b>Bio-Quiz:</b> Aprenda e evolua sua patente ambiental.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("ACESSO AO SISTEMA")
        u = st.text_input("USUÁRIO", key="user_in")
        p = st.text_input("SENHA", type="password", key="pass_in")
        
        if st.button("START MISSION →"):
            try:
                res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.user_data = res.data[0]['dados_json']
                    st.rerun()
                else:
                    st.session_state.login_err = True
            except:
                st.error("Erro de conexão.")
        
        if st.session_state.login_err:
            st.markdown('<p class="error-msg">DADOS INCORRETOS!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ─── INTERFACE INTERNA ───
    with st.sidebar:
        st.markdown(f"### 👾 PLAYER: {st.session_state.username}")
        pts = st.session_state.user_data.get('pontos_totais', 0)
        st.write(f"Patente: **{obter_nivel(pts)}**")
        st.divider()
        menu = st.radio("SISTEMA:", ["PAINEL DE IMPACTO", "RANKING GLOBAL", "ECO-RADAR"])
        if st.button("SAIR DO SISTEMA"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<p class="logo-interno">ECOTECH</p>', unsafe_allow_html=True)

    if menu == "PAINEL DE IMPACTO":
        st.markdown("""
        <div style="background:rgba(57, 255, 20, 0.1); padding:10px; border-radius:10px; border-left: 5px solid #39ff14; margin-bottom:20px;">
            <p style="margin:0; font-size:14px;"><b>INFO:</b> Este é seu centro de comando. Registre suas missões diárias para converter esforço em XP e redução de CO2.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pts = st.session_state.user_data.get('pontos_totais', 0)
        c1, c2, c3 = st.columns(3)
        c1.metric("XP TOTAL", f"{pts} pts")
        c2.metric("CO2 EVITADO", f"{pts*0.1:.1f} kg")
        c3.metric("NÍVEL", obter_nivel(pts))

        st.markdown("---")
        st.subheader("🏃 MISSÕES DISPONÍVEIS")
        
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🚲 TRANSPORTE SUSTENTÁVEL"):
                st.write("Cada trajeto limpo diminui sua pegada de carbono.")
                if st.button("Bike/A pé (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.success("XP SALVO!")
                    st.rerun()
                if st.button("Bus/Metrô (+10 XP)"):
                    st.session_state.user_data['pontos_totais'] += 10
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()

        with col_b:
            with st.expander("🧠 QUIZ AMBIENTAL"):
                st.write("Teste seu conhecimento para bônus intelectuais.")
                if st.button("Responder Quiz (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                    st.rerun()

    elif menu == "RANKING GLOBAL":
        st.markdown("""
        <div style="background:rgba(57, 255, 20, 0.1); padding:10px; border-radius:10px; border-left: 5px solid #39ff14; margin-bottom:20px;">
            <p style="margin:0; font-size:14px;"><b>INFO:</b> O Hall da Fama mostra os defensores da natureza mais ativos. Compita de forma saudável para inspirar outros!</p>
        </div>
        """, unsafe_allow_html=True)
        res = supabase.table("usuarios").select("username, dados_json").execute()
        data = [{"Player": u['username'], "XP": u['dados_json']['pontos_totais']} for u in res.data]
        st.table(pd.DataFrame(data).sort_values("XP", ascending=False))

    elif menu == "ECO-RADAR":
        st.markdown("""
        <div style="background:rgba(57, 255, 20, 0.1); padding:10px; border-radius:10px; border-left: 5px solid #39ff14; margin-bottom:20px;">
            <p style="margin:0; font-size:14px;"><b>INFO:</b> Utilize o radar para encontrar pontos de descarte correto de eletrônicos e evitar contaminação do solo.</p>
        </div>
        """, unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}))
