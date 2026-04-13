import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS REFORÇADO COM PALETA FINAL (ROXO-ROSA-VERDE)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #581C87 0%, #0F172A 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: rgba(26, 10, 41, 0.95) !important;
    border-right: 2px solid #7C3AED;
}

h1, h2, h3, h4, p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #FFFFFF !important;
}

.logo-ecotech {
    font-family: 'Press Start 2P', cursive !important;
    font-size: clamp(30px, 8vw, 70px) !important;
    text-align: center;
    padding: 30px 0;
    background: -webkit-linear-gradient(45deg, #7C3AED, #EC4899, #22C55E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 15px rgba(236, 72, 153, 0.6));
}

.stButton > button {
    background-color: #EC4899 !important;
    color: #FFFFFF !important;
    border: 2px solid #EC4899 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 12px !important;
    width: 100%;
}

.card-tech {
    background: rgba(124, 58, 237, 0.1);
    border: 2px solid #7C3AED;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.emblema-card {
    text-align: center;
    padding: 15px;
    border: 1px solid #22C55E;
    border-radius: 10px;
    background: rgba(34, 197, 94, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

def salvar_dados(dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", st.session_state.username).execute()

# ─── LÓGICA DE PATENTES & CURIOSIDADES ────────────────────────────────────────
patentes = {
    "Semente": {"icon": "🌱", "desc": "Cada semente plantada ajuda a recuperar o solo e aumenta a biodiversidade local.", "min": 0},
    "Broto": {"icon": "🌿", "desc": "Brotos absorvem CO2 em fase acelerada, purificando o ar que respiramos no início da vida.", "min": 150},
    "Árvore": {"icon": "🌳", "desc": "Uma árvore adulta pode absorver até 22kg de CO2 por ano, protegendo o clima.", "min": 400},
    "EcoLíder": {"icon": "👑", "desc": "Líderes inspiram comunidades a reduzir toneladas de lixo eletrônico anualmente.", "min": 800}
}

def obter_patente_info(pts):
    if pts >= 800: return "EcoLíder"
    if pts >= 400: return "Árvore"
    if pts >= 150: return "Broto"
    return "Semente"

# ─── INTERFACE ────────────────────────────────────────────────────────────────
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

st.markdown('<p class="logo-ecotech">ECOTECH</p>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("""
        <div class="card-tech">
            <h2 style="color:#22C55E">BEM-VINDO AO ECOTECH 🌍</h2>
            <p>O <b>EcoTech</b> é uma plataforma de monitoramento de impacto ambiental gamificada.</p>
            <p>Nossa missão é recompensar usuários que adotam hábitos sustentáveis. Ao registrar suas atividades de mobilidade e reciclagem, você ganha XP e evolui sua patente no ranking global.</p>
            <p><i>Tecnologia e Natureza em um só lugar.</i></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-tech">', unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("ACESSAR TERMINAL →"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                # Garante que a chave de tentativas exista
                if 'tentativas_quiz' not in st.session_state.user_data:
                    st.session_state.user_data['tentativas_quiz'] = 0
                st.rerun()
            else: st.error("DADOS INCORRETOS!")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown(f"### 👾 {st.session_state.username}")
        pts = st.session_state.user_data.get('pontos_totais', 0)
        pat = obter_patente_info(pts)
        st.write(f"Nível: {patentes[pat]['icon']} {pat}")
        menu = st.radio("SELECIONE A FASE:", ["📊 PAINEL", "🏆 RANKING", "🗺️ ECO-RADAR"])
        if st.button("SAIR DO SISTEMA"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "📊 PAINEL":
        pts = st.session_state.user_data.get('pontos_totais', 0)
        c1, c2, c3 = st.columns(3)
        c1.metric("XP ACUMULADO", f"{pts} pts")
        c2.metric("CARBONO POUPADO", f"{pts*0.1:.1f} kg")
        c3.metric("MISSÕES HOJE", f"{st.session_state.user_data.get('tentativas_quiz', 0)}/5")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        
        with col_a:
            with st.expander("🚲 REGISTRAR TRANSPORTE"):
                tempo = st.number_input("Tempo do trajeto (minutos):", 5, 120, 20)
                tipo = st.selectbox("Modalidade:", ["Caminhada/Bike", "Transporte Público"])
                if st.button("FINALIZAR MISSÃO 🚲"):
                    co2_eco = tempo * 0.15 if tipo == "Caminhada/Bike" else tempo * 0.05
                    st.session_state.user_data['pontos_totais'] += int(tempo/2)
                    salvar_dados(st.session_state.user_data)
                    st.success(f"Excelente! Você economizou {co2_eco:.2f}kg de CO2!")
                    st.rerun()

        with col_b:
            with st.expander("🧠 QUIZ SUSTENTÁVEL"):
                if st.session_state.user_data.get('tentativas_quiz', 0) >= 5:
                    st.warning("Você chegou ao limite de tentativas hoje, tente novamente amanhã")
                else:
                    perguntas = [
                        {"q": "Qual metal é mais comum em baterias de celular?", "a": ["Ouro", "Lítio", "Cobre"], "r": "Lítio"},
                        {"q": "Qual cor representa a reciclagem de Metal?", "a": ["Azul", "Amarelo", "Verde"], "r": "Amarelo"},
                        {"q": "Qual recurso é economizado ao reciclar alumínio?", "a": ["Energia", "Água", "Madeira"], "r": "Energia"}
                    ]
                    # Seleciona pergunta sem repetir com base nas tentativas do dia
                    idx = st.session_state.user_data['tentativas_quiz'] % len(perguntas)
                    item = perguntas[idx]
                    st.write(f"**Pergunta:** {item['q']}")
                    resp = st.radio("Sua Resposta:", item['a'], key=f"q_{idx}")
                    if st.button("ENVIAR RESPOSTA"):
                        st.session_state.user_data['tentativas_quiz'] += 1
                        if resp == item['r']:
                            st.session_state.user_data['pontos_totais'] += 20
                            st.success("ACERTOU! +20 XP")
                        else: st.error(f"ERROU! A resposta certa era {item['r']}")
                        salvar_dados(st.session_state.user_data)
                        st.rerun()

    elif menu == "🏆 RANKING":
        st.subheader("Leaderboard Global")
        res = supabase.table("usuarios").select("username, dados_json").execute()
        df_ranking = pd.DataFrame([{"Player": u['username'], "XP": u['dados_json']['pontos_totais']} for u in res.data])
        st.table(df_ranking.sort_values("XP", ascending=False))
        
        st.markdown("---")
        st.subheader("🌱 ENTENDA AS ETAPAS DA EVOLUÇÃO")
        cols = st.columns(4)
        for i, (nome, info) in enumerate(patentes.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="emblema-card">
                    <h1 style="margin:0;">{info['icon']}</h1>
                    <b style="color:#22C55E; font-size:16px;">{nome}</b>
                    <p style="font-size:12px; color:#ddd; margin-top:10px;">{info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

    elif menu == "🗺️ ECO-RADAR":
        cep = st.text_input("Digite um Endereço ou CEP para busca:")
        if cep:
            st.success(f"Localizando postos próximos de: {cep}")
            st.write("📍 **Ponto Identificado:** Rua das Palmeiras, 100 - Centro (Aceita Baterias e Plásticos)")
            st.map(pd.DataFrame({'lat': [-23.5505], 'lon': [-46.6333]}))
