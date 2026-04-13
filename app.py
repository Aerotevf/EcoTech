import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS REFORÇADO E UNIFICADO (PALETA DE CORES EXATA)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Fundo: Roxo Profundo para Azul Escuro */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #581C87 0%, #0F172A 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal Roxo */
[data-testid="stSidebar"] {
    background-color: rgba(26, 10, 41, 0.95) !important;
    border-right: 2px solid #7C3AED;
}

/* Forçar Texto Branco em tudo */
h1, h2, h3, h4, p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #FFFFFF !important;
}

/* ── TÍTULO GIGANTE ECOTECH (EM TODAS AS ABAS) ── */
.logo-ecotech-universal {
    font-family: 'Press Start 2P', cursive !important;
    font-size: clamp(30px, 8vw, 70px) !important;
    text-align: center;
    padding: 30px 0;
    margin-bottom: 20px;
    
    /* Gradiente Exato: Roxo -> Rosa -> Verde */
    background: -webkit-linear-gradient(45deg, #7C3AED, #EC4899, #22C55E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Brilho Neon */
    filter: drop-shadow(0 0 15px rgba(236, 72, 153, 0.6));
    image-rendering: pixelated;
}

/* Botões: Rosa Vibrante com Hover Verde Neon Suave */
.stButton > button {
    background-color: #EC4899 !important;
    color: #FFFFFF !important;
    border: 2px solid #EC4899 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 12px !important;
    border-radius: 5px !important;
    transition: 0.3s all !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #86EFAC !important; /* Verde Neon Suave */
    color: #0F172A !important;
    border-color: #86EFAC !important;
    box-shadow: 0 0 15px #86EFAC;
}

/* Cards de Informação Roxo Médio */
.card-tech {
    background: rgba(124, 58, 237, 0.1);
    border: 2px solid #7C3AED;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Destaque de XP (Verde Sustentável) */
.stSuccess {
    background-color: rgba(34, 197, 94, 0.1) !important;
    color: #22C55E !important;
    border: 1px solid #22C55E !important;
}

/* Mensagem de Erro Vermelha */
.stError {
    background-color: rgba(236, 72, 153, 0.1) !important;
    color: #EC4899 !important;
    border: 1px solid #EC4899 !important;
}

/* Alinhamento de Tabelas */
[data-testid="stTable"] table {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
# Credenciais Exatas do seu Banco
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DO SISTEMA ────────────────────────────────────────────────────────
def obter_patente(p):
    if p >= 500: return "👑 Guardião Master"
    if p >= 250: return "🌳 Eco Líder"
    if p >= 100: return "🌿 Broto Ativo"
    return "🌱 Semente Digital"

def salvar_dados_usuario(username, dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", username).execute()

# ─── INTERFACE ────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'login_err' not in st.session_state: st.session_state.login_err = False

# TÍTULO UNIVERSAL NO TOPO DE TUDO
st.markdown('<p class="logo-ecotech-universal">ECOTECH</p>', unsafe_allow_html=True)

# TELA DE ACESSO
if not st.session_state.logged_in:
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        <div class="card-tech">
            <h2 style="color:#22C55E !important; font-family:'Press Start 2P'; font-size:16px; margin-bottom:15px;">MANUAL DA MISSÃO 🌍</h2>
            <p>O <b>EcoTech</b> é o seu terminal de monitoramento ambiental de alta tecnologia.</p>
            <p>Nossa missão é usar a inovação digital para quantificar e recompensar suas boas ações no mundo real.</p>
            <p><b>Como funciona:</b></p>
            <ul>
                <li>🚲 <b>Mobilidade:</b> Registre trajetos limpos e ganhe XP.</li>
                <li>🧠 <b>Quiz:</b> Teste seus conhecimentos e evolua sua patente.</li>
                <li>🏆 <b>Impacto:</b> Acompanhe quanto CO2 você evitou.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-tech">', unsafe_allow_html=True)
        st.subheader("ACESSO AO TERMINAL")
        u = st.text_input("USUÁRIO", key="user_in", placeholder="ex: player1")
        p = st.text_input("SENHA", type="password", key="pass_in", placeholder="••••••••")
        
        if st.button("START MISSION →"):
            try:
                res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    # Carregar dados ou usar padrão se estiver vazio
                    dados_bd = res.data[0]['dados_json']
                    st.session_state.user_data = dados_bd if dados_bd else {"pontos_totais": 0}
                    st.session_state.login_err = False
                    st.rerun()
                else:
                    st.session_state.login_err = True
            except:
                st.error("Erro de conexão com o terminal.")
        
        if st.session_state.login_err:
            st.markdown('<p style="color:#EC4899; text-align:center; font-family:\'Press Start 2P\'; font-size:10px;">DADOS INCORRETOS!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ─── INTERFACE INTERNA (DASHBOARD) ───
    with st.sidebar:
        st.markdown(f"### 👾 PLAYER: {st.session_state.username}")
        pts = st.session_state.user_data.get('pontos_totais', 0)
        st.write(f"Patente: **{obter_patente(pts)}**")
        st.divider()
        menu = st.radio("SELECIONE A FASE:", ["📊 PAINEL DE IMPACTO", "🏆 RANKING GLOBAL", "🗺️ ECO-RADAR"])
        st.divider()
        if st.button("QUIT (SAIR)"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "📊 PAINEL DE IMPACTO":
        st.subheader("Missões e Estatísticas de Impacto")
        
        # EXPLICAÇÃO DA ABA (Com cor Verde Sustentável)
        st.markdown(f"""
        <div style="background:rgba(34, 197, 94, 0.1); padding:15px; border-radius:10px; border-left: 5px solid #22C55E; margin-bottom:20px;">
            <p style="margin:0; font-size:14px; color:#FFFFFF;"><b>INFO:</b> Este é seu centro de comando. Aqui você vê seu XP acumulado e registra as missões diárias de Transporte e Quiz para converter seu esforço em redução real de CO2.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pts = st.session_state.user_data.get('pontos_totais', 0)
        kg_co2 = pts * 0.1
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("XP TOTAO", f"{pts} pts")
        with c2: st.metric("CARBONO EVITADO", f"{kg_co2:.1f} kg")
        with c3: st.metric("NÍVEL ATUAL", obter_patente(pts))

        st.markdown("---")
        st.subheader("🏃 MISSÕES DISPONÍVEIS (+XP)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🚲 TRANSPORTE SUSTENTÁVEL"):
                st.write("Cada trajeto limpo diminui sua pegada de carbono.")
                if st.button("Bike/A pé (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
                    st.success("Missão Cumprida! XP salvo.")
                    st.rerun()
                if st.button("Bus/Metrô (+10 XP)"):
                    st.session_state.user_data['pontos_totais'] += 10
                    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
                    st.rerun()

        with col_b:
            with st.expander("🧠 DESAFIO QUIZ"):
                st.write("Reciclar 1 tonelada de papel salva 17 árvores?")
                if st.button("VERDADEIRO (+20 XP)"):
                    st.session_state.user_data['pontos_totais'] += 20
                    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
                    st.success("Resposta Exata! XP Adicionado.")
                    st.rerun()

    elif menu == "🏆 RANKING GLOBAL":
        st.subheader("Hall da Fama - Melhores Defensores do Planeta")
        
        st.markdown(f"""
        <div style="background:rgba(34, 197, 94, 0.1); padding:15px; border-radius:10px; border-left: 5px solid #22C55E; margin-bottom:20px;">
            <p style="margin:0; font-size:14px; color:#FFFFFF;"><b>INFO:</b> O Ranking Global mostra os usuários mais ativos na plataforma. Compita de forma saudável para inspirar a comunidade EcoTech!</p>
        </div>
        """, unsafe_allow_html=True)
        
        res = supabase.table("usuarios").select("username, dados_json").execute()
        data = []
        for u in res.data:
            p = u['dados_json'].get('pontos_totais', 0)
            data.append({"Patente": obter_patente(p), "Player": u['username'], "XP": p})
        
        df = pd.DataFrame(data).sort_values("XP", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif menu == "🗺️ ECO-RADAR":
        st.subheader("Localizador de Coleta 'Lixo-Tech'")
        
        st.markdown(f"""
        <div style="background:rgba(34, 197, 94, 0.1); padding:15px; border-radius:10px; border-left: 5px solid #22C55E; margin-bottom:20px;">
            <p style="margin:0; font-size:14px; color:#FFFFFF;"><b>INFO:</b> Use o Eco-Radar para encontrar os pontos de descarte correto mais próximos. Evite contaminação e garanta o descarte correto.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]})) # Exemplo SP
