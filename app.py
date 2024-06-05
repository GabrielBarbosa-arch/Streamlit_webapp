import streamlit as st
import pandas as pd
import plotly.express as px

try:
    import plotly.express as px
    print("Plotly is installed.")
except ImportError:
    print("Plotly is not installed.")


# Função para carregar dados do arquivo Excel
@st.cache_data  # Decoração para maior desempenho de carregamento
def load_data(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

# Caminho para o arquivo Excel
file_path = "Etc_fo.xlsm"

# Carregar os dados
df = load_data(file_path)

# Barra de seleção no tipo
with st.sidebar:
    st.header("Seleção de Filtro_TIPO")
    if 'TIPO' in df.columns:
        unique_values = df['TIPO'].unique()
        selected_value = st.selectbox('Selecione O TIPO:', unique_values)
        
        # Filtrar o DataFrame com base na seleção
        filtered_df = df[df['TIPO'] == selected_value]
    else:
        filtered_df = df
        st.write("A coluna 'TIPO' não foi encontrada no DataFrame.")


# Usando colunas para ocupar 100% do espaço do layout abaixo do filtro
tab1,tab2,tab3= st.tabs(["TABELA","GRÁFICO","TODOS"])
with tab1:
    st.header("Tabela Filtrada")
    st.dataframe(filtered_df, use_container_width=True)
  

with tab2:
    st.header("Gráfico")
    if 'COR' in filtered_df.columns and 'METRAGEM' in filtered_df.columns:
        fig = px.bar(filtered_df ,x='COR', y='METRAGEM', title='Grafico por filtro')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("As colunas 'COR' e 'METRAGEM' não foram encontradas no DataFrame.")
    
with tab3:
    st.header("Visão Geral")
    # Recarregar o DataFrame original
    df_original = load_data(file_path)
    fig_2 = px.bar(df_original, x='COR', y='METRAGEM', title="Visão Geral")
    st.plotly_chart(fig_2, use_container_width=True)
