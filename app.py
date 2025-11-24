import streamlit as st
import datetime
import json
import os
import pandas as pd
import random

# --- CONFIGURAÇÃO DE ESTILO E CSS (FORÇAR TEMA CLARO) ---
st.markdown("""
<style>

    /* Importa fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;900&display=swap');

    /* 1. FUNDO DA TELA INTEIRA */
    [data-testid="stAppViewContainer"] {
        background-color: #F0FFF0 !important; /* Verde Menta Claro */
        color: #000000 !important;
    }
    
    /* 2. BARRA LATERAL */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #e0e0e0;
    }

    /* 3. REMOVE CABEÇALHO PADRÃO */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* 4. TÍTULO GIGANTE */
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
        color: #00A020 !important; /* Verde forte */
        margin-right: 8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }

    .logo-tech {
        font-family: 'Poppins', sans-serif;
        font-size: 80px;
        font-weight: 900;
        color: #111111 !important; /* PRETO moderno */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
    }

    /* 5. CAIXAS DE INFO */
    [data-testid="stNotification"], [data-testid="stInfo"] {
        border-left: 8px solid #008000 !important;
        background-color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* 6. BOTÕES */
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

    /* 7. TEXTOS GERAIS */
    h1, h2, h3, p, li, span, label {
        color: #333333 !important;
    }

</style>
""", unsafe_allow_html=True)


# --- FUNÇÃO AUXILIAR PARA O TÍTULO ---
def exibir_logo_centralizado():
    st.markdown("""
        <div class="main-logo-container">
            <span class="logo-eco">ECO</span>
            <span class="logo-tech">TECH</span>
        </div>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS E VARIÁVEIS FIXAS ---
DATA_FILE = "users_data.json"
DEFAULT_USER_DATA = {
    "pontos_totais": 0,
    "historico": [],
    "quiz_date": datetime.date.min.strftime('%Y-%m-%d'),
    "quiz_answered_today": False,
    "nivel_anterior": "Semente"
}
QUIZ_PONTOS = 25

# --- QUIZ: PERGUNTAS ---
QUIZ_PERGUNTAS = [
    {"pergunta": "Qual é a principal causa do aquecimento global?", "opcoes": ["Aumento da energia solar", "Emissão de gases de efeito estufa", "Erupções vulcânicas"], "resposta": "Emissão de gases de efeito estufa"},
    {"pergunta": "Qual o principal benefício de usar sacolas reutilizáveis?", "opcoes": ["São mais bonitas", "Redução da produção de lixo plástico", "São mais baratas"], "resposta": "Redução da produção de lixo plástico"},
    {"pergunta": "O que significa 'pegada de carbono'?", "opcoes": ["A marca que você deixa ao andar", "O total de gases de efeito estufa emitidos", "A quantidade de árvores plantadas"], "resposta": "O total de gases de efeito estufa emitidos"},
    {"pergunta": "Qual é o destino mais sustentável para óleo de cozinha usado?", "opcoes": ["Descartar no ralo", "Guardar e reciclar em postos de coleta", "Jogar no lixo comum"], "resposta": "Guardar e reciclar em postos de coleta"},
    {"pergunta": "O que a sigla ODS representa?", "opcoes": ["Organização de Descarte Sustentável", "Objetivos de Desenvolvimento Sustentável", "Operações Diárias de Saneamento"], "resposta": "Objetivos de Desenvolvimento Sustentável"},
]

# --- PONTOS DE COLETA (MOCK DATA ATUALIZADO COM ENDEREÇOS E HORÁRIOS) ---
PONTOS_COLETA = pd.DataFrame({
    # Coordenadas mantidas para o st.map
    'lat': [-23.5505, -23.545, -23.560],
    'lon': [-46.6333, -46.640, -46.625],
    'nome': ['Eco Ponto Central', 'Recicla Fácil SP', 'Posto de Óleo'],
    'tipo': ['Eletrônicos/Pilhas', 'Plástico/Papel', 'Óleo de Cozinha'],
    
    # NOVAS COLUNAS DE ENDEREÇO E HORÁRIO
    'rua': ['Av. Paulista', 'R. Augusta', 'Av. Rebouças'],
    'numero': ['1000', '2500', '400'],
    'bairro': ['Bela Vista', 'Cerqueira César', 'Pinheiros'],
    'cep': ['01310-100', '01412-100', '05401-000'],
    'horario': ['Seg-Sex: 9h às 18h', 'Seg-Sáb: 10h às 19h', 'Ter-Sáb: 8h às 17h'],
})

# --- MAPAS DE NÍVEIS E EMOJIS ---
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

# --- FUNÇÕES DE PERSISTÊNCIA ---

def carregar_todos_dados():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"__credentials__": {}}
    try:
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
            if "__credentials__" not in all_data:
                 all_data["__credentials__"] = {}
            return all_data
    except json.JSONDecodeError:
        return {"__credentials__": {}}

def salvar_todos_dados(all_data):
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

def carregar_dados_usuario(username):
    all_users_data = carregar_todos_dados()
    if username not in all_users_data:
        all_users_data[username] = DEFAULT_USER_DATA.copy()
        salvar_todos_dados(all_users_data)
    return all_users_data[username]

def salvar_dados_usuario(username, user_data):
    all_users_data = carregar_todos_dados()
    all_users_data[username] = user_data
    salvar_todos_dados(all_users_data)

# --- FUNÇÕES DE LÓGICA GERAL ---

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
    st.rerun()

def registrar_pontos_quiz(quiz_do_dia):
    pontos_ganhos = QUIZ_PONTOS
    st.session_state.user_data["pontos_totais"] += pontos_ganhos
    registro = {
        "Ação": f"Quiz Sustentável Diário (Acerto)",
        "Pontos": pontos_ganhos,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M:%S")
    }
    st.session_state.user_data["historico"].append(registro)
    st.session_state.user_data["quiz_answered_today"] = True
    salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    st.success(f"🎉 Resposta Correta! Você ganhou {pontos_ganhos} pontos.")

def gerar_quiz_diario():
    # --- INÍCIO DA CORREÇÃO DE SEGURANÇA ---
    # Busca a string de data. Se não existir, define uma string padrão antiga
    last_quiz_date_str = st.session_state.user_data.get("quiz_date", datetime.date.min.strftime('%Y-%m-%d'))
    
    try:
        # Tenta converter a string para data
        last_quiz_date = datetime.datetime.strptime(last_quiz_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # SE DER ERRO (como aconteceu no seu print), reseta para uma data antiga
        # Isso impede que o app quebre
        last_quiz_date = datetime.date.min
    # --- FIM DA CORREÇÃO DE SEGURANÇA ---

    hoje = datetime.date.today()
    if hoje > last_quiz_date:
        random.seed(hoje.day + hoje.month + hoje.year)
        indice_quiz = random.choice(range(len(QUIZ_PERGUNTAS)))
        st.session_state.user_data["quiz_date"] = hoje.strftime('%Y-%m-%d')
        st.session_state.user_data["quiz_index"] = indice_quiz
        st.session_state.user_data["quiz_answered_today"] = False
        salvar_dados_usuario(st.session_state.username, st.session_state.user_data)
    
    return QUIZ_PERGUNTAS[st.session_state.user_data.get("quiz_index", 0)]

# --- AUTENTICAÇÃO E CADASTRO ---

def registrar_usuario(username, password):
    all_data = carregar_todos_dados()
    credentials = all_data.get("__credentials__", {})
    if username in credentials:
        st.error("Usuário já existe. Por favor, escolha outro nome.")
        return False
    credentials[username] = password
    all_data["__credentials__"] = credentials
    all_data[username] = DEFAULT_USER_DATA.copy()
    salvar_todos_dados(all_data)
    st.success(f"🎉 Usuário '{username}' criado com sucesso! Agora você pode fazer login.")
    return True

def login(username, password):
    all_data = carregar_todos_dados()
    credentials = all_data.get("__credentials__", {})
    if username in credentials and credentials[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_data = carregar_dados_usuario(username)
        st.rerun()
    else:
        st.error("Nome de Usuário ou Senha incorretos. Tente novamente ou cadastre-se.")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    if 'last_transport_info' in st.session_state: st.session_state.last_transport_info = None
    if 'last_purchase_info' in st.session_state: st.session_state.last_purchase_info = None
    st.rerun()

def registrar_acao_detalhada(acao, pontos, detalhes=None):
    user_data = st.session_state.user_data
    user_data["pontos_totais"] += pontos
    registro_detalhe = f"{acao}"
    if detalhes:
        registro_detalhe += f" ({detalhes})"
    registro = {
        "Ação": registro_detalhe,
        "Pontos": pontos,
        "Data/Hora": datetime.datetime.now().strftime("%d/%m %H:%M:%S")
    }
    user_data["historico"].append(registro)
    st.success(f"✅ Ação registrada! Você ganhou {pontos} pontos.")
    salvar_dados_usuario(st.session_state.username, user_data)
    st.rerun()

# --- TELA DE LOGIN ---
def tela_login():
    exibir_logo_centralizado() # LOGO GRANDE
    st.markdown("<h3 style='text-align: center;'>🔐 Plataforma de Recompensas Sustentáveis</h3>", unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["🚪 Entrar", "✨ Criar Nova Conta"])

    with tab_login:
        with st.form("login_form"):
            login_username = st.text_input("Nome de Usuário (Login)", key="login_user")
            login_password = st.text_input("Senha (Login)", type="password", key="login_pass")
            submitted = st.form_submit_button("Entrar")
            if submitted:
                if login_username and login_password:
                    login(login_username, login_password)
                else:
                    st.warning("Por favor, preencha o nome de usuário e a senha.")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Nome de Usuário (Cadastro)", key="new_user")
            new_password = st.text_input("Senha (Cadastro)", type="password", key="new_pass")
            confirm_password = st.text_input("Confirmar Senha", type="password", key="confirm_pass")
            submitted = st.form_submit_button("Criar Login")
            if submitted:
                if not new_username or not new_password or not confirm_password:
                    st.warning("Todos os campos de cadastro são obrigatórios.")
                elif new_password != confirm_password:
                    st.error("As senhas não coincidem.")
                else:
                    registrar_usuario(new_username, new_password)

# --- APP PRINCIPAL ---
def main_app():
    if 'last_transport_info' not in st.session_state: st.session_state.last_transport_info = None
    if 'last_purchase_info' not in st.session_state: st.session_state.last_purchase_info = None

    user_data = st.session_state.user_data
    pontos_acumulados = user_data["pontos_totais"]
    historico_usuario = user_data["historico"]
    
    nivel_num, nome_nivel, progresso, pontos_necessarios, pontos_feitos, _ = calcular_nivel(pontos_acumulados)  

    # SIDEBAR
    st.sidebar.title("Opções")
    st.sidebar.button("Logout", on_click=logout)
    if st.sidebar.button("🔴 Zerar Pontuação e Histórico"):
        resetar_pontuacao()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🌱 Progresso & Emblemas")
    emoji_nivel = MAPA_EMBLEMAS_EMOJI.get(nome_nivel, "✨")
    st.sidebar.markdown(f"**{emoji_nivel} Nível Atual:** **{nome_nivel}**")
    st.sidebar.markdown(f"**Pontos:** {pontos_acumulados}")
    st.sidebar.progress(progresso)
    if nome_nivel != "EcoLíder":
        pontos_restantes = pontos_necessarios - pontos_feitos
        st.sidebar.info(f"Faltam {pontos_restantes} pts para o próximo nível!")
    else:
        st.sidebar.success("Parabéns, EcoLíder! 👑")
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Histórico de Emblemas:")
    niveis_completos = list(limites.values())[:nivel_num]
    for nivel_info in niveis_completos:
        nome = nivel_info[2]
        emoji = MAPA_EMBLEMAS_EMOJI.get(nome, "✅")
        st.sidebar.markdown(f"{emoji} {nome} (Alcançado)")

    # CONTEÚDO CENTRAL
    exibir_logo_centralizado() # LOGO GRANDE
    st.markdown(f"<h3 style='text-align: center; margin-top: -20px;'>Olá, {st.session_state.username.capitalize()}! 👋</h3>", unsafe_allow_html=True)
    
    if nome_nivel != user_data.get("nivel_anterior"):
        if user_data.get("nivel_anterior") is not None:
            st.balloons()
            st.success(f"🎉 Parabéns! Você avançou para o nível: **{nome_nivel}**!")
            st.info(f"🎁 Recompensa Liberada: Cupom de 10% de desconto!")
        user_data["nivel_anterior"] = nome_nivel
        salvar_dados_usuario(st.session_state.username, user_data)
        st.rerun()

    st.markdown("---")

    st.subheader("1️⃣ Registre sua Contribuição Detalhada")
    contribuicoes = st.multiselect(
        "Selecione as formas de contribuição ao meio ambiente hoje:",
        ["Transporte Sustentável (Bike/Pé)", "Descarte de Eletrônicos", "Comprar Produtos Sustentáveis"]
    )
    
    if "Transporte Sustentável (Bike/Pé)" in contribuicoes:
        with st.expander("🚲 Registrar Transporte Sustentável", expanded=True):
            if st.session_state.last_transport_info:
                st.info(st.session_state.last_transport_info)
            
            # --- CORREÇÃO: SLIDER FORA DO FORMULÁRIO PARA GARANTIR ATUALIZAÇÃO IMEDIATA ---
            # O valor do slider é lido e atualizado diretamente aqui.
            minutos_slider = st.slider(
                "Quantos minutos você utilizou um transporte sustentável hoje?", 
                0, 120, 30, 
                key="transporte_minutos"
            )
            
            # Cálculo dos pontos baseado no valor atualizado
            pontos = minutos_slider // 10 
            
            # Exibe a pontuação dinâmica
            st.markdown(f"**Pontos a ganhar:** {pontos}")
            
            with st.form("transporte_form", clear_on_submit=True):
                # O widget radio button AINDA PRECISA ESTAR NO FORM
                finalidade = st.radio("Para qual finalidade você usou o transporte sustentável?", ["Trabalho", "Passeio", "Esporte", "Outros"])
                
                # O botão de submissão do formulário
                submitted = st.form_submit_button(f"Registrar e Ganhar {pontos} Pontos")
                
                if submitted:
                    # Usa 'minutos_slider' que já tem o valor correto do último estado
                    current_minutos = st.session_state["transporte_minutos"]
                    
                    co2_evitado = round((current_minutos / 30) * 0.5, 2) 
                    st.session_state.last_transport_info = (f"Cálculo: Você evitou a emissão de **{co2_evitado} kg de CO₂**! Isso é {round(co2_evitado / 1.5 * 100, 1)}% menos poluição do que um carro médio para a mesma distância.")
                    registrar_acao_detalhada("Transporte Sustentável", pontos, f"{current_minutos} min, Finalidade: {finalidade}")
            # --- FIM DA CORREÇÃO ---
    
    if "Descarte de Eletrônicos" in contribuicoes:
        with st.expander("📱 Registrar Descarte de Eletrônicos", expanded=True):
            with st.form("eletronicos_form", clear_on_submit=True):
                eletronico = st.selectbox("Qual tipo de eletrônico foi descartado?", ["Celular", "Teclado/Mouse", "Pilha/Bateria", "Lâmpada LED", "Outros"])
                pontos = {"Celular": 40, "Teclado/Mouse": 25, "Pilha/Bateria": 15, "Lâmpada LED": 10, "Outros": 5}.get(eletronico, 5)
                submitted = st.form_submit_button(f"Registrar e Ganhar {pontos} Pontos")
                if submitted:
                    registrar_acao_detalhada("Descarte de Eletrônico", pontos, f"Tipo: {eletronico}")
    
    if "Comprar Produtos Sustentáveis" in contribuicoes:
        with st.expander("🛒 Registrar Compra Sustentável", expanded=True):
            if st.session_state.last_purchase_info:
                 st.info(st.session_state.last_purchase_info)
            with st.form("compra_form", clear_on_submit=True):
                segmento = st.selectbox("Qual o segmento do produto comprado?", ["Limpeza Ecológica", "Roupas Recicladas", "Cosméticos Naturais", "Alimentos Orgânicos"])
                pontos = 15 
                submitted = st.form_submit_button(f"Registrar e Ganhar {pontos} Pontos")
                if submitted:
                    st.session_state.last_purchase_info = (f"✨ Curiosidade: Produtos de {segmento} geralmente usam até 70% menos água na produção do que os convencionais. Sua escolha faz a diferença!")
                    registrar_acao_detalhada("Compra Sustentável", pontos, f"Segmento: {segmento}")

    st.markdown("---")
    st.subheader("2️⃣ Quiz Sustentável do Dia")
    quiz_do_dia = gerar_quiz_diario()

    if user_data.get("quiz_answered_today"):
        st.info(f"Quiz de hoje respondido! Volte amanhã para ganhar mais {QUIZ_PONTOS} pontos. 🗓️")
    else:
        with st.container(border=True):
            st.markdown(f"**Pergunta:** {quiz_do_dia['pergunta']}")
            with st.form("quiz_form"):
                resposta_usuario = st.radio("Selecione a opção correta:", options=quiz_do_dia['opcoes'])
                submitted = st.form_submit_button("Responder e Ganhar Pontos")
                if submitted:
                    if resposta_usuario == quiz_do_dia['resposta']:
                        registrar_pontos_quiz(quiz_do_dia)
                    else:
                        st.error("Resposta incorreta. Tente novamente amanhã. 😔")

    st.markdown("---")
    st.subheader("3️⃣ Pontos de Coleta Próximos")
    st.write("Consulte os pontos de coleta de materiais recicláveis em sua região (dados de demonstração).")
    
    # Adiciona a pesquisa
    search_term = st.text_input("🔍 Pesquisar por Nome, Tipo, Bairro ou CEP (ex: 'Óleo', 'Pinheiros')", "")

    # Lógica de filtro aprimorada para incluir os novos campos de endereço
    if search_term:
        search_term_lower = search_term.lower()
        df_filtered = PONTOS_COLETA[
            PONTOS_COLETA['nome'].str.lower().str.contains(search_term_lower) |
            PONTOS_COLETA['tipo'].str.lower().str.contains(search_term_lower) |
            PONTOS_COLETA['rua'].str.lower().str.contains(search_term_lower) |
            PONTOS_COLETA['bairro'].str.lower().str.contains(search_term_lower) |
            PONTOS_COLETA['cep'].str.lower().str.contains(search_term_lower) 
        ]
    else:
        df_filtered = PONTOS_COLETA

    # Exibe o mapa
    st.map(df_filtered, latitude='lat', longitude='lon', size=15, color='#008000')

    st.markdown("##### Detalhes dos Pontos Encontrados:")
    
    # Constrói a coluna de endereço completo para exibição
    df_display = df_filtered.copy()
    df_display['Endereço Completo'] = df_display.apply(
        lambda row: f"{row['rua']}, {row['numero']} - {row['bairro']} - CEP: {row['cep']}", axis=1
    )
    
    # Exibe a tabela com as informações completas, sem lat/lon
    st.dataframe(
        df_display[[
            "nome", "tipo", "Endereço Completo", "horario"
        ]].rename(columns={
            "nome": "Nome do Ponto", 
            "tipo": "Tipo de Coleta", 
            "horario": "Horário de Funcionamento"
        }), 
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("📊 Histórico de Ações")
    if historico_usuario:
        df_historico = pd.DataFrame(historico_usuario[::-1]) 
        df_historico.columns = ["Ação Sustentável", "Pontos Ganhos", "Data/Hora"]
        st.dataframe(df_historico, use_container_width=True)
    else:
        st.info("Nenhuma ação registrada ainda. Comece a ganhar seus pontos EcoTech!")

# --- ENTRY POINT ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = None
if 'user_data' not in st.session_state: st.session_state.user_data = None
    
if st.session_state.logged_in:
    main_app()
else:
    tela_login()
