import streamlit as st

st.set_page_config(page_title="Robô da Sorte", layout="wide")

# --- TÍTULO PRINCIPAL ---
st.markdown("""
    <h1 style='text-align: center; color: #004080;'>🤖 Robô da Sorte</h1>
    <h4 style='text-align: center; color: #666;'>Seu assistente inteligente para apostas nas Loterias Caixa</h4>
    <hr style='border: 1px solid #004080;' />
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.markdown("## 🎯 Escolha o jogo")
jogo = st.sidebar.selectbox(
    "Tipo de Loteria:",
    ["Mega-Sena", "Quina", "Lotofácil", "Lotomania", "Timemania", "Dia de Sorte", "Super Sete"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("## ⚙️ Funcionalidades")
func_selecionada = st.sidebar.radio(
    "O que deseja fazer?",
    [
        "📊 Ver estatísticas (Gráficos de frequência)",
        "🎰 Simular apostas anteriores",
        "🧠 Gerar jogo com IA",
        "📄 Exportar para PDF",
        "📲 Enviar por Telegram"
    ]
)

# --- PAINEL PRINCIPAL ---
st.markdown(f"""
    <div style='padding: 10px; background-color: #f2f2f2; border-radius: 10px;'>
        <h2 style='color: #004080;'>🎮 Jogo selecionado: {jogo}</h2>
        <p style='color: #333;'>Abaixo você poderá explorar dados, gerar apostas inteligentes e muito mais!</p>
    </div>
""", unsafe_allow_html=True)

# Exibir funcionalidade selecionada
st.info(f"Você selecionou a funcionalidade: {func_selecionada}")
