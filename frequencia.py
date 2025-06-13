import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def gerar_grafico_frequencia(jogo):
    if jogo == "Mega-Sena":
        numeros = list(range(1, 61))
        freq_simulada = [abs((i * 17) % 30 - 15) + i % 5 for i in numeros]

        df = pd.DataFrame({
            'Número': numeros,
            'Frequência': freq_simulada
        })

        st.subheader("📊 Frequência dos Números - Mega-Sena")
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(df['Número'], df['Frequência'], color='#1f77b4')
        ax.set_xlabel("Números")
        ax.set_ylabel("Frequência")
        ax.set_title("Números mais sorteados (simulação)")
        st.pyplot(fig)
    else:
        st.warning("Gráfico de frequência ainda não implementado para esse jogo.")
