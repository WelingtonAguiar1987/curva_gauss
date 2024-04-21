import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm
import plotly.graph_objs as go


# DICIONÁRIO DOS ATIVOS FUTUROS OPERADOS:

futuros = {
    'MICRO NASDAQ': {'sigla': 'MNQ=F', 'tick': 0.25, 'valor tick': 0.50},
    'MINI NASDAQ': {'sigla': 'NQ=F', 'tick': 0.25, 'valor tick': 5.00},
    'MICRO S&P500': {'sigla': 'MES=F', 'tick': 0.25, 'valor tick': 1.25},
    'MINI S&P500': {'sigla': 'ES=F', 'tick': 0.25, 'valor tick': 12.50},
    'MICRO DOW JONES': {'sigla': 'MYM=F', 'tick': 1.00, 'valor tick': 0.50},
    'MINI DOW JONES': {'sigla': 'YM=F', 'tick': 1.00, 'valor tick': 5.00},   
    'MICRO RUSSELL2000': {'sigla': 'M2K=F', 'tick': 0.10, 'valor tick': 0.50},
    'MINI RUSSELL2000': {'sigla': 'RTY=F', 'tick': 0.10, 'valor tick': 5.00},  
    'MICRO OURO': {'sigla': 'MGC=F', 'tick': 0.10, 'valor tick': 1.00},
    'MINI OURO': {'sigla': 'GC=F', 'tick': 0.10, 'valor tick': 10.00},
    'MICRO PETRÓLEO WTI': {'sigla': 'MCL=F', 'tick': 0.01, 'valor tick': 100.00}
  
}

def lista_ativos():
    ativos = st.selectbox('Selecione o Ativo: ', options=futuros)
    return ativos


st.set_page_config(page_title='CURVA DE GAUSS', page_icon=':chart_with_upwards_trend:', layout='wide')

# Define o título da aplicação web
st.title('Análise Interativa da Curva de Gauss do Nasdaq Futuros')


# Inputs para seleção das datas
with st.sidebar:
    st.header('Curva de Gauss', divider='rainbow')
    st.image('gauss.JPEG')
    st.write(lista_ativos())
    start_date = st.date_input('Selecione a data inicial:', value=pd.to_datetime('2023-03-17'), format='DD/MM/YYYY')
    end_date = st.date_input('Selecione a data final:', value=pd.to_datetime('2024-06-21'), format='DD/MM/YYYY')
    

# Função para carregar os dados do Yahoo Finance
def load_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Carrega os dados do MNQ=F
data = load_data('MNQ=F')
data_selecao = data.iloc[0:-1]

# Verifica se há dados para processar
if not data.empty:
    # Calcula a média e o desvio padrão dos preços de fechamento ajustados
    mu = data_selecao['Adj Close'].mean()
    sigma = data_selecao['Adj Close'].std()
    last_price = data['Adj Close'][-1]
    preco_ultimo_fechamento = data_selecao['Adj Close'][-1]
    
    # Calcula a mediana dos preços de fechamento ajustados
    median = data_selecao['Adj Close'].median()
    
    # Cria um intervalo de preços com base na média e desvio padrão
    prices = np.linspace(data_selecao['Adj Close'].min(), data_selecao['Adj Close'].max(), 100)
    
    # Ajusta a curva de Gauss aos preços do ativo
    density = norm.pdf(prices, mu, sigma)
    
    # Cria o gráfico interativo com Plotly
    fig = go.Figure()

    # Adiciona a curva de Gauss
    fig.add_trace(go.Scatter(x=density, y=prices, mode='lines', name='Curva de Gauss', line_color="#00FFFF"))

    # Adiciona linhas para a média, desvios padrões e último preço
    fig.add_hline(y=mu, line=dict(color='red', width=2, dash='dash'), name='Média')
    fig.add_hline(y=mu + sigma, line=dict(color='green', width=2, dash='dot'), name='+1 Desvio Padrão')
    fig.add_hline(y=mu - sigma, line=dict(color='blue', width=2, dash='dot'), name='-1 Desvio Padrão')
    fig.add_hline(y=mu + 2*sigma, line=dict(color='green', width=2, dash='dashdot'), name='+2 Desvios Padrões')
    fig.add_hline(y=mu - 2*sigma, line=dict(color='blue', width=2, dash='dashdot'), name='-2 Desvios Padrões')
    fig.add_hline(y=last_price, line=dict(color='purple', width=2, dash='dot'), name='Último Preço')
    
    # Adiciona a linha da mediana ao gráfico
    fig.add_hline(y=median, line=dict(color='orange', width=2, dash='dash'), name='Mediana')

    # Adiciona anotações para média, desvios padrões, último preço e mediana
    fig.add_annotation(xref="paper", x=0.05, y=mu,
                       text=f"Média: {mu:.2f}", showarrow=False, bgcolor="red")
    fig.add_annotation(xref="paper", x=0.05, y=mu + sigma,
                       text=f"+1 Desvio Padrão: {mu + sigma:.2f}", showarrow=False, bgcolor="green")
    fig.add_annotation(xref="paper", x=0.05, y=mu - sigma,
                       text=f"-1 Desvio Padrão: {mu - sigma:.2f}", showarrow=False, bgcolor="blue")
    fig.add_annotation(xref="paper", x=0.05, y=mu + 2*sigma,
                       text=f"+2 Desvios Padrões: {mu + 2*sigma:.2f}", showarrow=False, bgcolor="green")
    fig.add_annotation(xref="paper", x=0.05, y=mu - 2*sigma,
                       text=f"-2 Desvios Padrões: {mu - 2*sigma:.2f}", showarrow=False, bgcolor="blue")
    fig.add_annotation(xref="paper", x=0.95, y=last_price,
                       text=f"Último Preço: {last_price:.2f}", showarrow=False, bgcolor="purple", font=dict(color="white"))
    fig.add_annotation(xref="paper", x=0.95, y=median,
                       text=f"Mediana: {median:.2f}", showarrow=False, bgcolor="orange", font=dict(color="white"))

    # Configurações adicionais do layout
    fig.update_layout(title='Curva de Gauss dos Preços de Fechamento Ajustados', template='plotly_dark',
                      title_x=0.35, title_font_color="#00FFFF", title_font_family="Times New Roman", title_font_size=22,
                      xaxis_title='Densidade de Probabilidade', 
                      yaxis_title='Preço de Fechamento Ajustado',
                      margin=dict(l=0, r=0, t=30, b=0), height=720, width=1080)
    fig.update_xaxes(title_font_family="Times New Roman", title_font_color="#00FF00", title_font_size=18)
    fig.update_yaxes(title_font_family="Times New Roman", title_font_color="#00FF00", title_font_size=18)
    
    
    # Adicionando linha e anotação de texto acima da linha do último fechamento:
    fig.add_hline(preco_ultimo_fechamento, line=dict(color='blue', width=2, dash='dash'), name=f'Último Fechamento: {preco_ultimo_fechamento:.2f}')
    descricao_ultimo_fechamento = (f'Fech. Anterior: {preco_ultimo_fechamento:.2f}')
    fig.add_annotation(xref='paper', x=0.95, y=preco_ultimo_fechamento,
                text=descricao_ultimo_fechamento,
                showarrow=False,
                font=dict(family="Courier New, monospace",
                            size=12,
                            color="blue"),
                align="right",
                yshift=10)  # Ajuste vertical da anotação para não sobrepor a linha

    # Mostra o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Nenhum dado disponível para o período selecionado. Por favor, selecione outro intervalo de datas.")

# Adicionando uma tabela no dashboard:    
st.subheader('Tabela de dados para a Curva de Gauss:')
st.dataframe(data)
st.dataframe(data)
    
with st.sidebar:
    st.write(f'Distância entre Desvios Padrões: :blue[{sigma:.2f}]')
    st.write(f'Média: :red[{mu:.2f}]')
    st.write(f'Mediana: :orange[{median:.2f}]')
    

