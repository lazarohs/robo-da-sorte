import streamlit as st
import requests
import pandas as pd
import random

st.set_page_config(page_title="Robô da Sorte", layout="wide")
st.title("🤖 Robô da Sorte")

# --- Funções utilitárias ---

def buscar_resultado(jogo="megasena"):
    """Busca o último resultado do jogo especificado usando a API pública."""
    url = f"https://loteriascaixa-api.herokuapp.com/api/{jogo}/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def gerar_jogo(jogo, dezenas_freq=None):
    """Gera uma combinação aleatória ou com pesos com base na frequência."""
    if jogo == "Mega-Sena":
        total_numeros = 60
        numeros_por_jogo = 6
    elif jogo == "Quina":
        total_numeros = 80
        numeros_por_jogo = 5
    elif jogo == "Lotofácil":
        total_numeros = 25
        numeros_por_jogo = 15
    else:
        return []

    if dezenas_freq:
        pesos = [dezenas_freq.get(str(n).zfill(2), 1) for n in range(1, total_numeros + 1)]
        jogo = random.choices(range(1, total_numeros + 1), weights=pesos, k=numeros_por_jogo)
    else:
        jogo = random.sample(range(1, total_numeros + 1), numeros_por_jogo)
    
    return sorted(jogo)

# --- Interface ---

aba = st.sidebar.radio("Escolha uma opção", ["🔢 Gerar jogos", "📊 Estatísticas", "🎯 Resultados reais"])

jogos_disponiveis = {
    "Mega-Sena": "megasena",
    "Quina": "quina",
    "Lotofácil": "lotofacil"
}
jogo_nome = st.sidebar.selectbox("Jogo:", list(jogos_disponiveis.keys()))
jogo_api = jogos_disponiveis[jogo_nome]

# --- ABA: Gerar Jogos ---
if aba == "🔢 Gerar jogos":
    st.subheader(f"Gerador inteligente de jogos - {jogo_nome}")

    dezenas_freq = {}
    resultado = buscar_resultado(jogo_api)
    numeros = resultado.get("numeros") or resultado.get("listaDezenas") or resultado.get("dezenas") or []

    if isinstance(numeros, str):
        numeros = numeros.split(",")

    for n in numeros:
        dezenas_freq[n.strip()] = dezenas_freq.get(n.strip(), 0) + 1

    qtd = st.slider("Quantos jogos deseja gerar?", 1, 20, 5)
    jogos = [gerar_jogo(jogo_nome, dezenas_freq) for _ in range(qtd)]

    for i, jogo in enumerate(jogos, 1):
        st.write(f"Jogo {i}: {', '.join(str(n).zfill(2) for n in jogo)}")

# --- ABA: Estatísticas ---
elif aba == "📊 Estatísticas":
    st.subheader(f"Frequência de dezenas - {jogo_nome}")

    todos_resultados = []
    for i in range(1, 31):  # Simula 30 concursos com o último resultado
        resultado = buscar_resultado(jogo_api)
        numeros = resultado.get("numeros") or resultado.get("listaDezenas") or resultado.get("dezenas") or []
        if isinstance(numeros, str):
            numeros = numeros.split(",")
        todos_resultados.extend([n.strip() for n in numeros])

    df_freq = pd.Series(todos_resultados).value_counts().sort_index()
    st.bar_chart(df_freq)

# --- ABA: Resultados reais ---
elif aba == "🎯 Resultados reais":
    st.subheader(f"Último resultado da {jogo_nome}")
    dados = buscar_resultado(jogo_api)
    if dados:
        st.write(f"Concurso Nº: {dados.get('concurso')}")
        st.write(f"Data do sorteio: {dados.get('data')}")
        numeros = dados.get("numeros") or dados.get("listaDezenas") or dados.get("dezenas") or []
        if isinstance(numeros, str):
            numeros = numeros.split(",")
        st.success(f"Números sorteados: {', '.join(str(n).strip() for n in numeros)}")
