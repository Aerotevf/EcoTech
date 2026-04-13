import streamlit as st
import pandas as pd
import random
from datetime import date, datetime
from supabase import create_client, Client

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    --roxo:   #7C3AED;
    --rosa:   #EC4899;
    --verde:  #22C55E;
    --bg:     #0A0A14;
    --card:   rgba(255,255,255,0.04);
    --border: rgba(124,58,237,0.4);
    --text:   #E2E8F0;
    --muted:  #94A3B8;
}

* { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] {
    background: rgba(10,10,20,0.97) !important;
    border-right: 1px solid var(--border) !important;
}
h1,h2,h3,h4,h5,h6,p,li,label,
.stMetric,[data-testid="stMarkdown"] p,
[data-testid="stMetricValue"],[data-testid="stMetricLabel"] {
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stExpander"] details summary p {
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
input,[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--roxo), var(--rosa)) !important;
    color: #fff !important;
    border: none !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 9px !important;
    letter-spacing: 0.05em !important;
    padding: 12px 20px !important;
    border-radius: 8px !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.1s !important;
    cursor: pointer !important;
}
.stButton > button:hover  { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }
[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 14px 16px !important;
}

[data-testid="stExpander"] summary span[data-testid="stExpanderToggleIcon"] {
    flex-shrink: 0 !important;
    order: 2 !important;
    margin-left: auto !important;
}

[data-testid="stExpander"] summary p {
    order: 1 !important;
    margin: 0 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

[data-testid="stExpander"] summary svg {
    position: static !important;
    display: inline-block !important;
}

[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
.stRadio > div { gap: 6px !important; }

.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] * {
    color: var(--text) !important;
}

[data-baseweb="select"] input {
    color: #E2E8F0 !important;
    -webkit-text-fill-color: #E2E8F0 !important;
}

div[role="listbox"] {
    background: #191927 !important;
    border: 1px solid var(--border) !important;
}

div[role="option"] {
    background: #191927 !important;
    color: #E2E8F0 !important;
}

div[role="option"]:hover {
    background: rgba(124,58,237,0.25) !important;
    color: #FFFFFF !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--roxo); border-radius: 4px; }

.logo-wrap { text-align:center; padding:40px 0 20px; }
.logo-pixel {
    font-family: 'Press Start 2P', monospace !important;
    font-size: clamp(22px, 6vw, 52px) !important;
    background: linear-gradient(90deg, #7C3AED 0%, #EC4899 50%, #22C55E 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: inline-block;
    filter: drop-shadow(0 0 20px rgba(236,72,153,0.4));
    letter-spacing: 6px;
}
.logo-sub {
    font-size: 11px !important; color: var(--muted) !important;
    letter-spacing: 4px; text-transform: uppercase; margin-top: 6px;
}

.eco-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.eco-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--roxo), var(--rosa), var(--verde));
}

.badge-patente {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(124,58,237,0.2);
    border: 1px solid rgba(124,58,237,0.5);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #C4B5FD !important;
}

.xp-bar-track {
    background: rgba(255,255,255,0.08);
    border-radius: 99px; height: 8px; overflow: hidden;
}
.xp-bar-fill {
    height: 8px; border-radius: 99px;
    background: linear-gradient(90deg, var(--roxo), var(--verde));
    transition: width 0.6s ease;
}
.xp-bar-label { font-size: 11px !important; color: var(--muted) !important; margin-top: 4px; }

.rank-row {
    display: flex; align-items: center; gap: 12px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 16px; margin-bottom: 8px;
    transition: border-color 0.2s;
}
.rank-row:hover { border-color: var(--roxo); }
.rank-pos  { font-family: 'Press Start 2P', monospace; font-size: 11px; width: 32px; color: var(--muted) !important; }
.rank-name { flex: 1; font-weight: 600; font-size: 15px; }
.rank-xp   { font-weight: 700; color: var(--verde) !important; font-size: 14px; }

.emblema-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 14px; text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.emblema-card.ativo { border-color: var(--verde); background: rgba(34,197,94,0.06); }
.emblema-card.ativo:hover { transform: translateY(-4px); border-color: #4ADE80; }
.emblema-card .icone    { font-size: 36px; display: block; margin-bottom: 8px; }
.emblema-card .nome     { font-weight: 700; font-size: 13px; color: var(--verde) !important; }
.emblema-card .xp-req   { font-size: 11px !important; color: var(--muted) !important; margin-top: 4px; }
.emblema-card .desc-pat { font-size: 11px !important; color: #CBD5E1 !important; margin-top: 8px; line-height: 1.5; }

.eco-ponto {
    display: flex; align-items: flex-start; gap: 14px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px; margin-bottom: 10px;
}
.eco-ponto-icon  { font-size: 28px; flex-shrink: 0; margin-top: 2px; }
.eco-ponto-nome  { font-weight: 600; font-size: 14px; }
.eco-ponto-info  { font-size: 12px !important; color: var(--muted) !important; margin-top: 3px; }
.eco-ponto-tag {
    display: inline-block;
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 20px;
    padding: 2px 10px; font-size: 10px;
    color: #86EFAC !important;
    margin: 2px 2px 0 0;
}

.dica-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(236,72,153,0.08));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 14px;
    padding: 18px 22px; margin-bottom: 16px;
}
.dica-label {
    font-size: 9px !important;
    font-family: 'Press Start 2P', monospace !important;
    color: var(--rosa) !important;
    letter-spacing: 2px; margin-bottom: 8px; display: block;
}
.dica-texto { font-size: 13px !important; color: #E2E8F0 !important; line-height: 1.6; }

.streak-wrap {
    display: flex; align-items: center; gap: 8px;
    padding: 10px 14px;
    background: rgba(234,179,8,0.1);
    border: 1px solid rgba(234,179,8,0.3);
    border-radius: 10px; margin-bottom: 14px;
}
.streak-num   { font-family: 'Press Start 2P', monospace; font-size: 14px; color: #FDE047 !important; }
.streak-label { font-size: 12px !important; color: #FDE047 !important; }

.conquista {
    display: inline-flex; flex-direction: column;
    align-items: center; gap: 4px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px; text-align: center;
    width: 100%; margin-bottom: 12px;
}
.conquista.desbloqueada { border-color: #EAB308; background: rgba(234,179,8,0.08); }
.conquista .c-icon { font-size: 28px; }
.conquista .c-nome { font-size: 10px !important; color: var(--muted) !important; line-height: 1.3; }
.conquista.desbloqueada .c-nome { color: #FDE047 !important; }

.info-box {
    background: rgba(34,197,94,0.08);
    border-left: 3px solid var(--verde);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px; margin: 10px 0;
    font-size: 13px !important; color: #BBF7D0 !important; line-height: 1.6;
}

.sep { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 24px 0; }

@keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
.eco-card, .rank-row, .emblema-card { animation: fadeIn 0.3s ease; }
</style>
""", unsafe_allow_html=True)

# ─── SUPABASE ─────────────────────────────────────────────────────────────────
URL_DB = st.secrets.get("SUPABASE_URL", "https://cusjupdmiqxgtwbubynu.supabase.co")
KEY_DB = st.secrets.get("SUPABASE_KEY", "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7")
supabase: Client = create_client(URL_DB, KEY_DB)

def dados_iniciais():
    return {
        "pontos_totais": 0,
        "tentativas_quiz": 0,
        "data_quiz": "",
        "idx_perguntas_hoje": [],
        "total_quizzes_certos": 0,
        "total_trajetos": 0,
        "streak_dias": 0,
        "ultima_atividade": ""
    }

def normalizar_dados(dados):
    base = dados_iniciais()
    if not isinstance(dados, dict):
        return base
    base.update(dados)
    return base

def salvar_dados(dados):
    dados = normalizar_dados(dados)
    st.session_state.user_data = dados
    try:
        supabase.table("usuarios").update({"dados_json": dados}).eq(
            "username", st.session_state.username
        ).execute()
        return True
    except Exception as e:
        st.toast(f"Erro ao salvar: {e}", icon="⚠️")
        return False

def registrar_acesso(acao, detalhes=None):
    if "username" not in st.session_state:
        return
    try:
        supabase.table("acessos").insert({
            "usuario": st.session_state.username,
            "acao": acao,
            "data_hora": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        # st.toast(f"Erro log: {e}")
        pass

# ─── PATENTES ─────────────────────────────────────────────────────────────────
PATENTES = [
    {"nome": "Semente",  "icon": "🌱", "min": 0,
     "desc": "Cada semente plantada recupera o solo e aumenta a umidade do ar local."},
    {"nome": "Broto",    "icon": "🌿", "min": 150,
     "desc": "Brotos absorvem CO₂ em fase acelerada, purificando o ar que respiramos."},
    {"nome": "Árvore",   "icon": "🌳", "min": 400,
     "desc": "Uma árvore adulta absorve até 22 kg de CO₂ por ano, estabilizando o clima."},
    {"nome": "EcoLíder", "icon": "👑", "min": 800,
     "desc": "Líderes sustentáveis inspiram comunidades e geram impacto em larga escala."},
]

def obter_patente(pts):
    for p in reversed(PATENTES):
        if pts >= p["min"]:
            return p
    return PATENTES[0]

def barra_xp(pts):
    pat = obter_patente(pts)
    idx = PATENTES.index(pat)
    if idx == len(PATENTES) - 1:
        return 100, 0, None
    prox = PATENTES[idx + 1]
    pct = int((pts - pat["min"]) / (prox["min"] - pat["min"]) * 100)
    return min(100, pct), prox["min"] - pts, prox

# ─── QUIZ ─────────────────────────────────────────────────────────────────────
PERGUNTAS = [
    {"q": "Quanto tempo o vidro leva para se decompor?",
     "a": ["100 anos", "4.000 anos", "Tempo indeterminado"], "r": "Tempo indeterminado",
     "exp": "O vidro é feito de sílica, praticamente inerte. Na natureza ele pode fragmentar em partículas minúsculas mas não se decompõe quimicamente — pode levar até 1 milhão de anos."},
    {"q": "O que é chorume?",
     "a": ["Adubo orgânico", "Líquido tóxico do lixo em decomposição", "Gás metano de aterros"],
     "r": "Líquido tóxico do lixo em decomposição",
     "exp": "O chorume é formado pela umidade e decomposição de resíduos em aterros. É altamente tóxico e pode contaminar solo e lençóis freáticos se não tratado."},
    {"q": "Qual país recicla mais resíduos sólidos no mundo?",
     "a": ["Brasil", "Japão", "Alemanha"], "r": "Alemanha",
     "exp": "A Alemanha recicla ~67% dos seus resíduos graças ao sistema Pfand (depósito por embalagem) e coleta seletiva rigorosa."},
    {"q": "Qual transporte urbano emite MENOS CO₂ por passageiro?",
     "a": ["Carro elétrico (solo)", "Metrô lotado", "Ônibus BRT"],
     "r": "Metrô lotado",
     "exp": "O metrô movido a eletricidade, quando bem utilizado, pode emitir até 10× menos CO₂ por passageiro que um carro particular."},
    {"q": "Quanto tempo uma sacola plástica leva para se decompor?",
     "a": ["10 anos", "100 anos", "400 anos"], "r": "400 anos",
     "exp": "Sacolas plásticas levam entre 100 e 400 anos para se decompor, liberando microplásticos que entram na cadeia alimentar."},
    {"q": "O que é pegada hídrica?",
     "a": ["Rastro de poluição em rios", "Água usada na cadeia produtiva", "Evaporação em regiões quentes"],
     "r": "Água usada na cadeia produtiva",
     "exp": "Produzir 1 kg de carne bovina consome ~15.000 L de água; 1 kg de tomate consome ~180 L. Escolher o que consumir impacta diretamente os recursos hídricos."},
    {"q": "O que destruiu a camada de ozônio?",
     "a": ["CO₂ de veículos", "CFCs de aerossóis e geladeiras", "Metano da pecuária"],
     "r": "CFCs de aerossóis e geladeiras",
     "exp": "Os clorofluorcarbonetos (CFCs) liberam cloro na estratosfera, destruindo o ozônio. O Protocolo de Montreal baniu essas substâncias e a camada está se recuperando."},
    {"q": "Qual metal é mais comum em baterias de celular?",
     "a": ["Ouro", "Cobre", "Lítio"], "r": "Lítio",
     "exp": "O lítio é leve e tem alta capacidade energética. Por isso é muito extraído, causando impactos em regiões como o Triângulo do Lítio na América do Sul."},
    {"q": "Qual cor do lixo separa Metal na coleta seletiva?",
     "a": ["Azul", "Amarelo", "Vermelho"], "r": "Amarelo",
     "exp": "Pela norma ABNT: Amarelo = Metal, Azul = Papel, Verde = Vidro, Vermelho = Plástico, Marrom = Orgânico."},
    {"q": "Reciclar alumínio economiza principalmente qual recurso?",
     "a": ["Água", "Energia elétrica", "Madeira"], "r": "Energia elétrica",
     "exp": "Reciclar alumínio gasta até 95% menos energia do que produzir alumínio do minério bauxita."},
]

def perguntas_do_dia():
    rng = random.Random(date.today().toordinal())
    return rng.sample(range(len(PERGUNTAS)), k=5)

# ─── DICAS DIÁRIAS ────────────────────────────────────────────────────────────
DICAS = [
    "🚿 Banhos de 5 min economizam até 90 litros comparados a banhos de 15 min.",
    "🛍️ Uma sacola retornável substitui ~600 sacolas plásticas ao longo da vida.",
    "🥦 Reduzir carne bovina 1× por semana equivale a não usar o carro por 5 semanas.",
    "💡 Lâmpadas LED consomem até 80% menos energia que as incandescentes.",
    "🔌 Desligar da tomada pode reduzir a conta de luz em até 12%.",
    "🌳 Árvores próximas a uma casa podem reduzir o uso de ar-condicionado em até 30%.",
    "📱 Um celular descartado errado pode contaminar até 60 mil litros de água.",
    "🧺 Lavar roupas com água fria economiza até 90% da energia da máquina de lavar.",
    "🚰 Uma torneira pingando desperdiça até 46 litros de água por dia.",
    "🛒 Comprar a granel gera até 70% menos embalagens plásticas.",
]

def dica_do_dia():
    return random.Random(date.today().toordinal()).choice(DICAS)

# ─── CONQUISTAS ───────────────────────────────────────────────────────────────
CONQUISTAS_DEF = [
    {"icon": "🌱", "nome": "Primeira missão",  "cond": lambda d: d.get("pontos_totais", 0) >= 1,         "desc": "Registre qualquer atividade pela primeira vez."},
    {"icon": "🧠", "nome": "Quiz mestre",      "cond": lambda d: d.get("total_quizzes_certos", 0) >= 10, "desc": "Acerte 10 perguntas do quiz no total."},
    {"icon": "🚲", "nome": "Ciclista urbano",  "cond": lambda d: d.get("total_trajetos", 0) >= 5,        "desc": "Registre 5 trajetos de bike ou caminhada."},
    {"icon": "🔥", "nome": "Sequência 3 dias", "cond": lambda d: d.get("streak_dias", 0) >= 3,           "desc": "Jogue 3 dias consecutivos."},
    {"icon": "🌳", "nome": "EcoÁrvore",        "cond": lambda d: d.get("pontos_totais", 0) >= 400,       "desc": "Alcance 400 XP."},
    {"icon": "👑", "nome": "EcoLíder",         "cond": lambda d: d.get("pontos_totais", 0) >= 800,       "desc": "Alcance 800 XP e lidere o movimento."},
]

# ─── ESTADO ───────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = None

if "quiz_respondido" not in st.session_state:
    st.session_state.quiz_respondido = False

if "user_data" not in st.session_state:
    st.session_state.user_data = dados_iniciais()

# ─── CABEÇALHO ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="logo-wrap">
  <div class="logo-pixel">ECOTECH</div>
  <div class="logo-sub">Tecnologia a serviço do planeta</div>
</div>
""", unsafe_allow_html=True)

# ─── LOGIN ────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col1, col2 = st.columns([1.5, 1], gap="large")

    with col1:
        st.markdown(f"""
        <div class="eco-card">
            <h2 style="font-size:20px; margin:0 0 12px;">O que é o EcoTech? 🌍</h2>
            <p style="color:#CBD5E1; line-height:1.7; margin-bottom:12px;">
            O <b style="color:#4ADE80;">EcoTech</b> transforma hábitos sustentáveis em recompensas reais.
            Registre trajetos de bicicleta e transporte público, responda quizzes educativos
            e descubra pontos de descarte consciente perto de você.
            </p>
            <div class="info-box">
            💡 <b>Dica do dia:</b> {dica_do_dia()}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:2px; margin:8px 0 12px;'>Jornada de evolução</p>", unsafe_allow_html=True)
        cols_pat = st.columns(4)
        for i, pat in enumerate(PATENTES):
            with cols_pat[i]:
                st.markdown(f"""
                <div class="emblema-card">
                    <span class="icone">{pat['icon']}</span>
                    <div class="nome">{pat['nome']}</div>
                    <div class="xp-req">{pat['min']}+ XP</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="eco-card">', unsafe_allow_html=True)

        st.markdown(
            "<p style='font-family:\"Press Start 2P\",monospace; font-size:9px; color:var(--muted); letter-spacing:2px; margin-bottom:16px;'>ACESSO AO TERMINAL</p>",
            unsafe_allow_html=True
        )

        u = st.text_input("Usuário", placeholder="seu_usuario")
        p = st.text_input("Senha", type="password", placeholder="••••••••")

        if st.button("▶ INICIAR MISSÃO"):
            try:
                res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()

                if res.data:
                    st.session_state.logged_in = True
                    st.session_state.username = u

                    dados = res.data[0].get("dados_json") or {}
                    dados = normalizar_dados(dados)

                    st.session_state.user_data = dados
                    st.session_state.quiz_feedback = None
                    st.session_state.quiz_respondido = False

                    registrar_acesso("Login realizado")
                    st.rerun()
                else:
                    try:
                        supabase.table("acessos").insert({
                            "username": u,
                            "evento": "login_falha",
                            "detalhes": {},
                            "criado_em": datetime.utcnow().isoformat()
                        }).execute()
                    except Exception:
                        pass
                    st.error("Usuário ou senha inválidos.")

            except Exception as e:
                st.error(f"Erro de conexão: {e}")

        if st.button("📝 CADASTRAR NOVO USUÁRIO"):
            try:
                existente = supabase.table("usuarios").select("*").eq("username", u).execute()

                if existente.data:
                    st.warning("Usuário já existe.")
                else:
                    novo_usuario = {
                        "username": u,
                        "password": p,
                        "dados_json": dados_iniciais()
                    }

                    supabase.table("usuarios").insert(novo_usuario).execute()
                    try:
                        supabase.table("acessos").insert({
                            "username": u,
                            "evento": "cadastro",
                            "detalhes": {},
                            "criado_em": datetime.utcnow().isoformat()
                        }).execute()
                    except Exception:
                        pass
                    st.success("Usuário cadastrado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao cadastrar: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

# ─── APP PRINCIPAL ────────────────────────────────────────────────────────────
else:
    dados = normalizar_dados(st.session_state.user_data)
    st.session_state.user_data = dados

    pts = dados.get("pontos_totais", 0)
    pat = obter_patente(pts)
    pct, faltando, prox = barra_xp(pts)
    hoje_str = str(date.today())

    if dados.get("data_quiz") != hoje_str:
        dados["data_quiz"] = hoje_str
        dados["tentativas_quiz"] = 0
        dados["idx_perguntas_hoje"] = perguntas_do_dia()
        salvar_dados(dados)
        st.session_state.quiz_feedback = None
        st.session_state.quiz_respondido = False

    def atualizar_streak():
        ultima = dados.get("ultima_atividade", "")
        hoje_d = date.today()
        if ultima:
            try:
                delta = (hoje_d - date.fromisoformat(ultima)).days
                if delta == 1:
                    dados["streak_dias"] = dados.get("streak_dias", 0) + 1
                elif delta == 0:
                    dados["streak_dias"] = max(1, dados.get("streak_dias", 0))
                else:
                    dados["streak_dias"] = 1
            except Exception:
                dados["streak_dias"] = 1
        else:
            dados["streak_dias"] = 1
        dados["ultima_atividade"] = hoje_str

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:8px 0 16px;">
            <p style="font-size:11px; color:var(--muted); margin:0 0 2px; letter-spacing:2px; text-transform:uppercase;">Jogador</p>
            <p style="font-size:18px; font-weight:700; margin:0;">{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<span class="badge-patente">{pat["icon"]} {pat["nome"]}</span>', unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:11px; color:var(--muted); margin:8px 0 4px; line-height:1.5;'>{pat['desc']}</p>", unsafe_allow_html=True)

        if prox:
            st.markdown(f"""
            <div style="margin:10px 0 4px;">
                <div class="xp-bar-track"><div class="xp-bar-fill" style="width:{pct}%"></div></div>
                <p class="xp-bar-label">Faltam <b style="color:#E2E8F0;">{faltando} XP</b> para {prox['icon']} {prox['nome']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:11px; color:#FDE047;'>🏆 Nível máximo!</p>", unsafe_allow_html=True)

        streak = dados.get("streak_dias", 0)
        if streak >= 1:
            st.markdown(f"""
            <div class="streak-wrap">
                <span class="streak-num">🔥 {streak}</span>
                <span class="streak-label">dia{'s' if streak>1 else ''} seguido{'s' if streak>1 else ''}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        menu = st.radio("Nav", ["📊 Painel", "🏆 Ranking", "🗺️ Eco-Radar", "🏅 Conquistas"], label_visibility="collapsed")
        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

        if st.button("Sair"):
            registrar_acesso("logout", {})
            st.session_state.logged_in = False
            st.session_state.quiz_feedback = None
            st.session_state.quiz_respondido = False
            st.session_state.user_data = dados_iniciais()
            st.rerun()

    # ── PAINEL ───────────────────────────────────────────────────────────────
    if menu == "📊 Painel":
        st.markdown(f"""
        <div class="dica-card">
            <span class="dica-label">💡 Dica do dia</span>
            <p class="dica-texto">{dica_do_dia()}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("⚡ XP Total", f"{pts} pts")
        c2.metric("🌿 CO₂ Economizado", f"{pts * 0.1:.1f} kg")
        c3.metric("🚲 Trajetos", dados.get("total_trajetos", 0))
        c4.metric("📝 Quiz hoje", f"{dados.get('tentativas_quiz', 0)}/5")

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")

        with col_a:
            with st.expander("🚲 Registrar transporte sustentável", expanded=True):
                st.markdown("""
                <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">
                Bicicleta e caminhada têm emissão zero; ônibus e metrô emitem ~7× menos CO₂
                por passageiro do que o carro particular.
                </p>
                """, unsafe_allow_html=True)

                tempo = st.number_input("Duração (minutos):", 5, 120, 20, key="tempo_t")
                tipo = st.selectbox("Modalidade:", ["🚴 Bike / Caminhada", "🚌 Ônibus / Metrô"], key="tipo_t")
                distancia = st.number_input("Distância estimada (km):", 0.5, 100.0, 5.0, step=0.5, key="dist_t")

                if "Bike" in tipo:
                    co2_salvo = round(distancia * 0.21, 2)
                    xp_ganho = int(tempo * 0.8)
                else:
                    co2_salvo = round(distancia * 0.089, 2)
                    xp_ganho = int(tempo * 0.4)

                st.markdown(f"""
                <div class="info-box">
                    Esta missão vai gerar <b>+{xp_ganho} XP</b> e economizar <b>{co2_salvo} kg de CO₂</b>
                    — equivalente a {co2_salvo / 0.022:.0f} h de absorção de uma árvore adulta.
                </div>
                """, unsafe_allow_html=True)

        if st.button("✅ Confirmar trajeto"):
                    dados["pontos_totais"] += int(tempo * 0.5)
                    dados["total_trajetos"] += 1
                    salvar_dados(dados)

                    registrar_acesso(f"Ação: Transporte ({tipo})") 
                    
                    st.success(f"Trajeto registrado! +{int(tempo * 0.5)} XP | {co2_salvo} kg de CO₂ não emitidos 🌱")
                    st.rerun()

        with col_b:
            with st.expander("🧠 Quiz Sustentável", expanded=True):
                tentativas = dados.get("tentativas_quiz", 0)
                idx_hoje = dados.get("idx_perguntas_hoje", [])

                if tentativas >= 5:
                    st.markdown("""
                    <div style="text-align:center; padding:24px 0;">
                        <div style="font-size:40px; margin-bottom:10px;">🌟</div>
                        <p style="font-weight:600; margin-bottom:4px;">Quiz completo hoje!</p>
                        <p style="font-size:12px; color:var(--muted);">Volte amanhã para novas perguntas.</p>
                    </div>
                    """, unsafe_allow_html=True)

                elif not idx_hoje:
                    st.info("Carregando perguntas...")

                else:
                    idx_q = idx_hoje[tentativas % len(idx_hoje)]
                    item = PERGUNTAS[idx_q]

                    st.markdown(f"""
                    <p style="font-size:10px; color:var(--muted); letter-spacing:2px; text-transform:uppercase; margin-bottom:8px;">
                        Pergunta {tentativas+1} de 5
                    </p>
                    <p style="font-size:15px; font-weight:600; margin-bottom:14px; line-height:1.5;">{item['q']}</p>
                    """, unsafe_allow_html=True)

                    if not st.session_state.quiz_respondido:
                        resp = st.radio(
                            "Escolha:",
                            item["a"],
                            key=f"quiz_{tentativas}",
                            label_visibility="collapsed"
                        )

                        if st.button("📤 Enviar resposta"):
                            atualizar_streak()
                            acertou = resp == item["r"]

                            if acertou:
                                dados["pontos_totais"] += 20
                                dados["total_quizzes_certos"] = dados.get("total_quizzes_certos", 0) + 1
                                mensagem = "✅ Correto! +20 XP"
                                tipo_msg = "success"
                            else:
                                mensagem = f"❌ A resposta certa era: {item['r']}"
                                tipo_msg = "error"

                            resultado = "Acertou" if acertou else "Errou"
                            registrar_acesso(f"Quiz: {resultado} ({item['q']})")

                            st.session_state.quiz_feedback = {
                                "tipo": tipo_msg,
                                "mensagem": mensagem,
                                "exp": item["exp"]
                            }
                            st.session_state.quiz_respondido = True
                            salvar_dados(dados)
                            st.rerun()

                    else:
                        feedback = st.session_state.quiz_feedback

                        if feedback:
                            if feedback["tipo"] == "success":
                                st.success(feedback["mensagem"])
                            else:
                                st.error(feedback["mensagem"])

                            st.markdown(f"""
                            <div class="info-box" style="margin-top:8px;">
                                💡 <b>Saiba mais:</b> {feedback['exp']}
                            </div>
                            """, unsafe_allow_html=True)

                        if st.button("➡️ Próxima pergunta"):
                            dados["tentativas_quiz"] += 1
                            salvar_dados(dados)
                            st.session_state.quiz_feedback = None
                            st.session_state.quiz_respondido = False
                            st.rerun()

    # ── RANKING ──────────────────────────────────────────────────────────────
    elif menu == "🏆 Ranking":
        st.markdown("<h2 style='font-size:20px; margin-bottom:4px;'>🏆 Ranking Global</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:var(--muted); margin-bottom:20px;'>Os maiores agentes de mudança do planeta.</p>", unsafe_allow_html=True)

        try:
            res = supabase.table("usuarios").select("username, dados_json").execute()
            jogadores = sorted(
                [{"nome": u["username"], "xp": normalizar_dados(u["dados_json"]).get("pontos_totais", 0)} for u in res.data],
                key=lambda x: x["xp"], reverse=True
            )
            medals = ["🥇", "🥈", "🥉"]
            for i, j in enumerate(jogadores):
                pat_j = obter_patente(j["xp"])
                pos = medals[i] if i < 3 else f"#{i+1}"
                destaque = "color: #FDE047 !important; font-weight:700;" if j["nome"] == st.session_state.username else ""
                st.markdown(f"""
                <div class="rank-row">
                    <span class="rank-pos">{pos}</span>
                    <span style="font-size:20px">{pat_j['icon']}</span>
                    <span class="rank-name" style="{destaque}">{j['nome']}</span>
                    <span style="font-size:11px; color:var(--muted); margin-right:8px;">{pat_j['nome']}</span>
                    <span class="rank-xp">{j['xp']} XP</span>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao carregar ranking: {e}")

        st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:16px; margin-bottom:16px;'>🌿 Jornada de Evolução</h3>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, p in enumerate(PATENTES):
            with cols[i]:
                ativo = pts >= p["min"]
                st.markdown(f"""
                <div class="emblema-card {'ativo' if ativo else ''}" style="{'opacity:0.45' if not ativo else ''}">
                    <span class="icone">{p['icon']}</span>
                    <div class="nome">{p['nome']}</div>
                    <div class="xp-req">a partir de {p['min']} XP</div>
                    <p class="desc-pat">{p['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

    # ── ECO-RADAR ─────────────────────────────────────────────────────────────
    elif menu == "🗺️ Eco-Radar":
        st.markdown("<h2 style='font-size:20px; margin-bottom:4px;'>🗺️ Eco-Radar</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:var(--muted); margin-bottom:20px;'>Encontre pontos de descarte consciente próximos a você.</p>", unsafe_allow_html=True)

        ECOPONTOS = [
            {"nome": "Ecoponto Lapa",         "lat": -23.525, "lon": -46.700, "icon": "♻️", "tags": ["Metal","Vidro","Eletrônicos"],    "horario": "Seg–Sáb 8h–17h"},
            {"nome": "Ecoponto Pinheiros",   "lat": -23.566, "lon": -46.683, "icon": "🌿", "tags": ["Orgânico","Papel","Plástico"],    "horario": "Seg–Sex 7h–19h"},
            {"nome": "Cooperativa Verde Vida","lat": -23.551, "lon": -46.634, "icon": "🤝", "tags": ["Reciclagem geral"],              "horario": "Seg–Sex 8h–16h"},
            {"nome": "Ecoponto Mooca",       "lat": -23.547, "lon": -46.606, "icon": "🏗️", "tags": ["Entulho","Eletrônicos","Móveis"], "horario": "Ter–Dom 8h–17h"},
            {"nome": "Coleta PMSP – Santana","lat": -23.493, "lon": -46.628, "icon": "🔋", "tags": ["Pilhas","Baterias","Remédios"],   "horario": "Seg–Sex 9h–17h"},
        ]

        CATEGORIAS = [
            ("♻️", "Seco Reciclável",   "Papel, plástico, metal, vidro → Coleta seletiva ou ecoponto"),
            ("🥦", "Orgânico",          "Restos de comida → Compostagem ou coleta municipal"),
            ("💻", "E-lixo",            "Celulares, cabos, baterias → Ecopontos especializados"),
            ("💊", "Medicamentos",      "Remédios vencidos → Farmácias parceiras ou PMSP"),
            ("🔋", "Pilhas e baterias", "Nunca no lixo comum → Supermercados e ecopontos"),
            ("🏗️", "Entulho",           "Resíduos de obra → Ecopontos específicos para entulho"),
        ]

        cep = st.text_input("🔍 Endereço ou CEP:", placeholder="Ex: Av. Paulista, 1000 ou 01310-100")

        if cep:
            st.success(f"Mostrando ecopontos para: **{cep}**")
            st.caption("⚠️ Em produção, integre a API da Prefeitura ou Google Places para dados reais.")

            df_mapa = pd.DataFrame([{"lat": p["lat"], "lon": p["lon"]} for p in ECOPONTOS])
            st.map(df_mapa, zoom=11)

            st.markdown("<h3 style='font-size:15px; margin:20px 0 12px;'>Pontos encontrados</h3>", unsafe_allow_html=True)
            for ep in ECOPONTOS:
                tags_html = "".join([f'<span class="eco-ponto-tag">{t}</span>' for t in ep["tags"]])
                st.markdown(f"""
                <div class="eco-ponto">
                    <span class="eco-ponto-icon">{ep['icon']}</span>
                    <div>
                        <div class="eco-ponto-nome">{ep['nome']}</div>
                        <div class="eco-ponto-info">🕐 {ep['horario']}</div>
                        <div style="margin-top:6px">{tags_html}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='font-size:15px; margin-bottom:14px;'>📖 O que descartar onde?</h3>", unsafe_allow_html=True)
            cols_cat = st.columns(2)
            for i, (icon, nome, desc) in enumerate(CATEGORIAS):
                with cols_cat[i % 2]:
                    st.markdown(f"""
                    <div class="eco-ponto">
                        <span class="eco-ponto-icon">{icon}</span>
                        <div>
                            <div class="eco-ponto-nome">{nome}</div>
                            <div class="eco-ponto-info">{desc}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── CONQUISTAS ────────────────────────────────────────────────────────────
    elif menu == "🏅 Conquistas":
        st.markdown("<h2 style='font-size:20px; margin-bottom:4px;'>🏅 Suas Conquistas</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:var(--muted); margin-bottom:20px;'>Complete missões para desbloquear emblemas exclusivos.</p>", unsafe_allow_html=True)

        conquistas = [{"icon": c["icon"], "nome": c["nome"], "desc": c["desc"], "desbloqueada": c["cond"](dados)} for c in CONQUISTAS_DEF]
        desbloqueadas = sum(1 for c in conquistas if c["desbloqueada"])
        pct_c = int(desbloqueadas / len(conquistas) * 100)

        st.markdown(f"""
        <div class="eco-card" style="margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted); margin-bottom:6px;">Progresso geral</p>
            <p style="font-size:22px; font-weight:700; margin:0 0 8px;">{desbloqueadas} / {len(conquistas)} desbloqueadas</p>
            <div class="xp-bar-track"><div class="xp-bar-fill" style="width:{pct_c}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        cols_c = st.columns(3)
        for i, c in enumerate(conquistas):
            with cols_c[i % 3]:
                opacidade = "1" if c["desbloqueada"] else "0.35"
                filtro_img = "grayscale(0)" if c["desbloqueada"] else "grayscale(1)"
                st.markdown(f"""
                <div class="conquista {'desbloqueada' if c['desbloqueada'] else ''}" style="opacity:{opacidade}">
                    <span class="c-icon" style="filter:{filtro_img}">{c['icon']}</span>
                    <span class="c-nome">{c['nome']}</span>
                </div>
                """, unsafe_allow_html=True)
                if not c["desbloqueada"]:
                    st.caption(c["desc"])
