import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS REFORÇADO COM GRADIENTE ROXO-ROSA-VERDE
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

.stButton > button:hover {
    background-color: #86EFAC !important;
    color: #0F172A !important;
    border-color: #86EFAC !important;
}

.card-tech {
    background: rgba(124, 58, 237, 0.1);
    border: 2px solid #7C3AED;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

def salvar_dados(dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", st.session_state.username).execute()

# ─── INTERFACE ────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

st.markdown('<p class="logo-ecotech">ECOTECH</p>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="card-tech"><h2>MANUAL DA MISSÃO 🌍</h2><p>Transforme tecnologia em aliada da natureza. Registre ações e ganhe XP.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card-tech">', unsafe_allow_html=True)
        u = st.text_input("USER")
        p = st.text_input("PASS", type="password")
        if st.button("START MISSION →"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else: st.error("Login Inválido")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    with st.sidebar:
        st.markdown(f"### 👾 {st.session_state.username}")
        pts = st.session_state.user_data.get('pontos_totais', 0)
        menu = st.radio("SISTEMA:", ["📊 PAINEL", "🏆 RANKING", "🗺️ ECO-RADAR"])
        if st.button("SAIR"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "📊 PAINEL":
        pts = st.session_state.user_data.get('pontos_totais', 0)
        co2_total = pts * 0.1
        
        c1, c2, c3 = st.columns(3)
        c1.metric("XP TOTAL", f"{pts} pts")
        c2.metric("CARBONO EVITADO", f"{co2_total:.1f} kg")
        c3.metric("NÍVEL", "🌱 Semente" if pts < 100 else "🌳 Árvore")
        
        st.info(f"💡 IMPACTO: Você evitou o CO2 equivalente a {int(co2_total * 5)} viagens de carro de 1km!")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        
        with col_a:
            with st.expander("🚲 TRANSPORTE SUSTENTÁVEL"):
                tempo = st.number_input("Minutos de trajeto:", 5, 300, 20)
                tipo_t = st.selectbox("Modalidade:", ["Bike/A pé", "Ônibus/Metrô"])
                fator = 2 if tipo_t == "Bike/A pé" else 1
                economia = (tempo * 0.15) * fator # Cálculo: tempo x taxa de emissão evitada
                
                if st.button("REGISTRAR TRAJETO"):
                    st.session_state.user_data['pontos_totais'] += int(tempo/2)
                    salvar_dados(st.session_state.user_data)
                    st.success(f"Missão Concluída! Você evitou {economia:.2f}kg de CO2 neste trajeto.")
                    st.rerun()

        with col_b:
            with st.expander("🧠 QUIZ SUSTENTÁVEL"):
                st.write("Qual lixo abaixo demora 450 anos para sumir?")
                alternativas = ["Papel", "Garrafa PET", "Casca de Banana"]
                resp = st.radio("Sua resposta:", alternativas)
                if st.button("CONFIRMAR"):
                    if resp == "Garrafa PET":
                        st.session_state.user_data['pontos_totais'] += 30
                        salvar_dados(st.session_state.user_data)
                        st.success("ACERTOU! +30 XP")
                    else: st.error("Incorreto!")

    elif menu == "🏆 RANKING":
        res = supabase.table("usuarios").select("username, dados_json").execute()
        data = [{"Player": u['username'], "XP": u['dados_json']['pontos_totais']} for u in res.data]
        st.table(pd.DataFrame(data).sort_values("XP", ascending=False))

    elif menu == "🗺️ ECO-RADAR":
        st.subheader("Localizador de Coleta")
        cep = st.text_input("Digite seu CEP ou Endereço para busca:")
        if cep:
            # Simulação de busca lógica: em um app real aqui usaria uma API de Geocoding
            st.success(f"Ponto mais próximo de '{cep}': Rua das Palmeiras, 123 - Centro (Coleta de Eletrônicos)")
            st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}))
