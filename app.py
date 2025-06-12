
# Robô da Sorte – Sistema Inteligente de Previsão de Jogos da Caixa
import pandas as pd
import random
from collections import Counter
import os
import streamlit as st

class JogoCaixa:
    def __init__(self, nome, faixa_numeros, numeros_por_jogo, caminho_csv):
        self.nome = nome
        self.faixa = faixa_numeros
        self.qtd = numeros_por_jogo
        self.dados = pd.read_csv(caminho_csv)

    def analisar_frequencia(self):
        dezenas = self.dados.iloc[:, -self.qtd:].values.flatten()
        return Counter(dezenas)

    def analisar_atraso(self):
        ultimos = self.dados.iloc[-1, -self.qtd:].values.tolist()
        todos_numeros = list(range(self.faixa[0], self.faixa[1] + 1))
        atrasados = [n for n in todos_numeros if n not in ultimos]
        return atrasados

    def gerar_aposta_inteligente(self):
        frequencia = self.analisar_frequencia()
        top_freq = [int(num) for num, _ in frequencia.most_common(30)]
        atraso = self.analisar_atraso()
        candidatos = list(set(top_freq + atraso))
        if len(candidatos) < self.qtd:
            candidatos = list(range(self.faixa[0], self.faixa[1] + 1))
        return sorted(random.sample(candidatos, self.qtd))

# Configuração dos jogos
jogos = {
    "Mega-Sena": {"faixa": (1, 60), "qtd": 6, "csv": "dados/mega_sena.csv"},
    "Quina": {"faixa": (1, 80), "qtd": 5, "csv": "dados/quina.csv"},
    "Lotofácil": {"faixa": (1, 25), "qtd": 15, "csv": "dados/lotofacil.csv"},
    "Lotomania": {"faixa": (0, 99), "qtd": 50, "csv": "dados/lotomania.csv"},
    "Dupla Sena": {"faixa": (1, 50), "qtd": 6, "csv": "dados/dupla_sena.csv"},
}

# Interface com Streamlit
st.set_page_config(page_title="Robô da Sorte", layout="centered")
st.title("🤖 Robô da Sorte")
st.caption("Geração inteligente de apostas para jogos da Caixa")

jogo_escolhido = st.selectbox("Escolha o jogo:", list(jogos.keys()))

if st.button("🎲 Gerar Aposta Inteligente"):
    config = jogos[jogo_escolhido]
    if os.path.exists(config['csv']):
        jogo = JogoCaixa(jogo_escolhido, config["faixa"], config["qtd"], config["csv"])
        aposta = jogo.gerar_aposta_inteligente()
        st.success(f"Aposta sugerida para {jogo_escolhido}: {aposta}")
    else:
        st.error(f"Arquivo CSV não encontrado para {jogo_escolhido} - {config['csv']}")
