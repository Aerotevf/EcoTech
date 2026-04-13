import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

[data-testid="stAppViewContainer"] {
    background: #F2F7EE !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #D8EAD0;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Tipografia geral ── */
h1, h2, h3, h4, p, li, span, label, div {
    font-family: 'DM Sans', sans-serif !important;
    color: #1A2E1A !important;
}

/* ── Logo ── */
.logo-wrap {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 2px;
    margin: 0 0 8px;
}
.logo-eco {
    font-family: 'Syne', sans-serif !important;
    font-size: 64px;
    font-weight: 800;
    color: #2D7A3A !important;
    letter-spacing: -2px;
    line-height: 1;
}
.logo-tech {
    font-family: 'Syne', sans-serif !important;
    font-size: 64px;
    font-weight: 700;
    color: #1A2E1A !important;
    letter-spacing: -2px;
    line-height: 1;
}
.logo-dot {
    width: 10px; height: 10px;
    background: #5BBF6A;
    border-radius: 50%;
    display: inline-block;
    margin-left: 4px;
    margin-bottom: 14px;
}
.tagline {
    text-align: center;
    font-size: 14px;
    color: #5C7A5C !important;
    margin-top: -4px;
    margin-bottom: 24px;
    letter-spacing: 0.02em;
}

/* ── Cards ── */
.card {
    background: #FFFFFF;
    border: 1px solid #D8EAD0;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.card-icon {
    width: 36px; height: 36px;
    background: #E8F5E0;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.card-title {
    font-size: 15px;
    font-weight: 600;
    color: #1A2E1A !important;
    margin: 0;
}

/* ── Stat cards ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.stat-card {
    background: #FFFFFF;
    border: 1px solid #D8EAD0;
    border-radius: 12px;
    padding: 14px 12px;
    text-align: center;
}
.stat-value {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px;
    font-weight: 800;
    color: #2D7A3A !important;
    line-height: 1.1;
}
.stat-label {
    font-size: 11px;
    color: #5C7A5C !important;
    margin-top: 2px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Barra XP ── */
.xp-wrap { margin: 10px 0 4px; }
.xp-bar-bg {
    background: #E0EED8;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
}
.xp-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: #2D7A3A;
    transition: width 0.6s ease;
}
.xp-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #5C7A5C !important;
    margin-top: 4px;
}

/* ── Botões de ação rápida ── */
.quick-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 8px;
}
.quick-btn {
    background: #F2F7EE;
    border: 1.5px solid #C5DFBA;
    border-radius: 12px;
    padding: 14px 12px;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s, transform 0.1s;
    text-align: left;
    display: block;
    width: 100%;
}
.quick-btn:hover {
    background: #E4F0DB;
    border-color: #2D7A3A;
    transform: translateY(-1px);
}
.quick-btn-icon { font-size: 22px; display: block; margin-bottom: 6px; }
.quick-btn-name {
    font-size: 13px;
    font-weight: 600;
    color: #1A2E1A !important;
    display: block;
}
.quick-btn-pts {
    font-size: 12px;
    color: #2D7A3A !important;
    font-weight: 600;
}

/* ── Badge de streak ── */
.streak-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FFF3E0;
    border: 1px solid #FFCC80;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 13px;
    font-weight: 600;
    color: #E65100 !important;
}

/* ── Desafios ── */
.challenge-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #EEF5E8;
}
.challenge-check {
    width: 22px; height: 22px;
    border-radius: 50%;
    border: 2px solid #C5DFBA;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
}
.challenge-check.done {
    background: #2D7A3A;
    border-color: #2D7A3A;
    color: white !important;
}
.challenge-text {
    flex: 1;
    font-size: 13px;
    color: #1A2E1A !important;
}
.challenge-pts {
    font-size: 12px;
    font-weight: 600;
    color: #2D7A3A !important;
    white-space: nowrap;
}

/* ── Impacto ── */
.impact-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 4px;
}
.impact-pill {
    background: #E8F5E0;
    border-radius: 10px;
    padding: 10px 8px;
    text-align: center;
}
.impact-num {
    font-family: 'Syne', sans-serif !important;
    font-size: 18px;
    font-weight: 800;
    color: #2D7A3A !important;
}
.impact-desc {
    font-size: 10px;
    color: #4A7A4A !important;
    margin-top: 2px;
    line-height: 1.3;
}

/* ── Quiz ── */
.quiz-question {
    font-size: 15px;
    font-weight: 600;
    color: #1A2E1A !important;
    margin-bottom: 12px;
    line-height: 1.5;
}

/* ── Histórico ── */
.hist-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #EEF5E8;
    font-size: 13px;
}
.hist-pts {
    font-weight: 700;
    color: #2D7A3A !important;
    white-space: nowrap;
}
.hist-date { color: #8AAA8A !important; font-size: 11px; }

/* ── Botões Streamlit ── */
.stButton > button {
    background: #2D7A3A !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 8px 20px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #1F5C2A !important;
    color: #FFFFFF !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] select {
    border-radius: 10px !important;
    border: 1.5px solid #C5DFBA !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #2D7A3A !important;
    box-shadow: 0 0 0 3px rgba(45,122,58,0.12) !important;
}

/* ── Sidebar ── */
.sidebar-nivel {
    background: #F2F7EE;
    border-radius: 12px;
    padding: 12px 14px;
    margin: 8px 0;
}
.nivel-emoji { font-size: 28px; display: block; text-align: center; margin-bottom: 4px; }
.nivel-nome {
    font-family: 'Syne', sans-serif !important;
    font-size: 16px;
    font-weight: 800;
    color: #2D7A3A !important;
    text-align: center;
}

/* ── Notificações ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
}

/* ── Toast de pontos ── */
.pts-toast {
    background: #2D7A3A;
    color: white !important;
    border-radius: 12px;
    padding: 14px 20px;
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    margin: 8px 0;
    animation: pop 0.3s ease;
}
@keyframes pop {
    0% { transform: scale(0.8); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

/* ── Mensagem motivacional ── */
.motivation {
    background: linear-gradient(135deg, #E8F5E0, #F0F9EA);
    border-left: 4px solid #2D7A3A;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    font-size: 13px;
    font-style: italic;
    color: #2D5A2D !important;
    margin: 8px 0 16px;
}

/* Esconder elementos padrão do Streamlit */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── SUPABASE ──────────────────────────────────────────────────────────────────
URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

# ─── CONSTANTES ───────────────────────────────────────────────────────────────
DEFAULT_USER_DATA = {
    "pontos_totais": 0,
    "historico": [],
    "quiz_date": datetime.date.min.strftime('%Y-%m-%d'),
    "quiz_answered_today": False,
    "quiz_index": 0,
    "streak": 0,
    "ultimo_acesso": datetime.date.min.strftime('%Y-%m-%d'),
    "badges": [],
    "acoes_hoje": 0,
    "acoes_semana": 0,
    "semana_ref": "",
}

QUIZ_PONTOS = 30

QUIZ_PERGUNTAS = [
    {"pergunta": "Qual é a principal causa do aquecimento global?", "opcoes": ["Aumento da energia solar", "Emissão de gases de efeito estufa", "Erupções vulcânicas"], "resposta": "Emissão de gases de efeito estufa"},
    {"pergunta": "Qual o principal benefício de usar sacolas reutilizáveis?", "opcoes": ["São mais bonitas", "Redução da produção de lixo plástico", "São mais baratas"], "resposta": "Redução da produção de lixo plástico"},
    {"pergunta": "O que significa 'pegada de carbono'?", "opcoes": ["A marca que você deixa ao andar", "O total de gases de efeito estufa emitidos", "A quantidade de árvores plantadas"], "resposta": "O total de gases de efeito estufa emitidos"},
    {"pergunta": "Qual é o destino mais sustentável para óleo de cozinha usado?", "opcoes": ["Descartar no ralo", "Guardar e reciclar em postos de coleta", "Jogar no lixo comum"], "resposta": "Guardar e reciclar em postos de coleta"},
    {"pergunta": "O que a sigla ODS representa?", "opcoes": ["Organização de Descarte Sustentável", "Objetivos de Desenvolvimento Sustentável", "Operações Diárias de Saneamento"], "resposta": "Objetivos de Desenvolvimento Sustentável"},
    {"pergunta": "Qual fonte de energia é considerada mais renovável?", "opcoes": ["Carvão mineral", "Energia solar", "Gás natural"], "resposta": "Energia solar"},
    {"pergunta": "O que é compostagem?", "opcoes": ["Um tipo de reciclagem de metais", "Transformação de resíduos orgânicos em adubo", "Tratamento de água residual"], "resposta": "Transformação de resíduos orgânicos em adubo"},
]

ACOES_RAPIDAS = [
    {"nome": "Fui de bike ou a pé", "icone": "🚲", "pontos": 20, "co2": 0.5},
    {"nome": "Usei garrafa reutilizável", "icone": "💧", "pontos": 10, "co2": 0.1},
    {"nome": "Evitei sacola plástica", "icone": "♻️", "pontos": 8, "co2": 0.05},
    {"nome": "Economizei energia em casa", "icone": "💡", "pontos": 12, "co2": 0.3},
    {"nome": "Comi refeição vegetal", "icone": "🥗", "pontos": 15, "co2": 0.8},
    {"nome": "Descartei eletrônico", "icone": "📱", "pontos": 40, "co2": 0.0},
]

LIMITES = {
    1: (0, 100, "Semente", "🌱"),
    2: (100, 250, "Broto", "🌿"),
    3: (250, 500, "Árvore Jovem", "🌳"),
    4: (500, 900, "EcoLíder", "🌲"),
    5: (900, 9999, "Guardião", "👑"),
}

FRASES_MOTIVACAO = [
    "Cada ação conta. O planeta agradece! 🌍",
    "Você está construindo um futuro melhor, passo a passo. 💚",
    "Pequenos gestos, grande impacto. Continue assim!",
    "Sustentabilidade não é um destino, é um estilo de vida. 🌿",
    "Você inspira as pessoas ao seu redor. Parabéns! ✨",
    "O futuro pertence a quem age hoje. 🌱",
]

BADGES_DISPONIVEIS = [
    {"id": "primeiro_passo", "nome": "Primeiro Passo", "icone": "🥇", "descricao": "Registrou sua primeira ação", "condicao": lambda d: d["pontos_totais"] >= 1},
    {"id": "eco_iniciante", "nome": "Eco Iniciante", "icone": "🌱", "descricao": "Atingiu 50 pontos", "condicao": lambda d: d["pontos_totais"] >= 50},
    {"id": "streak_3", "nome": "3 Dias Seguidos", "icone": "🔥", "descricao": "Manteve sequência por 3 dias", "condicao": lambda d: d.get("streak", 0) >= 3},
    {"id": "quiz_mestre", "nome": "Quiz Mestre", "icone": "🧠", "descricao": "Respondeu quiz corretamente", "condicao": lambda d: d.get("quiz_answered_today", False)},
    {"id": "eco_lider", "nome": "EcoLíder", "icone": "🏆", "descricao": "Atingiu 300 pontos", "condicao": lambda d: d["pontos_totais"] >= 300},
]

PONTOS_COLETA = pd.DataFrame({
    'lat': [-23.5505, -23.545, -23.560],
    'lon': [-46.6333, -46.640, -46.625],
    'nome': ['Eco Ponto Central', 'Recicla Fácil SP', 'Posto de Óleo'],
    'tipo': ['Eletrônicos/Pilhas', 'Plástico/Papel', 'Óleo de Cozinha'],
})

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def registrar_log(username, acao):
    try:
        supabase.table("acessos").insert({"usuario": username, "acao": acao}).execute()
    except:
        pass

def carregar_dados_usuario(username):
    res = supabase.table("usuarios").select("dados_json").eq("username", username).execute()
    if res.data:
        dados = res.data[0]["dados_json"]
        # garante chaves novas para usuários antigos
        for k, v in DEFAULT_USER_DATA.items():
            if k not in dados:
                dados[k] = v
        return dados
    return DEFAULT_USER_DATA.copy()

def salvar_dados_usuario(username, user_data):
    res = supabase.table("usuarios").select("password").eq("username", username).execute()
    pw = res.data[0]["password"] if res.data else "123"
    supabase.table("usuarios").upsert({"username": username, "password": pw, "dados_json": user_data}).execute()

def calcular_nivel(pontos):
    nivel_num = 1
    for n, (piso, teto, nome, emoji) in LIMITES.items():
        if pontos >= piso:
            nivel_num = n
    n = nivel_num
    piso, teto, nome, emoji = LIMITES[n]
    if n == max(LIMITES.keys()):
        return n, nome, emoji, 1.0, 0, 0
    span = teto - piso
    feito = pontos - piso
    progresso = min(feito / span, 1.0)
    return n, nome, emoji, progresso, span, feito

def atualizar_streak(user_data):
    hoje = datetime.date.today().strftime('%Y-%m-%d')
    ontem = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    ultimo = user_data.get("ultimo_acesso", "")
    if ultimo == hoje:
        return user_data
    if ultimo == ontem:
        user_data["streak"] = user_data.get("streak", 0) + 1
    elif ultimo != hoje:
        user_data["streak"] = 1
    user_data["ultimo_acesso"] = hoje
    return user_data

def verificar_badges(user_data):
    novos = []
    badges_atuais = user_data.get("badges", [])
    for badge in BADGES_DISPONIVEIS:
        if badge["id"] not in badges_atuais:
            try:
                if badge["condicao"](user_data):
                    badges_atuais.append(badge["id"])
                    novos.append(badge)
            except:
                pass
    user_data["badges"] = badges_atuais
    return user_data, novos

def pontos_para_co2(pontos):
    """Aproximação didática: cada ponto ~ 10g CO₂"""
    return round(pontos * 10 / 1000, 2)

def pontos_para_km(pontos):
    """Cada 20 pts ~ 1km de carro não usado"""
    return round(pontos / 20, 1)

def pontos_para_arvores(pontos):
    """100 pts ~ plantar 1 árvore (didático)"""
    return round(pontos / 100, 1)

def exibir_logo():
    st.markdown("""
        <div class="logo-wrap">
            <span class="logo-eco">ECO</span>
            <span class="logo-tech">TECH</span>
            <span class="logo-dot"></span>
        </div>
        <p class="tagline">Transforme hábitos sustentáveis em conquistas</p>
    """, unsafe_allow_html=True)

# ─── TELA LOGIN ───────────────────────────────────────────────────────────────

def tela_login():
    exibir_logo()
    st.markdown('<div class="card">', unsafe_allow_html=True)
    tab_login, tab_register = st.tabs(["Entrar", "Criar conta"])
    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Usuário", placeholder="seu_usuario")
            pw = st.text_input("Senha", type="password", placeholder="••••••••")
            if st.form_submit_button("Entrar →", use_container_width=True):
                login(user, pw)
    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("Usuário", placeholder="escolha_um_usuario")
            new_pw = st.text_input("Senha", type="password", placeholder="••••••••")
            conf_pw = st.text_input("Confirmar senha", type="password", placeholder="••••••••")
            if st.form_submit_button("Criar conta →", use_container_width=True):
                if not new_user:
                    st.error("Preencha o usuário.")
                elif new_pw != conf_pw:
                    st.error("Senhas não coincidem.")
                else:
                    registrar_usuario(new_user, new_pw)
    st.markdown('</div>', unsafe_allow_html=True)

def registrar_usuario(username, password):
    res = supabase.table("usuarios").select("username").eq("username", username).execute()
    if res.data:
        st.error("Usuário já existe. Escolha outro nome.")
        return False
    supabase.table("usuarios").insert({"username": username, "password": password, "dados_json": DEFAULT_USER_DATA.copy()}).execute()
    registrar_log(username, "Novo cadastro")
    st.success(f"Conta criada! Agora faça login.")
    return True

def login(username, password):
    res = supabase.table("usuarios").select("*").eq("username", username).execute()
    if res.data and res.data[0]['password'] == password:
        user_data = res.data[0]['dados_json']
        for k, v in DEFAULT_USER_DATA.items():
            if k not in user_data:
                user_data[k] = v
        user_data = atualizar_streak(user_data)
        salvar_dados_usuario(username, user_data)
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_data = user_data
        registrar_log(username, "Login")
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos.")

def logout():
    registrar_log(st.session_state.username, "Logout")
    for k in ["logged_in", "username", "user_data"]:
        st.session_state.pop(k, None)
    st.rerun()

# ─── APP PRINCIPAL ────────────────────────────────────────────────────────────

def registrar_acao(acao_nome, pontos, co2=0.0):
    ud = st.session_state.user_data
    ud["pontos_totais"] += pontos
    ud["acoes_hoje"] = ud.get("acoes_hoje", 0) + 1
    ud["historico"].append({
        "Ação": acao_nome,
        "Pontos": pontos,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M"),
    })
    ud = atualizar_streak(ud)
    ud, novos_badges = verificar_badges(ud)
    salvar_dados_usuario(st.session_state.username, ud)
    registrar_log(st.session_state.username, f"Ação: {acao_nome}")
    st.session_state.user_data = ud
    # feedback
    frase = random.choice(FRASES_MOTIVACAO)
    st.markdown(f'<div class="pts-toast">+{pontos} pontos! 🎉</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="motivation">{frase}</div>', unsafe_allow_html=True)
    for b in novos_badges:
        st.success(f"🏅 Novo badge desbloqueado: **{b['icone']} {b['nome']}** — {b['descricao']}")
    st.rerun()

def registrar_pontos_quiz(pergunta):
    ud = st.session_state.user_data
    ud["pontos_totais"] += QUIZ_PONTOS
    ud["quiz_answered_today"] = True
    ud["historico"].append({
        "Ação": "Quiz Diário ✓",
        "Pontos": QUIZ_PONTOS,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M"),
    })
    ud, novos_badges = verificar_badges(ud)
    salvar_dados_usuario(st.session_state.username, ud)
    registrar_log(st.session_state.username, "Quiz respondido")
    st.session_state.user_data = ud
    st.markdown(f'<div class="pts-toast">+{QUIZ_PONTOS} pontos! Resposta correta! 🧠</div>', unsafe_allow_html=True)
    for b in novos_badges:
        st.success(f"🏅 **{b['icone']} {b['nome']}** desbloqueado!")
    st.rerun()

def gerar_quiz_diario():
    ud = st.session_state.user_data
    hoje = datetime.date.today()
    ultimo_quiz = datetime.datetime.strptime(ud.get("quiz_date", "2000-01-01"), '%Y-%m-%d').date()
    if hoje > ultimo_quiz:
        random.seed(hoje.day + hoje.month * 31 + hoje.year)
        ud["quiz_date"] = hoje.strftime('%Y-%m-%d')
        ud["quiz_index"] = random.randint(0, len(QUIZ_PERGUNTAS) - 1)
        ud["quiz_answered_today"] = False
        salvar_dados_usuario(st.session_state.username, ud)
        st.session_state.user_data = ud
    return QUIZ_PERGUNTAS[ud.get("quiz_index", 0)]

def main_app():
    ud = st.session_state.user_data
    n_num, nome_nivel, emoji_nivel, progresso, span, feito = calcular_nivel(ud["pontos_totais"])
    streak = ud.get("streak", 0)

    # ── SIDEBAR ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-nivel">
            <span class="nivel-emoji">{emoji_nivel}</span>
            <p class="nivel-nome">{nome_nivel}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="xp-wrap">
            <div class="xp-bar-bg">
                <div class="xp-bar-fill" style="width:{int(progresso*100)}%"></div>
            </div>
            <div class="xp-labels">
                <span>{ud['pontos_totais']} pts</span>
                <span>Nível {n_num+1} → {ud['pontos_totais'] + (span - feito) if span > 0 else '∞'} pts</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if streak > 0:
            st.markdown(f'<div class="streak-badge">🔥 {streak} dias seguidos!</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Badges
        badges_usuario = ud.get("badges", [])
        if badges_usuario:
            st.markdown("**Suas conquistas**")
            cols = st.columns(4)
            for i, bid in enumerate(badges_usuario):
                badge = next((b for b in BADGES_DISPONIVEIS if b["id"] == bid), None)
                if badge:
                    cols[i % 4].markdown(f"<span title='{badge['nome']}'>{badge['icone']}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.button("Sair", on_click=logout, use_container_width=True)
        if st.button("🔴 Zerar pontos", use_container_width=True):
            ud["pontos_totais"] = 0
            ud["historico"] = []
            ud["streak"] = 0
            salvar_dados_usuario(st.session_state.username, ud)
            st.session_state.user_data = ud
            st.rerun()

    # ── CABEÇALHO ────────────────────────────────────────────────────────────
    exibir_logo()
    st.markdown(f"<p style='text-align:center;font-size:16px;margin-bottom:8px;'>Olá, <b>{st.session_state.username}</b>! 👋</p>", unsafe_allow_html=True)

    # ── STATS ────────────────────────────────────────────────────────────────
    co2 = pontos_para_co2(ud["pontos_totais"])
    km = pontos_para_km(ud["pontos_totais"])
    arvores = pontos_para_arvores(ud["pontos_totais"])

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">{ud['pontos_totais']}</div>
            <div class="stat-label">pontos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{streak}🔥</div>
            <div class="stat-label">dias seguidos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(ud['historico'])}</div>
            <div class="stat-label">ações feitas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── IMPACTO REAL ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">🌍</div>
            <p class="card-title">Seu impacto real</p>
        </div>
        <div class="impact-row">
            <div class="impact-pill">
                <div class="impact-num">{co2} kg</div>
                <div class="impact-desc">CO₂ evitado</div>
            </div>
            <div class="impact-pill">
                <div class="impact-num">{km} km</div>
                <div class="impact-desc">sem carro</div>
            </div>
            <div class="impact-pill">
                <div class="impact-num">{arvores}</div>
                <div class="impact-desc">árvores equiv.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AÇÕES RÁPIDAS ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">⚡</div>
            <p class="card-title">O que você fez hoje?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, acao in enumerate(ACOES_RAPIDAS):
        with cols[i % 2]:
            if st.button(
                f"{acao['icone']}  {acao['nome']}\n+{acao['pontos']} pts",
                key=f"acao_{i}",
                use_container_width=True,
            ):
                registrar_acao(acao["nome"], acao["pontos"], acao.get("co2", 0))

    # ── DESAFIO DA SEMANA ─────────────────────────────────────────────────────
    semana_atual = datetime.date.today().strftime("%Y-W%W")
    total_acoes = len([h for h in ud["historico"] if h.get("Data/Hora", "")[:5] >= (datetime.date.today() - datetime.timedelta(days=7)).strftime("%d/%m")])
    quiz_ok = ud.get("quiz_answered_today", False)
    streak_ok = streak >= 3

    desafios = [
        {"texto": "Registre 5 ações sustentáveis esta semana", "pts": 50, "done": total_acoes >= 5},
        {"texto": "Responda o quiz de hoje", "pts": 30, "done": quiz_ok},
        {"texto": "Mantenha 3 dias seguidos", "pts": 40, "done": streak_ok},
    ]

    itens_html = ""
    for d in desafios:
        check_class = "done" if d["done"] else ""
        check_icon = "✓" if d["done"] else ""
        style = "text-decoration: line-through; color: #8AAA8A !important;" if d["done"] else ""
        itens_html += f"""
        <div class="challenge-item">
            <div class="challenge-check {check_class}">{check_icon}</div>
            <span class="challenge-text" style="{style}">{d['texto']}</span>
            <span class="challenge-pts">+{d['pts']}</span>
        </div>
        """

    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">🏆</div>
            <p class="card-title">Desafios da semana</p>
        </div>
        {itens_html}
    </div>
    """, unsafe_allow_html=True)

    # ── QUIZ ─────────────────────────────────────────────────────────────────
    pergunta = gerar_quiz_diario()
    ud = st.session_state.user_data  # refresh após possível rerun do quiz

    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">🧠</div>
            <p class="card-title">Quiz diário</p>
        </div>
    """, unsafe_allow_html=True)

    if ud.get("quiz_answered_today"):
        st.info("Você já respondeu o quiz de hoje! Volte amanhã para uma nova pergunta. 🗓️")
    else:
        st.markdown(f'<p class="quiz-question">{pergunta["pergunta"]}</p>', unsafe_allow_html=True)
        resp = st.radio("", pergunta["opcoes"], key="quiz_resp", label_visibility="collapsed")
        if st.button("Responder →", key="quiz_btn"):
            if resp == pergunta["resposta"]:
                registrar_pontos_quiz(pergunta)
            else:
                st.error(f"Incorreto. A resposta certa era: **{pergunta['resposta']}**. Tente amanhã!")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── MAPA ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">📍</div>
            <p class="card-title">Pontos de coleta próximos</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.map(PONTOS_COLETA, latitude='lat', longitude='lon', size=60, color='#2D7A3A')

    # ── HISTÓRICO ─────────────────────────────────────────────────────────────
    historico = ud["historico"]
    if historico:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <div class="card-icon">📋</div>
                <p class="card-title">Histórico de ações</p>
            </div>
        """, unsafe_allow_html=True)
        itens = ""
        for h in reversed(historico[-15:]):
            itens += f"""
            <div class="hist-row">
                <div>
                    <span style="font-size:13px;color:#1A2E1A;">{h['Ação']}</span><br>
                    <span class="hist-date">{h.get('Data/Hora','')}</span>
                </div>
                <span class="hist-pts">+{h['Pontos']} pts</span>
            </div>
            """
        st.markdown(itens + "</div>", unsafe_allow_html=True)


# ─── ROTEADOR ─────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    tela_login()
