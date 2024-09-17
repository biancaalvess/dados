import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Carregar os dados
def load_data(file_path):
    """
    Carregar o arquivo CSV contendo dados de comércio exterior.
    """
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'])
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_path} não existe.")
        return None

# Pré-processar os dados
def preprocess_data(df):
    """
    Pré-processar os dados definindo a data como índice e ordenando.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    return df

# Calcular o saldo comercial
def calculate_trade_balance(df):
    """
    Calcular o saldo comercial (Exportações - Importações).
    """
    df['TradeBalance'] = df['Exports'] - df['Imports']
    return df

# Analisar os principais parceiros comerciais
def analyze_top_partners(df, n=5):
    """
    Identificar os principais n parceiros comerciais com base no volume total de comércio.
    """
    df['TotalTrade'] = df['Exports'] + df['Imports']
    top_partners = df.groupby('Country')['TotalTrade'].sum().sort_values(ascending=False).head(n)
    return top_partners

# Visualizar tendências de comércio
def visualize_trade_trends(df):
    """
    Criar um gráfico de linha mostrando as tendências de exportação e importação ao longo do tempo.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Exports'], label='Exportações')
    plt.plot(df.index, df['Imports'], label='Importações')
    plt.title('Tendências de Exportação e Importação')
    plt.xlabel('Data')
    plt.ylabel('Valor (em milhões)')
    plt.legend()
    plt.grid(True)
    plt.savefig('trade_trends.png')
    plt.close()

# Visualizar o saldo comercial
def visualize_trade_balance(df):
    """
    Criar um gráfico de barras mostrando o saldo comercial ao longo do tempo.
    """
    plt.figure(figsize=(12, 6))
    df['TradeBalance'].plot(kind='bar')
    plt.title('Saldo Comercial ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Saldo Comercial (em milhões)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('trade_balance.png')
    plt.close()

# Analisar padrões sazonais
def analyze_seasonal_patterns(df):
    """
    Analisar padrões sazonais nos dados de comércio.
    """
    df['Month'] = df.index.month
    monthly_avg = df.groupby('Month')[['Exports', 'Imports']].mean()
    return monthly_avg

# Função principal de análise
def analyze_trade_data(file_path):
    """
    Realizar uma análise abrangente dos dados de comércio.
    """
    # Carregar e pré-processar dados
    df = load_data(file_path)
    if df is None:
        return
    
    df = preprocess_data(df)
    
    # Calcular saldo comercial
    df = calculate_trade_balance(df)
    
    # Analisar principais parceiros comerciais
    top_partners = analyze_top_partners(df)
    print("Principais 5 Parceiros Comerciais:")
    print(top_partners)
    
    # Visualizar tendências de comércio
    visualize_trade_trends(df)
    
    # Visualizar saldo comercial
    visualize_trade_balance(df)
    
    # Analisar padrões sazonais
    seasonal_patterns = analyze_seasonal_patterns(df)
    print("\nPadrões Sazonais (Médias Mensais):")
    print(seasonal_patterns)
    
    # Calcular crescimento ano a ano
    yearly_growth = df.resample('Y')[['Exports', 'Imports']].sum().pct_change() * 100
    print("\nCrescimento Ano a Ano:")
    print(yearly_growth)
    
    # Identificar produtos com maior valor comercial
    if 'Product' in df.columns:
        df['TotalTrade'] = df['Exports'] + df['Imports']
        top_products = df.groupby('Product')['TotalTrade'].sum().sort_values(ascending=False).head(10)
        print("\nTop 10 Produtos por Valor Comercial:")
        print(top_products)
    else:
        print("\nColuna 'Product' não encontrada nos dados.")

if __name__ == "__main__":
    file_path = "trade_data.csv"  # Substitua pelo caminho real do seu arquivo
    analyze_trade_data(file_path)
