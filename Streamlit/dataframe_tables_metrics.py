import pandas as pd
import numpy as np
import streamlit as st

#Dataframe
st.header('DATAFRAME')
"Gerando um dataframe aleatório 5x5"
df = pd.DataFrame(
    np.random.randn(5, 5),
    columns=('col %d' % i for i in range(5)))

st.subheader("Exemplo 1 - imprimindo o Dataframe")
st.dataframe(df)

st.subheader("Exemplo 2 - Alterando as dimensões")
st.dataframe(df, 300, 200)


st.subheader("Exemplo 3 - Dando um destaque nos maiores valores")
st.dataframe(df.style.highlight_max(axis=0))


st.header('TABLE - Similar ao Dataframe, mas o conteúdo de TABLE é estático')
st.subheader("Exemplo 4 - Imprimindo os dados com Table")
st.table(df)

st.header('METRIC - Similar ao Dataframe, mas o conteúdo de TABLE é estático')
st.subheader('Exemplo 5 - Temperatura')
st.metric(label="Temperatura", value="22 °C", delta="1 °C")

st.subheader('Exemplo 6 - Exemplo com 3 colunas')
col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", "25 °C", "2 °C")
col2.metric("Vento", "10 Km/h", "-8%")
col3.metric("Humidade", "86%", "4%")

st.subheader('Exemplo 7 - alterando cor do delta')
st.metric(label="Gas price", value=4, delta=-0.5,
     delta_color="inverse")

st.metric(label="Active developers", value=123, delta=123,
     delta_color="off")