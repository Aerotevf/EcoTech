import streamlit as st
import datetime
import json
import os
import pandas as pd
import random
from supabase import create_client, Client

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;900&display=swap');
    [data-testid="stAppViewContainer"] {
        background-color: #F0FFF0 !important;
        color: #000000 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    .main-logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -50px;
        margin-bottom: 20px;
    }
    .logo-eco {
        font-family: 'Poppins', sans-serif;
        font-size: 80px;
        font-weight: 900;
        color: #00A020 !important;
        margin-right: 8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }
    .logo-tech {
        font-family: 'Poppins', sans-serif;
        font-size: 80px;
        font-weight: 900;
        color: #111111 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }
    [data-testid="stNotification"], [data-testid="stInfo"] {
        border-left: 8px solid #008000 !important;
        background-color: #FFFFFF !important;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #008000 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #006400 !important;
        color: #FFFFFF !important;
    }
    h1, h2, h3, p, li, span, label {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

URL_DB = "https://cusjupdmiqxgtwbubynu.supabase.co"
KEY_DB = "sb_publishable_LDsAzMOj3NCHso8nVAeTMQ_WBzj3rb7"
supabase: Client = create_client(URL_DB, KEY_DB)

def registrar_log(username, acao):
    supabase.table("acessos").insert({"usuario": username, "acao": acao}).execute()

def exibir_logo_centralizado():
    st.markdown("""
        <div class="main-logo-container">
            <span class="logo-eco">ECO</span>
            <span class="logo-tech">TECH</span>
        </div>
    """, unsafe_allow_html=True)

DEFAULT_USER_DATA = {
    "pontos_totais": 0,
    "historico": [],
    "quiz_date": datetime.date.min.strftime('%Y-%m-%d'),
    "quiz_answered_today": False,
    "nivel_anterior": "Semente"
}

QUIZ_PONTOS = 25

QUIZ_PERGUNTAS = [
    {"pergunta": "Qual é a principal causa do aquecimento global?", "opcoes": ["Aumento da energia solar", "Emissão de gases de efeito estufa", "Erupções vulcânicas"], "resposta": "Emissão de gases de efeito estufa"},
    {"pergunta": "Qual o principal benefício de usar sacolas reutilizáveis?", "opcoes": ["São mais bonitas", "Redução da produção de lixo plástico", "São mais baratas"], "resposta": "Redução da produção de lixo plástico"},
    {"pergunta": "O que significa 'pegada de carbono'?", "opcoes": ["A marca que você deixa ao andar", "O total de gases de efeito estufa emitidos", "A quantidade de árvores plantadas"], "resposta": "O total de gases de efeito estufa emitidos"},
    {"pergunta": "Qual é o destino mais sustentável para óleo de cozinha usado?", "opcoes": ["Descartar no ralo", "Guardar e reciclar em postos de coleta", "Jogar no lixo comum"], "resposta": "Guardar e reciclar em postos de coleta"},
    {"pergunta": "O que a sigla ODS representa?", "opcoes": ["Organização de Descarte Sustentável", "Objetivos de Desenvolvimento Sustentável", "Operações Diárias de Saneamento"], "resposta": "Objetivos de Desenvolvimento Sustentável"},
]

PONTOS_COLETA = pd.DataFrame({
    'lat': [-23.5505, -23.545, -23.560],
    'lon': [-46.6333, -46.640, -46.625],
    'nome': ['Eco Ponto Central', 'Recicla Fácil SP', 'Posto de Óleo'],
    'tipo': ['Eletrônicos/Pilhas', 'Plástico/Papel', 'Óleo de Cozinha'],
    'rua': ['Av. Paulista', 'R. Augusta', 'Av. Rebouças'],
    'numero': ['1000', '2500', '400'],
    'bairro': ['Bela Vista', 'Cerqueira César', 'Pinheiros'],
    'cep': ['01310-100', '01412-100', '05401-000'],
    'horario': ['Seg-Sex: 9h às 18h', 'Seg-Sáb: 10h às 19h', 'Ter-Sáb: 8h às 17h'],
})

limites = {
    1: (0, 50, "Semente"),
    2: (50, 150, "Broto"),
    3: (150, 300, "Árvore Jovem"),
    4: (300, 500, "EcoLíder")
}

MAPA_EMBLEMAS_EMOJI = {
    "Semente": "🌱",
    "Broto": "🌿",
    "Árvore Jovem": "🌳",
    "EcoLíder": "👑"
}

def carregar_todos_dados():
    res = supabase.table("usuarios").select("*").execute()
    all_data = {"__credentials__": {}}
    for user in res.data:
        all_data["__credentials__"][user["username"]] = user["password"]
        all_data[user["username"]] = user["dados_json"]
    return all_data

def carregar_dados_usuario(username):
    res = supabase.table("usuarios").select("dados_json").eq("username", username).execute()
    if res.data:
        return res.data[0]["dados_json"]
    return DEFAULT_USER_DATA.copy()

def salvar_dados_usuario(username, user_data):
    res = supabase.table("usuarios").select("password").eq("username", username).execute()
    pw = res.data[0]["password"] if res.data else "123" 
    supabase.table("usuarios").upsert({"username": username, "password": pw, "dados_json": user_data}).execute()

def calcular_nivel(pontos):
    nivel_num = 1
    for nivel, (piso_atual, piso_proximo, nome) in limites.items():
        if pontos >= piso_atual:
            nivel_num = nivel
        else:
            break
    if nivel_num == 4:
        return nivel_num, limites[nivel_num][2], 1.0, 0, 0, None
    piso_atual = limites[nivel_num][0]
    piso_proximo = limites[nivel_num][1]
    pontos_necessarios = piso_proximo - piso_atual
    pontos_feitos = pontos - piso_atual
    progresso_porcentagem = pontos_feitos / pontos_necessarios
    return (nivel_num, limites[nivel_num][2], progresso_porcentagem, pontos_necessarios, pontos_feitos, None)

def resetar_pontuacao():
    st.session_state.user_data["pontos_totais"] = 0
    st.session_state.user_data["historico"] = []
    st.session_state.user_data["quiz_answered_today"] = False
    st.session_state.user_data["quiz_date"] = datetime.date.min.strftime('%Y-%m-%d')
    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    registrar_log(st.session_state.username, "Resetou pontuação")
    st.rerun()

def registrar_pontos_quiz(quiz_do_dia):
    pontos_ganhos = QUIZ_PONTOS
    st.session_state.user_data["pontos_totais"] += pontos_ganhos
    st.session_state.user_data["historico"].append({
        "Ação": "Quiz Sustentável Diário",
        "Pontos": pontos_ganhos,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M:%S")
    })
    st.session_state.user_data["quiz_answered_today"] = True
    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    registrar_log(st.session_state.username, "Respondeu Quiz")
    st.success(f"🎉 Resposta Correta! +{pontos_ganhos} pontos.")

def gerar_quiz_diario():
    last_quiz_date_str = st.session_state.user_data.get("quiz_date", datetime.date.min.strftime('%Y-%m-%d'))
    try:
        last_quiz_date = datetime.datetime.strptime(last_quiz_date_str, '%Y-%m-%d').date()
    except:
        last_quiz_date = datetime.date.min
    hoje = datetime.date.today()
    if hoje > last_quiz_date:
        random.seed(hoje.day + hoje.month + hoje.year)
        st.session_state.user_data["quiz_date"] = hoje.strftime('%Y-%m-%d')
        st.session_state.user_data["quiz_index"] = random.choice(range(len(QUIZ_PERGUNTAS)))
        st.session_state.user_data["quiz_answered_today"] = False
        salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    return QUIZ_PERGUNTAS[st.session_state.user_data.get("quiz_index", 0)]

def registrar_usuario(username, password):
    res = supabase.table("usuarios").select("username").eq("username", username).execute()
    if res.data:
        st.error("Usuário já existe.")
        return False
    supabase.table("usuarios").insert({"username": username, "password": password, "dados_json": DEFAULT_USER_DATA}).execute()
    registrar_log(username, "Novo cadastro")
    st.success(f"Usuário '{username}' criado com sucesso!")
    return True

def login(username, password):
    res = supabase.table("usuarios").select("*").eq("username", username).execute()
    if res.data and res.data[0]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_data = res.data[0]['dados_json']
        registrar_log(username, "Login realizado")
        st.rerun()
    else:
        st.error("Credenciais incorretas.")

def logout():
    registrar_log(st.session_state.username, "Logout realizado")
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def registrar_acao_detalhada(acao, pontos, detalhes=None):
    st.session_state.user_data["pontos_totais"] += pontos
    texto_acao = f"{acao} ({detalhes})" if detalhes else acao
    st.session_state.user_data["historico"].append({
        "Ação": texto_acao,
        "Pontos": pontos,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M:%S")
    })
    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    registrar_log(st.session_state.username, f"Ação: {acao}")
    st.rerun()

def tela_login():
    exibir_logo_centralizado()
    st.markdown("<h3 style='text-align: center;'>🔐 Recompensas Sustentáveis</h3>", unsafe_allow_html=True)
    tab_login, tab_register = st.tabs(["🚪 Entrar", "✨ Criar Conta"])
    with tab_login:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            pw = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                login(user, pw)
    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("Novo Usuário")
            new_pw = st.text_input("Nova Senha", type="password")
            conf_pw = st.text_input("Confirmar Senha", type="password")
            if st.form_submit_button("Criar Conta"):
                if new_pw == conf_pw and new_user:
                    registrar_usuario(new_user, new_pw)

def main_app():
    user_data = st.session_state.user_data
    nivel_num, nome_nivel, progresso, p_nec, p_feito, _ = calcular_nivel(user_data["pontos_totais"])
    
    st.sidebar.title("Opções")
    st.sidebar.button("Logout", on_click=logout)
    if st.sidebar.button("🔴 Zerar Tudo"):
        resetar_pontuacao()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌱 Progresso")
    emoji = MAPA_EMBLEMAS_EMOJI.get(nome_nivel, "✨")
    st.sidebar.markdown(f"**{emoji} Nível:** {nome_nivel}")
    st.sidebar.progress(progresso)
    
    exibir_logo_centralizado()
    st.markdown(f"<h3 style='text-align: center;'>Olá, {st.session_state.username}! 👋</h3>", unsafe_allow_html=True)

    st.subheader("1️⃣ Ações Sustentáveis")
    contribuicoes = st.multiselect("O que você fez hoje?", ["Bike/Pé", "Eletrônicos", "Produtos Sustentáveis"])
    
    if "Bike/Pé" in contribuicoes:
        with st.expander("🚲 Transporte", expanded=True):
            minutos = st.slider("Minutos:", 0, 120, 30, key="slider_transp")
            pontos = minutos // 10
            if st.button(f"Ganhar {pontos} pts"):
                registrar_acao_detalhada("Transporte", pontos, f"{minutos} min")

    if "Eletrônicos" in contribuicoes:
        with st.expander("📱 Descarte", expanded=True):
            tipo = st.selectbox("Item:", ["Celular", "Pilha", "Outros"])
            pts = {"Celular": 40, "Pilha": 15, "Outros": 5}.get(tipo, 5)
            if st.button(f"Ganhar {pts} pts"):
                registrar_acao_detalhada("Descarte", pts, tipo)

    st.markdown("---")
    st.subheader("2️⃣ Quiz Diário")
    pergunta = gerar_quiz_diario()
    if user_data.get("quiz_answered_today"):
        st.info("Quiz concluído por hoje! 🗓️")
    else:
        resp = st.radio(pergunta['pergunta'], pergunta['opcoes'])
        if st.button("Responder"):
            if resp == pergunta['resposta']:
                registrar_pontos_quiz(pergunta)
            else:
                st.error("Incorreto. Tente amanhã!")

    st.markdown("---")
    st.subheader("3️⃣ Mapa de Coleta")
    st.map(PONTOS_COLETA, latitude='lat', longitude='lon', size=15, color='#008000')

    st.markdown("---")
    st.subheader("📊 Seu Histórico")
    if user_data["historico"]:
        st.dataframe(pd.DataFrame(user_data["historico"][::-1]), use_container_width=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if st.session_state.logged_in:
    main_app()
else:
    tela_login()
