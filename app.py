import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

# Page head
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📈",
    layout="wide"
)

# Data load
df = pd.read_csv("data/processed/data_processed.csv")
print(df.columns.tolist())

# Sidebar
st.sidebar.header("🗂️ Filtros")

# Year Filter
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Seniority Filter
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Position Filter
cargos_disponiveis = sorted(df['cargo'].unique())
cargos_selecionados = st.sidebar.multiselect("Cargo", cargos_disponiveis, default=cargos_disponiveis)

# Employment Filter
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Company Size Filter
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# > DataFrame Filtering
# main dataframe is filtered based on the selections made in the sidebar
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['cargo'].isin(cargos_selecionados)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# >> Main Content <<
st.title("📊 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Análise os dados salariais na área de dados nos últimos anos.")

# >> Key Metrics <<
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['salario_usd'].mean()
    salario_maximo = df_filtrado['salario_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# >> Visual Analysis with Plotly <<
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['salario_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'salario_usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'salario_usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None
    
with col_graf4:
    if not df_filtrado.empty:
        df_cargo = 'Data Scientist'
        if len(cargos_selecionados) == 1:
            df_cargo = cargos_selecionados[0]
        df_ds = df_filtrado[df_filtrado['cargo'] == df_cargo]
        media_ds_pais = df_ds.groupby('residencia_iso3')['salario_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='salario_usd',
            color_continuous_scale='rdylgn',
            title=f'Salário médio de {df_cargo} por país',
            labels={'salario_usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

# >> Detailed Data Table <<
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)

