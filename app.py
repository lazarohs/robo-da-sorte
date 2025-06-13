import streamlit as st
from frequencia import gerar_grafico_frequencia
from simulador import simular_apostas

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

# Chamar a funcionalidade correspondente
if func_selecionada == "📊 Ver estatísticas (Gráficos de frequência)":
    gerar_grafico_frequencia(jogo)

elif func_selecionada == "🎰 Simular apostas anteriores":
    st.markdown("### Insira sua aposta (Mega-Sena):")
    aposta_usuario = st.multiselect(
        "Escolha 6 números entre 1 e 60:",
        options=list(range(1, 61)),
        default=[],
        max_selections=6
    )
    if st.button("Simular aposta"):
        if len(aposta_usuario) != 6:
            st.warning("Por favor, escolha exatamente 6 números para a Mega-Sena.")
        else:
            simular_apostas(jogo, aposta_usuario)

else:
    st.warning("Funcionalidade ainda em desenvolvimento. Aguarde as próximas atualizações!")
