import streamlit as st
import pandas as pd
import random

def simular_apostas(jogo, aposta_usuario):
    st.subheader("🎰 Simulador de Apostas")

    if jogo != "Mega-Sena":
        st.warning("Simulação ainda disponível apenas para Mega-Sena.")
        return

    concursos_simulados = []
    for i in range(1, 51):
        concurso = random.sample(range(1, 61), 6)
        concursos_simulados.append(sorted(concurso))

    resultados = []
    for idx, concurso in enumerate(concursos_simulados):
        acertos = len(set(aposta_usuario) & set(concurso))
        resultados.append({
            'Concurso': f'# {idx+1}',
            'Números Sorteados': concurso,
            'Acertos': acertos
        })

    df_resultados = pd.DataFrame(resultados)
    st.write("Aposta realizada:", sorted(aposta_usuario))
    st.dataframe(df_resultados)
