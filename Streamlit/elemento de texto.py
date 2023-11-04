import streamlit as st

# title
st.title('Texto com maior destaque - Título')

# header
st.header('Texto com pouco destaque - Cabeçalho')

# subheader
st.subheader("Texto com pouco destaque - subcabeçalho")

# markdown
"Texto sem nenhuma função"
st.write('Este é um *write*')
st.markdown('Este é um *markdown*')

# caption
st.caption('Texto com fonte pequena usado para descrições e outros detalhamentos')

# code
code = '''if(hungry > 0):
    return "go to refrigerator"
else:
    return "study Streamlit"'''
st.code(code, language='python')

# text
st.text('Texto usando st.text')

# Latex https://katex.org/docs/supported.html
st.latex('\int x²+y²+32ab \isin x²+y²+z²')

