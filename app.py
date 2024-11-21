import streamlit as st
import pandas as pd

# Caminho do arquivo Excel
EXCEL_FILE_PATH = "01 - Dados Municipais da Bahia - Copia.xlsx"


# Função para redefinir o cabeçalho com base na primeira linha com valores de cada coluna
def redefine_header(df):
    new_header = []
    for col in df.columns:
        # Busca o primeiro valor não vazio da coluna
        first_non_empty = df[col].dropna().iloc[0]
        new_header.append(first_non_empty)
    # Redefine o cabeçalho e remove a linha original usada como header
    df.columns = new_header
    return df[1:]  # Remove a linha do "header" antigo


# Título do aplicativo
st.title("Dados Estatísticos da Bahia")

# Carregar o arquivo Excel
try:
    excel_data = pd.ExcelFile(EXCEL_FILE_PATH)
    tabelas = excel_data.sheet_names  # Obter nomes das planilhas

    # Seleção da tabela
    tabela_selecionada = st.selectbox("Selecione uma tabela para visualizar", tabelas)

    # Ler a tabela selecionada
    df = pd.read_excel(excel_data, sheet_name=tabela_selecionada)

    # Redefinir o cabeçalho
    df = redefine_header(df)

    st.write(f"### {tabela_selecionada}")
    st.dataframe(df)

    # Filtros dinâmicos
    st.sidebar.header("Filtros")
    colunas = st.sidebar.multiselect("Selecione as colunas para exibir", options=df.columns)

    if colunas:
        st.write("### Dados Filtrados")
        st.dataframe(df[colunas])
    else:
        st.write("Selecione colunas no menu lateral para aplicar filtros.")
except FileNotFoundError:
    st.error(f"O arquivo `{EXCEL_FILE_PATH}` não foi encontrado. Verifique o caminho e tente novamente.")
