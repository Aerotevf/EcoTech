import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (CYBER-NATURE + PIXEL ART + FUNDO ANIMADO)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=DM+Sans:wght@400;700&display=swap');

/* Forçar Fundo Transparente para a Animação aparecer */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: transparent !important;
}

[data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Estilo Terminal */
[data-testid="stSidebar"] {
    background-color: rgba(0, 15, 0, 0.95) !important;
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
    font-weight: 500;
}

/* Logo GIGANTE, Centralizado e Brilhante */
.logo-pixel-home {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 80px; /* BEM GRANDE */
    text-align: center;
    padding: 50px 0;
    margin-bottom: 30px;
    background: -webkit-linear-gradient(#39ff14, #00ffcc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(6px 6px #000);
}

/* Logo Interno (no topo das abas) */
.logo-pixel-interno {
    font-family: 'Press Start 2P', cursive !important;
    font-size: 30px;
    text-align: center;
    padding: 15px 0;
    color: #39ff14 !important;
    text-shadow: 2px 2px #000;
}

/* Botões Estilo Arcade Retro */
.stButton > button {
    background-color: #000 !important;
    color: #39ff14 !important;
    border: 3px solid #39ff14 !important;
    font-family: 'Press Start 2P', cursive !important;
    font-size: 14px !important;
    border-radius: 0px !important;
    box-shadow: 6px 6px 0px #052b05;
}

.stButton > button:hover {
    background-color: #39ff14 !important;
    color: #000 !important;
}

.card-pixel {
    background: rgba(0, 30, 0, 0.8);
    border: 2px solid #00ffcc;
    padding: 25px;
    margin-bottom: 20px;
}

/* Mensagem de Erro Vermelha vibrante */
.stError {
    background-color: #330000 !important;
    color: #ff3333 !important;
    border: 2px solid #ff3333 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ─── ANIMAÇÃO DE FUNDO (CÓDIGO MATRIX COM FOLHAS) ──────────────────────────
st.markdown("""
<canvas id="canvas"></canvas>
<script>
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');

    // Forçar o canvas a cobrir toda a tela
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1'; // Fica atrás de tudo

    // Caracteres e Símbolos
    var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$&*🌿🌱';
    letters = letters.split('');

    var fontSize = 16;
    var columns = canvas.width / fontSize;

    // Posição vertical de cada coluna
    var drops = [];
    for (var x = 0; x < columns; x++)
        drops[x] = 1;

    // Função de desenho
    function draw() {
        // Fundo preto translúcido para criar o efeito de rastro
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#39ff14'; // Cor Verde Neon
        ctx.font = fontSize + 'px arial';

        for (var i = 0; i < drops.length; i++) {
            var text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            // Reiniciar a gota se chegar ao fim da tela
            if (drops[i] * fontSize > canvas.width && Math.random() > 0.975)
                drops[i] = 0;

            drops[i]++;
        }
    }

    // Rodar a animação
    setInterval(draw, 33);
    
    // Ajustar tamanho se a janela mudar
    window.onresize = function() {
        canvas.height = window.innerHeight;
        canvas.width = window.innerWidth;
        columns = canvas.width / fontSize;
        for (var x = 0; x < columns; x++) drops[x] = 1;
    }
</script>
""", unsafe_allow_html=True)

# ─── CONEXÃO SUPABASE ──────────────────────────────────────────────────────────
# Substitua com suas credenciais reais
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── LÓGICA DO SISTEMA ────────────────────────────────────────────────────────

def obter_nivel(pontos):
    if pontos >= 500: return "👑 Guardião"
    if pontos >= 250: return "🌳 Árvore"
    if pontos >= 100: return "🌿 Broto"
    return "🌱 Semente"

def salvar_dados(dados):
    supabase.table("usuarios").update({"dados_json": dados}).eq("username", st.session_state.username).execute()

def carregar_ranking():
    res = supabase.table("usuarios").select("username, dados_json").execute()
    data = []
    for u in res.data:
        p = u['dados_json'].get('pontos_totais', 0)
        data.append({"NÍVEL": obter_nivel(p), "PLAYER": u['username'], "XP (PONTOS)": p})
    return pd.DataFrame(data).sort_values("XP (PONTOS)", ascending=False)

# ─── INTERFACE ────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# TELA DE ACESSO (Home/Login)
if not st.session_state.logged_in:
    # Logo GIGANTE na Home
    st.markdown('<p class="logo-pixel-home">ECOTECH</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("📖 MANUAL DA MISSÃO")
        st.write("**OBJETIVO:** Salvar o planeta ganhando XP através de ações reais.")
        st.write("---")
        st.write("🏃 **MISSÕES:** Registre transporte, reciclagem e responda Quizzes.")
        st.write("🏆 **RANKING:** Veja quem são os melhores defensores da natureza.")
        st.write("💡 **IMPACTO:** Aprenda sobre o carbono que você evitou.")
        st.write("<i>Transforme o mundo enquanto evolui seu perfil!</i>")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-pixel">', unsafe_allow_html=True)
        st.subheader("ACESSO")
        u = st.text_input("USER", placeholder="seu_usuario")
        p = st.text_input("PASS", type="password", placeholder="••••••••")
        if st.button("START →"):
            try:
                res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.session_state.user_data = res.data[0]['dados_json']
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos. Tente novamente.")
            except:
                st.error("⚠️ Erro de conexão com o servidor.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ─── SISTEMA LOGADO ───
    with st.sidebar:
        # PAINEL DO USUÁRIO NO TOPO DA SIDEBAR
        st.markdown(f"### 👾 Olá, {st.session_state.username}")
        pts_atuais = st.session_state.user_data['pontos_totais']
        st.write(f"Sua Patente: **{obter_nivel(pts_atuais)}**")
        st.write(f"Total XP: **{pts_atuais}**")
        st.divider()
        
        menu = st.radio("FASES DO SISTEMA:", ["📊 PAINEL DE IMPACTO", "🏆 RANKING GLOBAL", "🗺️ MAPA DE COLETA"])
        st.divider()
        if st.button("QUIT (SAIR)"):
            st.session_state.logged_in = False
            st.rerun()

    # Logo no topo de todas as abas internas
    st.markdown('<p class="logo-pixel-interno">ECOTECH</p>', unsafe_allow_html=True)

    if menu == "📊 PAINEL DE IMPACTO":
        st.subheader("Seu Status e Missões Diárias")
        
        pts = st.session_state.user_data['pontos_totais']
        kg_co2 = pts * 0.1
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("XP ATUAL", f"{pts} pts")
        with c2: st.metric("CARBONO EVITADO", f"{kg_co2:.1f} kg")
        with c3: st.metric("NÍVEL", obter_nivel(pts))
        
        st.markdown("---")
        st.subheader("🏃 MISSÕES DISPONÍVEIS (+XP)")
        
        # QUIZ JÁ NAS MISSÕES DIÁRIAS
        with st.expander("🧠 DESAFIO INTEL (QUIZ DIÁRIO)"):
            if 'pergunta' not in st.session_state:
                st.session_state.pergunta = random.choice([
                    {"p": "Qual destes materiais polui mais o oceano?", "o": ["Papel", "Vidro", "Plástico"], "r": "Plástico"},
                    {"p": "Reciclar uma tonelada de papel salva quantas árvores?", "o": ["5", "17", "50"], "r": "17"}
                ])
            
            st.markdown(f"### {st.session_state.pergunta['p']}")
            resp = st.radio("Sua resposta:", st.session_state.pergunta['o'])
            
            if st.button("RESPONDER QUIZ"):
                if resp == st.session_state.pergunta['r']:
                    st.success("ACERTO CRÍTICO! +20 XP")
                    st.session_state.user_data['pontos_totais'] += 20
                    salvar_dados(st.session_state.user_data)
                    del st.session_state.pergunta # Nova pergunta no próximo clique
                else:
                    st.error("Tente novamente amanhã!")

        # TODAS AS OPÇÕES DE TRANSPORTE SUSTENTÁVEL
        with st.expander("🚲 TRANSPORTE SUSTENTÁVEL"):
            opcoes_transporte = ["Fui de Bike/A pé", "Usei Ônibus/Metrô", "Carona Compartilhada"]
            transporte = st.radio("Como você se locomoveu?", opcoes_transporte)
            if st.button("REGISTRAR TRAJETO"):
                pts_transporte = 10 if transporte == "Carona Compartilhada" else 15
                st.session_state.user_data['pontos_totais'] += pts_transporte
                salvar_dados(st.session_state.user_data)
                st.success(f"+{pts_transporte} XP Adicionado! Bom trajeto.")

        # DESCARTE ELETRÔNICO
        with st.expander("📱 DESCARTE CORRETO"):
            tipo = st.selectbox("O que você descartou?", ["Pilhas/Baterias", "Celular Antigo", "Cabos/Periféricos"])
            if st.button("REGISTRAR DESCARTE"):
                st.session_state.user_data['pontos_totais'] += 30
                salvar_dados(st.session_state.user_data)
                st.success("+30 XP! Ótima ação para o planeta.")

    elif menu == "🏆 RANKING GLOBAL":
        st.subheader("Melhores Defensores do Planeta")
        df = carregar_ranking()
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif menu == "🗺️ MAPA DE COLETA":
        st.subheader("Onde descartar seu 'Lixo-Tech'?")
        mapa_data = pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}) # Exemplo SP
        st.map(mapa_data)
