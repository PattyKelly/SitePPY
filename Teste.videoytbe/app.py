import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Carrega o dataset
df = pd.read_csv("pizzas.csv")

# Cria o modelo
modelo = LinearRegression()
x = df[["diametro"]]
y = df["preco"]  # Mantém como série para facilitar

modelo.fit(x, y)

# Interface com o usuário
st.title("Prevendo o valor de uma pizza")
st.divider()

# Input do usuário
diametro = st.number_input("Digite o tamanho do diâmetro da pizza:", min_value=0.0, step=0.1)

if diametro:
    # Corrigindo o formato de entrada para previsão
    entrada = pd.DataFrame({"diametro": [diametro]})
    preco_previsto = modelo.predict(entrada)[0]  # Acessa o primeiro elemento corretamente
    
    st.write(f"O valor da pizza com {diametro:.2f} cm é de R$ {preco_previsto:.2f}.")
