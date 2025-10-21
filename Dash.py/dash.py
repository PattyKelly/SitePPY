import json
import pandas as pd
import streamlit as st

# Caminho para o arquivo JSON
caminho_arquivo = r"C:\Users\Patty\Desktop\PY\Dash.py\bquxjob_3eb8e4a7_192b7276695.json"

# Carregar o JSON e converter para DataFrame
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

df = pd.DataFrame(dados)

# Exibir o DataFrame no Streamlit
st.title("Visualização de Transações")
st.dataframe(df)

# Calcular e exibir o total das transações
if 'valor_transacao' in df.columns:
    df['valor_transacao'] = pd.to_numeric(df['valor_transacao'], errors='coerce')
    total_transacoes = df['valor_transacao'].sum()
    st.write(f"Valor total das transações: R$ {total_transacoes:,.2f}")
