import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (ALTO CONTRASTE: VERDE + CINZA DARK)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700&family=DM+Sans:wght@400;700&display=swap');

/* Fundo Cinza Tecnológico Escuro */
[data-testid="stAppViewContainer"] {
    background-color: #0e1111 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Verde Escura */
[data-testid="stSidebar"] {
    background-color: #0a2412 !important;
    border-right: 2px solid #22c55e;
}

/* Textos em Branco e Verde Água para leitura */
h1, h2, h3, h4, p, span, label, .stMetric {
    color: #ffffff !important;
}

.logo-eco {
    font-family: 'Syne', sans-serif !important;
    color: #22c55e !important;
    font-size: 50px;
    font-weight: 800;
}

/* Botões que se destacam */
.stButton > button {
    background-color: #166534 !important;
    color: white !important;
    border: 2px solid #22c55e !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #22c55e !important;
    color: #0e1111 !important;
}

/* Cards de Informação */
.card-home {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid #22c55e;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Tabela de Ranking */
[data-testid="stTable"] {
    background-color: transparent !important;
}
th { color: #22c55e !important; text-align: left !important; }
td { color: #ffffff !important; padding: 10px !important; }

</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── FUNÇÕES DE APOIO ─────────────────────────────────────────────────────────

def obter_emblema(pts):
    if pts >= 500: return "👑 Guardião"
    if pts >= 250: return "🌳 Árvore"
    if pts >= 100: return "🌿 Broto"
    return "🌱 Iniciante"

def salvar_dados(dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", st.session_state.username).execute()

def carregar_ranking():
    res = supabase.table("usuarios").select("username, dados_json").execute()
    data = []
    for u in res.data:
        p = u['dados_json'].get('pontos_totais', 0)
        data.append({"Posição": "", "Emblema": obter_emblema(p), "Usuário": u['username'], "Pontos": p})
    df = pd.DataFrame(data).sort_values("Pontos", ascending=False)
    df["Posição"] = range(1, len(df) + 1)
    return df

# ─── INTERFACE DE LOGIN ───────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<p class="logo-eco">ECOTECH</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="card-home">
        <h3>Bem-vindo à Revolução Sustentável! 🌍</h3>
        <p>O <b>EcoTech</b> é uma plataforma gamificada para transformar seus hábitos diários em impacto real.</p>
        <ul>
            <li><b>Ganhe Pontos:</b> Registre caminhadas, pedaladas e descarte correto de resíduos.</li>
            <li><b>Aprenda:</b> Responda ao nosso Quiz diário sobre o meio ambiente.</li>
            <li><b>Evolua:</b> Suba de nível, de Semente a Guardião da Natureza.</li>
            <li><b>Ranking:</b> Veja sua posição entre os usuários mais eco-friendly do mundo!</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Acesse sua conta")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else: st.error("Erro no login.")

else:
    # ─── DASHBOARD LOGADO ───
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.write(f"Nível: {obter_emblema(st.session_state.user_data['pontos_totais'])}")
        st.divider()
        menu = st.radio("Navegação", ["Início / Dashboard", "Quiz Sustentável", "Mapa de Coleta", "Ranking Global", "Mini-Game"])
        st.divider()
        if st.button("Sair"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "Início / Dashboard":
        st.title("🌿 Seu Impacto Atual")
        pts = st.session_state.user_data['pontos_totais']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pontos Acumulados", f"{pts} pts")
        c2.metric("CO₂ Evitado", f"{pts*0.1:.1f} kg")
        c3.metric("Emblema Atual", obter_emblema(pts))

        st.markdown("---")
        st.subheader("🚀 Registrar Nova Ação")
        
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🚲 Transporte Sustentável"):
                minutos = st.number_input("Minutos pedalando/andando:", 1, 300, 30)
                if st.button("Registrar Transporte"):
                    ganho = minutos // 10
                    st.session_state.user_data['pontos_totais'] += ganho
                    salvar_dados(st.session_state.user_data)
                    st.success(f"+{ganho} pontos registrados!")
                    st.rerun()

        with col_b:
            with st.expander("📱 Descarte Eletrônico"):
                tipo = st.selectbox("O que você descartou?", ["Pilhas/Baterias", "Celular Antigo", "Cab
