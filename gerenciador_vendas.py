import streamlit as st
import pandas as pd

# Dados iniciais - Produtos (simula um banco de dados)
if "produtos" not in st.session_state:
    st.session_state.produtos = pd.DataFrame(columns=["Produto", "Preço", "Quantidade"])

# Funções auxiliares
def exibir_estoque():
    """Exibe o estoque atual."""
    st.subheader("Estoque Atual")
    if st.session_state.produtos.empty:
        st.write("🔴 O estoque está vazio.")
    else:
        st.write(st.session_state.produtos)

def criar_produto(nome, preco, quantidade):
    """Cria um novo produto."""
    if nome in st.session_state.produtos["Produto"].values:
        st.warning("Produto já existe!")
        return False
    st.session_state.produtos = pd.concat([
        st.session_state.produtos, 
        pd.DataFrame({"Produto": [nome], "Preço": [preco], "Quantidade": [quantidade]})
    ], ignore_index=True)
    st.success(f"Produto '{nome}' adicionado com sucesso!")
    return True

def remover_produto(nome):
    """Remove um produto."""
    if nome not in st.session_state.produtos["Produto"].values:
        st.warning("Produto não encontrado!")
        return False
    st.session_state.produtos = st.session_state.produtos[st.session_state.produtos["Produto"] != nome]
    st.success(f"Produto '{nome}' removido com sucesso!")
    return True

def editar_produto(nome, novo_preco):
    """Edita o preço de um produto."""
    if nome not in st.session_state.produtos["Produto"].values:
        st.warning("Produto não encontrado!")
        return False
    st.session_state.produtos.loc[st.session_state.produtos["Produto"] == nome, "Preço"] = novo_preco
    st.success(f"Preço do produto '{nome}' atualizado para R$ {novo_preco:.2f}!")
    return True

def atualizar_estoque(nome, quantidade):
    """Adiciona ou remove unidades do estoque."""
    if nome not in st.session_state.produtos["Produto"].values:
        st.warning("Produto não encontrado!")
        return False
    st.session_state.produtos.loc[st.session_state.produtos["Produto"] == nome, "Quantidade"] += quantidade
    st.success(f"Estoque do produto '{nome}' atualizado com sucesso!")
    return True

# Menu principal
st.title("Gerenciador de Vendas 🛒")
menu = st.sidebar.radio("Menu", ["Estoque", "Criar/Remover Produto", "Editar Produto", "Gerenciar Estoque"])

# Opções do menu
if menu == "Estoque":
    exibir_estoque()

elif menu == "Criar/Remover Produto":
    st.subheader("Criar ou Remover Produtos")
    escolha = st.radio("Escolha uma ação:", ["Criar Produto", "Remover Produto"])
    
    if escolha == "Criar Produto":
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço do Produto (R$)", min_value=0.01, step=0.01)
        quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1)
        if st.button("Adicionar Produto"):
            criar_produto(nome, preco, quantidade)
    
    elif escolha == "Remover Produto":
        nome = st.selectbox("Selecione o Produto", st.session_state.produtos["Produto"].values if not st.session_state.produtos.empty else [])
        if st.button("Remover Produto"):
            remover_produto(nome)

elif menu == "Editar Produto":
    st.subheader("Editar Produto")
    nome = st.selectbox("Selecione o Produto", st.session_state.produtos["Produto"].values if not st.session_state.produtos.empty else [])
    novo_preco = st.number_input("Novo Preço (R$)", min_value=0.01, step=0.01)
    if st.button("Atualizar Preço"):
        editar_produto(nome, novo_preco)

elif menu == "Gerenciar Estoque":
    st.subheader("Adicionar ou Remover Estoque")
    nome = st.selectbox("Selecione o Produto", st.session_state.produtos["Produto"].values if not st.session_state.produtos.empty else [])
    quantidade = st.number_input("Quantidade a Adicionar/Remover", step=1, format="%d", value=0)
    acao = st.radio("Ação", ["Adicionar", "Remover"])
    if st.button("Atualizar Estoque"):
        if acao == "Adicionar":
            atualizar_estoque(nome, quantidade)
        else:
            if quantidade > st.session_state.produtos.loc[st.session_state.produtos["Produto"] == nome, "Quantidade"].values[0]:
                st.warning("Não é possível remover mais do que o disponível no estoque!")
            else:
                atualizar_estoque(nome, -quantidade)
