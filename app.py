import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Robô da Sorte - API Loteria", layout="centered")
st.title("🎯 Robô da Sorte - Resultados da Loteria (Beta)")

def buscar_resultado(jogo="megasena"):
    url = f"https://loteriascaixa-api.herokuapp.com/api/{jogo}/latest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Erro ao buscar dados da API.")
            return None
    except:
        st.error("Erro de conexão.")
        return None

jogos_disponiveis = {
    "Mega-Sena": "megasena",
    "Quina": "quina",
    "Lotofácil": "lotofacil"
}

jogo_escolhido = st.selectbox("Escolha o jogo:", list(jogos_disponiveis.keys()))
dados = buscar_resultado(jogos_disponiveis[jogo_escolhido])

if dados:
    st.subheader(f"Último resultado da {jogo_escolhido}")
    st.write(f"Concurso Nº: {dados.get('concurso')}")
    st.write(f"Data do sorteio: {dados.get('data')}")

    # Detectar o campo correto com os números sorteados
    numeros = dados.get("numeros") or dados.get("listaDezenas") or dados.get("dezenas") or []
    if isinstance(numeros, str):
        numeros = numeros.split(",")

    st.success(f"Números sorteados: {', '.join(str(n).strip() for n in numeros)}")

    if st.button("Salvar resultado localmente"):
        df = pd.DataFrame([{
            "jogo": jogo_escolhido,
            "concurso": dados.get("concurso"),
            "data": dados.get("data"),
            "numeros": ", ".join(str(n).strip() for n in numeros)
        }])
        df.to_csv(f"{jogos_disponiveis[jogo_escolhido]}_resultados.csv", index=False)
        st.success("Resultado salvo com sucesso!")
