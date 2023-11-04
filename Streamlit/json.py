import streamlit as st

st.json({
     'foo': 'bar',
     'baz': 'boz',
     'stuff': [
         'stuff 1',
         'stuff 2',
         'stuff 3',
         'stuff 5',
     ],
 })

meuObjeto = {
    'banana': 'amarela',
    'limão': 'verde',
    'laranja': 'laranja'
 }

st.json(meuObjeto)