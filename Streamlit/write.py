import streamlit as st
import pandas as pd

# Exemplo 1
st.write('Write and *Magic*')

#Exemplo 2
st.write(pd.DataFrame({
    'Coluna A': [1, 2,3,4,5],
    'Coluna B': ["Cachorro", "Gato", "Cavalo","Vaca","Zebra"],
}))

st.write(pd.DataFrame({
    'Coluna A': [1, 2,3,4,5],
    'Coluna B': ["Dog", "Cat", "Horse","Cow","Zebra"],
}))

#Exemplo 3
array = [1, 2, "abc", "Martin", True]
st.write(array)

#Exemplo 4
st.write('aqui teremos uma array:', array)

#Exemplo 5
#Colocar exemplo gráfico.