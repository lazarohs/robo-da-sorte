# Robô da Sorte – IA, Simulador, Gráficos e IA Evolutiva
import pandas as pd
import random
from collections import Counter
import os
import streamlit as st
import matplotlib.pyplot as plt

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

    def simular_acertos(self, aposta):
        resultados = self.dados.iloc[:, -self.qtd:].values.tolist()
        historico = []
        for i, concurso in enumerate(resultados):
            acertos = len(set(aposta) & set(concurso))
            historico.append((i + 1, acertos))
        return historico

# IA Evolutiva
def gerar_aposta_evolutiva(jogo: JogoCaixa, geracoes=30, populacao_inicial=100, elite=10, mutacao=0.2):
    todos_numeros = list(range(jogo.faixa[0], jogo.faixa[1] + 1))

    def gerar_individuo():
        return sorted(random.sample(todos_numeros, jogo.qtd))

    def fitness(individuo):
        resultados = jogo.simular_acertos(individuo)
        return sum(a for _, a in resultados[-30:])  # soma dos acertos nos últimos 30 concursos

    populacao = [gerar_individuo() for _ in range(populacao_inicial)]

    for _ in range(geracoes):
        populacao = sorted(populacao, key=fitness, reverse=True)
        nova_geracao = populacao[:elite]
        while len(nova_geracao) < populacao_inicial:
            pai = random.choice(populacao[:50])
            filho = pai[:]
            if random.random() < mutacao:
                i = random.randint(0, jogo.qtd - 1)
                novo_num = random.choice(todos_numeros)
                while novo_num in filho:
                    novo_num = random.choice(todos_numeros)
                filho[i] = novo_num
                filho = sorted(filho)
            nova_geracao.append(filho)
        populacao = nova_geracao

    melhor = max(populacao, key=fitness)
    return melhor

# Configurações
jogos = {
    "Mega-Sena": {"faixa": (1, 60), "qtd": 6, "csv": "dados/mega_sena.csv"},
    "Quina": {"faixa": (1, 80), "qtd": 5, "csv": "dados/quina.csv"},
    "Lotofácil": {"faixa": (1, 25), "qtd": 15, "csv": "dados/lotofacil.csv"},
    "Lotomania": {"faixa": (0, 99), "qtd": 50, "csv": "dados/lotomania.csv"},
    "Dupla Sena": {"faixa": (1, 50), "qtd": 6, "csv": "dados/dupla_sena.csv"},
}

st.set_page_config(page_title="Robô da Sorte", layout="centered")
st.title("🤖 Robô da Sorte")
st.caption("Geração inteligente • Simulador de acertos • Gráficos • IA Evolutiva")

aba = st.radio("Escolha uma função:", [
    "🎲 Gerar Aposta Inteligente",
    "🎯 Simulador de Acertos",
    "📊 Gráficos de Frequência",
    "🧠 IA Evolutiva"
])

jogo_escolhido = st.selectbox("Escolha o jogo:", list(jogos.keys()))
config = jogos[jogo_escolhido]

if os.path.exists(config["csv"]):
    jogo = JogoCaixa(jogo_escolhido, config["faixa"], config["qtd"], config["csv"])

    if aba == "🎲 Gerar Aposta Inteligente":
        if st.button("Gerar Aposta"):
            aposta = jogo.gerar_aposta_inteligente()
            st.success(f"Aposta sugerida para {jogo_escolhido}: {aposta}")

    elif aba == "🎯 Simulador de Acertos":
        dezenas = st.text_input(f"Digite sua aposta ({config['qtd']} números separados por vírgula):")
        if st.button("Simular Acertos"):
            try:
                numeros = [int(n.strip()) for n in dezenas.split(",")]
                if len(numeros) != config["qtd"]:
                    st.warning(f"Você deve digitar exatamente {config['qtd']} números.")
                else:
                    resultados = jogo.simular_acertos(numeros)
                    acertos_relevantes = [f"Concurso {c}: {a} acertos" for c, a in resultados if a >= config["qtd"] - 2]
                    if acertos_relevantes:
                        st.info("Acertos relevantes encontrados:")
                        for linha in acertos_relevantes:
                            st.write("- " + linha)
                    else:
                        st.error("Nenhum acerto relevante encontrado.")
            except Exception as e:
                st.error("Erro ao processar os números. Verifique o formato.")

    elif aba == "📊 Gráficos de Frequência":
        st.subheader(f"📈 Frequência das Dezenas - {jogo_escolhido}")
        freq = jogo.analisar_frequencia()
        numeros = list(range(config["faixa"][0], config["faixa"][1] + 1))
        contagens = [freq.get(n, 0) for n in numeros]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(numeros, contagens, color="skyblue")
        ax.set_title("Frequência de Dezenas Sorteadas")
        ax.set_xlabel("Dezena")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

    elif aba == "🧠 IA Evolutiva":
        st.subheader("Aposta gerada com IA Evolutiva")
        if st.button("Gerar aposta com IA"):
            aposta = gerar_aposta_evolutiva(jogo)
            st.success(f"Aposta evoluída para {jogo_escolhido}: {aposta}")
else:
    st.error(f"Arquivo CSV não encontrado: {config['csv']}")
