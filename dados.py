import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Nome do arquivo CSV contendo os dados
csv_file = 'dados.csv'

# Utilizando o Pandas para ler o arquivo CSV e criar um DataFrame (tabela)
tabela = pd.read_csv(csv_file)


def load_data(file_path):
    return pd.read_csv(file_path)


def plot_capital_count(data):
    st.write("Este gráfico mostra a contagem de empresas com base no tipo de capital. Isso é importante para entender a distribuição dos tipos de capital entre as empresas.")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.countplot(x='Capital', hue='Capital', data=data,
                  palette='viridis', legend=False)
    plt.title('Contagem de Capital')
    plt.xlabel('Tipo de Capital')
    plt.ylabel('Quantidade')
    return fig


def plot_size_distribution(data):
    st.write("Este gráfico em pizza mostra a distribuição das empresas com base no tamanho. É útil para entender como as empresas estão distribuídas em diferentes categorias de tamanho.")
    fig, ax = plt.subplots(figsize=(10, 10))
    size_counts = data['Tamanho'].value_counts()
    plt.pie(size_counts, labels=size_counts.index,
            autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Distribuição de Empresas por Tamanho')
    return fig


def plot_combination(data):
    st.write("Este gráfico de barras agrupadas mostra a combinação de capital e tamanho das empresas. Ajuda a identificar padrões e relações entre essas variáveis.")
    fig, ax = plt.subplots(figsize=(14, 10))
    ax = sns.countplot(x='Capital', hue='Tamanho',
                       data=data, palette='viridis')
    plt.legend(title='Tamanho', loc='upper right',
               labels=['Pequeno', 'Médio', 'Grande'])
    plt.xticks(rotation=45)

    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2.,
                height + 0.1, height, ha='center')

    plt.title('Combinação de Capital e Tamanho')
    plt.xlabel('Tipo de Capital')
    plt.ylabel('Quantidade')
    return fig


def plot_capital_distribution(data):
    st.write("Estes gráficos de pizza mostram a distribuição de empresas com ativo permanente maior ou menor que 100.000. Isso pode ser útil para identificar diferenças nas características das empresas com base nos ativos permanentes.")
    ativo_permanente_maior = data[data['Ativo Permanente'] > 100000]
    ativo_permanente_menor = data[data['Ativo Permanente'] < 100000]

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    # Gráfico de pizza para ativo permanente maior que 100000
    axes[0].pie(ativo_permanente_maior['Capital'].value_counts(
    ), labels=ativo_permanente_maior['Capital'].value_counts().index, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('Ativo Permanente > 100000')

    # Gráfico de pizza para ativo permanente menor que 100000
    axes[1].pie(ativo_permanente_menor['Capital'].value_counts(
    ), labels=ativo_permanente_menor['Capital'].value_counts().index, autopct='%1.1f%%', startangle=90)
    axes[1].set_title('Ativo Permanente < 100000')

    return fig


def main():
    st.title('Análise de Empresas')

    # Criando páginas
    pages = {
        "Página Inicial": "Bem-vindo ao Dashboard de Análise de Empresas. Este dashboard fornece insights sobre empresas, incluindo a contagem de capital, distribuição por tamanho e combinação de capital e tamanho.",
        "Contagem de Capital": plot_capital_count,
        "Distribuição de Empresas por Tamanho": plot_size_distribution,
        "Combinação de Capital e Tamanho": plot_combination,
        "Maior e Menor do que 100.000": plot_capital_distribution
    }

    # Selecionando a página
    selected_page = st.sidebar.radio("Selecione uma opção", list(pages.keys()))

    # Exibindo a página inicial
    if selected_page == "Página Inicial":
        st.subheader(selected_page)
        st.write(pages[selected_page])

    else:
        # Exibindo a página selecionada
        st.subheader(selected_page)
        selected_function = pages[selected_page]
        if callable(selected_function):
            fig = selected_function(tabela)
            st.pyplot(fig)


# Chamando a função principal
if __name__ == "__main__":
    main()
