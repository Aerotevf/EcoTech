import streamlit as st
import datetime
import pandas as pd
import random
from supabase import create_client, Client

# ─── CONFIGURAÇÃO DA PÁGINA ───────────────────────────────────────────────────
st.set_page_config(page_title="EcoTech", page_icon="🌿", layout="wide")

# CSS PERSONALIZADO (MÁXIMO CONTRASTE: FUNDO DARK + TEXTO BRANCO/NEON)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700&family=DM+Sans:wght@400;700&display=swap');

/* Fundo Cinza Grafite Profundo */
[data-testid="stAppViewContainer"] {
    background-color: #0a0c0a !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar Verde Escura com Borda Neon */
[data-testid="stSidebar"] {
    background-color: #051405 !important;
    border-right: 2px solid #22c55e;
}

/* Forçar Cor Branca em TODOS os textos e labels */
h1, h2, h3, h4, p, span, label, .stMetric, [data-testid="stMarkdown"] p {
    color: #ffffff !important;
}

.logo-eco {
    font-family: 'Syne', sans-serif !important;
    color: #22c55e !important;
    font-size: 55px;
    font-weight: 800;
    text-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
}

/* Botões com alto destaque (Verde Neon com borda branca) */
.stButton > button {
    background-color: #166534 !important;
    color: #ffffff !important;
    border: 2px solid #ffffff !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: bold !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #22c55e !important;
    border-color: #22c55e !important;
    color: #000000 !important;
}

/* Cards da Home com transparência */
.card-home {
    background-color: rgba(255, 255, 255, 0.07);
    border: 1px solid #22c55e;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 25px;
}

/* Ajuste do Ranking para ler no escuro */
[data-testid="stTable"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
}
th { color: #22c55e !important; font-size: 16px !important; }
td { color: #ffffff !important; font-size: 15px !important; }

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
        data.append({"Emblema": obter_emblema(p), "Usuário": u['username'], "Pontos": p})
    df = pd.DataFrame(data).sort_values("Pontos", ascending=False)
    # Adiciona a posição 1, 2, 3...
    df.insert(0, "Posição", range(1, len(df) + 1))
    return df

# ─── INTERFACE DE ACESSO ───────────────────────────────────────────────────────

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<p class="logo-eco">ECOTECH</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="card-home">
        <h3 style="color:#22c55e !important;">O que é o EcoTech? 🌍</h3>
        <p>Somos uma plataforma que une tecnologia e sustentabilidade para recompensar suas boas ações.</p>
        <p><b>Como funciona:</b></p>
        <ul>
            <li>🚲 <b>Mobilidade:</b> Registre seus trajetos sem motor e ganhe pontos.</li>
            <li>📱 <b>Reciclagem:</b> Descarte eletrônicos e ganhe bônus altos.</li>
            <li>🧠 <b>Educação:</b> Teste seus conhecimentos no Quiz diário.</li>
            <li>🏆 <b>Conquistas:</b> Ganhe emblemas e suba no ranking global.</li>
        </ul>
        <p><i>Transforme o mundo enquanto evolui seu perfil!</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-home">', unsafe_allow_html=True)
        st.subheader("Entrar no Sistema")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("Acessar Conta"):
            res = supabase.table("usuarios").select("*").eq("username", u).eq("password", p).execute()
            if res.data:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.user_data = res.data[0]['dados_json']
                st.rerun()
            else: st.error("Login inválido.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ─── DASHBOARD DO USUÁRIO ───
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.write(f"Sua Patente: **{obter_emblema(st.session_state.user_data['pontos_totais'])}**")
        st.divider()
        # Abas Visíveis como você pediu
        menu = st.radio("MENU PRINCIPAL", ["🏠 Painel de Impacto", "🧠 Quiz Ambiental", "📍 Pontos de Coleta", "🏆 Ranking Global", "🚀 Eco-Jump (Beta)"])
        st.divider()
        if st.button("Sair do Sistema"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "🏠 Painel de Impacto":
        st.title("🌿 Seu Impacto na Natureza")
        pts = st.session_state.user_data['pontos_totais']
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Seus Pontos", f"{pts} pts")
        with c2: st.metric("Carbono Evitado", f"{pts*0.1:.1f} kg")
        with c3: st.metric("Sua Patente", obter_emblema(pts))

        st.markdown("---")
        st.subheader("📝 Registrar Atividade Sustentável")
        
        col_a, col_b = st.columns(2)
        with col_a:
            with st.expander("🚲 Mobilidade Verde (Bike/Pé)"):
                minutos = st.number_input("Quanto tempo durou a atividade? (minutos)", 5, 300, 30)
                if st.button("Salvar Trajeto"):
                    pontos_ganhos = minutos // 10
                    st.session_state.user_data['pontos_totais'] += pontos_ganhos
                    salvar_dados(st.session_state.user_data)
                    st.success(f"Incrível! +{pontos_ganhos} pontos acumulados.")
                    st.rerun()

        with col_b:
            with st.expander("📱 Descarte de Eletrônicos"):
                item = st.selectbox("O que você descartou corretamente?", ["Pilhas/Baterias", "Celular Antigo", "Cabos e Periféricos", "Monitor/TV"])
                if st.button("Confirmar Descarte"):
                    st.session_state.user_data['pontos_totais'] += 50
                    salvar_dados(st.session_state.user_data)
                    st.success("Ação de alto impacto! +50 pontos computados.")
                    st.rerun()

    elif menu == "🧠 Quiz Ambiental":
        st.title("🧠 Desafio de Conhecimento")
        st.write("Responda corretamente para ganhar 20 pontos bônus!")
        perguntas = [
            {"p": "Qual destes materiais demora mais para se decompor?", "o": ["Papel", "Vidro", "Casca de Fruta"], "r": "Vidro"},
            {"p": "Qual a principal fonte de energia renovável no Brasil?", "o": ["Hidrelétrica", "Carvão", "Nuclear"], "r": "Hidrelétrica"}
        ]
        escolha = random.choice(perguntas)
        st.markdown(f"**Pergunta:** {escolha['p']}")
        resp = st.radio("Selecione sua resposta:", escolha['o'])
        if st.button("Enviar Resposta"):
            if resp == escolha['r']:
                st.session_state.user_data['pontos_totais'] += 20
                salvar_dados(st.session_state.user_data)
                st.success("Parabéns, você conhece o planeta! +20 pontos.")
            else: st.error("Não foi desta vez. Estude mais para o próximo!")

    elif menu == "Ranking Global":
        st.title("🏆 Leaderboard Global")
        st.write("Veja quem são os maiores defensores da natureza.")
        df_rank = carregar_ranking()
        # Tabela limpa e alinhada
        st.dataframe(df_rank, use_container_width=True, hide_index=True)

    elif menu == "📍 Pontos de Coleta":
        st.title("📍 Onde descartar?")
        st.write("Encontre os pontos mais próximos de você (Exemplo: Grande São Paulo)")
        # Dados fictícios para o mapa funcionar
        locais = pd.DataFrame({'lat': [-23.5505, -23.545, -23.560], 'lon': [-46.6333, -46.640, -46.625]})
        st.map(locais)

    elif menu == "🚀 Eco-Jump (Beta)":
        st.title("🚀 Eco-Jump")
        st.write("Teste seus reflexos! Cada clique simula um salto sobre a poluição.")
        if st.button("PULAR AGORA! ⬆️"):
            st.session_state.user_data['pontos_totais'] += 1
            salvar_dados(st.session_state.user_data)
            st.toast("Reflexo sustentável! +1 ponto.")
            st.balloons()
