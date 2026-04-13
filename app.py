import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (CYBER-NATURE + PIXEL ART + CONTRASTE)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Fundo Verde-Escuro Tecnológico (Melhor Contraste) */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #051a05 0%, #020814 100%) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal */
[data-testid="stSidebar"] {
    background-color: rgba(0, 20, 0, 0.9) !important;
    border-right: 2px solid #39ff14;
}

/* Títulos em PIXEL ART com Neon */
h1, h2, h3, .pixel-font {
    font-family: 'Press Start 2P', cursive !important;
    color: #39ff14 !important;
    text-shadow: 2px 2px #000, 0 0 10px #39ff14;
}

/* Texto Branco Puro para Leitura Máxima */
p, li, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #ffffff !important;
    font-size: 16px !important;
}

/* Logo Grande e Brilhante */
.logo-pixel {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 45px;
    text-align: center;
    padding: 20px;
    background: -webkit-linear-gradient(#39ff14, #00ffcc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(4px 4px #000);
}

/* Botões Estilo Arcade Retro */
.stButton > button {
    background-color: #000 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 12px !important;
    border-radius: 0px !important;
    box-shadow: 6px 6px 0px #052b05;
}

.stButton > button:hover {
    background-color: #39ff14 !important;
    color: #000 !important;
}

.card-pixel {
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid #00ffcc;
    padding: 25px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DO SISTEMA ────────────────────────────────────────────────────────

def carregar_ranking():
    res = supabase.table("usuarios").select("username, dados_json").execute()
    data = []
    for u in res.data:
        p = u['dados_json'].get('pontos_totais', 0)
        data.append({"PLAYER": u['username'], "XP (PONTOS)": p})
    return pd.DataFrame(data).sort_values("XP (PONTOS)", ascending=False)

def curisidade_impacto(kg):
    if kg <= 0: return "Sua jornada começa agora! Faça sua primeira ação."
    elif kg < 5: return f"Isso equivale a carregar seu celular {int(kg*120)} vezes!"
    else: return f"Impacto incrível! Você poupou o planeta de {int(kg/0.02)} canudos de plástico!"

# ─── INTERFACE ────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<p class="logo-pixel">ECOTECH</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("📖 MANUAL DA MISSÃO")
        st.write("**OBJETIVO:** Salvar o planeta ganhando XP através de ações reais.")
        st.write("---")
        st.write("🟢 **PAINEL:** Veja seus atributos e o carbono que você evitou.")
        st.write("🔵 **QUIZ:** Acerte perguntas para ganhar bônus de inteligência.")
        st.write("🟡 **MAPA:** Encontre locais para descartar seu 'lixo-tech'.")
        st.write("🔴 **ECO-JUMP:** Treine seus reflexos e ganhe pontos extras.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("LOGIN")
        u = st.text_input("USER")
        p = st.text_input("PASS", type="password")
        if st.button("START"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown(f"## 🔋 XP: {st.session_state.user_data['pontos_totais']}")
        menu = st.radio("SELECIONE A FASE:", ["📊 STATUS (PAINEL)", "🧠 DESAFIO (QUIZ)", "🗺️ RADAR (MAPA)", "🏆 RANKING", "🕹️ MINI-GAME"])
        st.divider()
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "📊 STATUS (PAINEL)":
        st.markdown('<h1 class="pixel-font">STATUS DO PLAYER</h1>', unsafe_allow_html=True)
        st.write("Aqui você acompanha sua evolução e o impacto real no planeta.")
        
        pts = st.session_state.user_data['pontos_totais']
        kg_co2 = pts * 0.1
        
        c1, c2 = st.columns(2)
        c1.metric("PONTOS TOTAIS", f"{pts} XP")
        c2.metric("CO2 POUPADO", f"{kg_co2:.1f} KG")
        
        st.warning(f"💡 **IMPACTO REAL:** {curisidade_impacto(kg_co2)}")

        st.markdown("---")
        st.subheader("🏃 MISSÕES DIÁRIAS")
        with st.expander("COMO GANHAR PONTOS? (CLIQUE AQUI)"):
            st.write("Escolha uma ação abaixo para registrar seu progresso sustentável:")
            
            if st.button("🚲 USEI TRANSPORTE VERDE (+10 XP)"):
                st.session_state.user_data['pontos_totais'] += 10
                supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                st.success("Missão Cumprida! XP Adicionado.")
                st.rerun()

    elif menu == "🧠 DESAFIO (QUIZ)":
        st.markdown('<h1 class="pixel-font">BOSS QUIZ</h1>', unsafe_allow_html=True)
        st.write("Responda sem errar para ganhar bônus de XP. Se errar, o Boss vence!")
        
        if 'pergunta' not in st.session_state:
            st.session_state.pergunta = random.choice([
                {"p": "Qual destes lixos é o mais perigoso se jogado no mar?", "o": ["Papel", "Pilhas", "Resto de comida"], "r": "Pilhas"},
                {"p": "Reciclar uma tonelada de papel salva quantas árvores?", "o": ["5", "17", "50"], "r": "17"}
            ])
        
        st.markdown(f"### {st.session_state.pergunta['p']}")
        resp = st.radio("Sua resposta:", st.session_state.pergunta['o'])
        
        if st.button("CONFIRMAR RESPOSTA"):
            if resp == st.session_state.pergunta['r']:
                st.success("ACERTO CRÍTICO! +20 XP")
                st.session_state.user_data['pontos_totais'] += 20
                supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                del st.session_state.pergunta # Nova pergunta no próximo clique
            else:
                st.error("GAME OVER! Essa você errou.")

    elif menu == "🗺️ RADAR (MAPA)":
        st.markdown('<h1 class="pixel-font">ECO-RADAR</h1>', unsafe_allow_html=True)
        st.write("Filtre por categoria para encontrar o ponto de descarte correto:")
        cat = st.selectbox("O QUE VOCÊ TEM PARA DESCARTAR?", ["Eletrônicos", "Pilhas e Baterias", "Óleo de Cozinha", "Plásticos"])
        st.write(f"Exibindo pontos de coleta para: **{cat}**")
        st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]})) # Exemplo SP

    elif menu == "🏆 RANKING":
        st.markdown('<h1 class="pixel-font">HALL OF FAME</h1>', unsafe_allow_html=True)
        df = carregar_ranking()
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif menu == "🕹️ MINI-GAME":
        st.markdown('<h1 class="pixel-font">ECO-JUMP</h1>', unsafe_allow_html=True)
        st.write("A cada 10 pulos, você limpa uma área e ganha +5 XP!")
        
        if 'pulos' not in st.session_state: st.session_state.pulos = 0
        
        st.markdown(f"## PROGRESSO: {st.session_state.pulos}/10")
        st.progress(st.session_state.pulos / 10)
        
        if st.button("PULAR ⬆️"):
            st.session_state.pulos += 1
            if st.session_state.pulos >= 10:
                st.session_state.user_data['pontos_totais'] += 5
                supabase.table("usuarios").update({"dados_json": st.session_state.user_data}).eq("username", st.session_state.username).execute()
                st.session_state.pulos = 0
                st.balloons()
                st.success("ÁREA LIMPA! +5 XP")
