import streamlit as st
from paginas.alimentacao.main import mostrar as pagina_alimentacao
from paginas.treinos.main import mostrar as pagina_treinos
from paginas.medidas.main import mostrar as pagina_medidas
from paginas.perfil.main import mostrar as pagina_perfil
from paginas.treinos.fichas import mostrar as pagina_fichas
from paginas.treinos.biblioteca import mostrar as pagina_biblioteca
from paginas.treinos.editar_fichas import mostrar as pagina_editar_fichas
from paginas.treinos.editar_treino import mostrar as pagina_editar_treino
from paginas.treinos.visualizar_ficha import mostrar as pagina_visualizar_ficha
from paginas.treinos.visualizar_treino import mostrar as pagina_visualizar_treino

# Configuração inicial da interface do Streamlit.
# Define título da aba e layout centralizado.
st.set_page_config(page_title="Plataforma de Rotina Fitness", layout="centered")

# Controle de estado da aplicação.
# 'pagina_atual' funciona como estrutura de dados simples (chave/valor)
# para manter qual página deve ser exibida.
if "pagina_atual" not in st.session_state:
    st.session_state["pagina_atual"] = "inicio"

# Função responsável pela navegação entre páginas.
# Atualiza o estado e força a interface a recarregar.
def ir_para(pagina: str):
    """Atualiza a página atual e recarrega a interface."""
    st.session_state["pagina_atual"] = pagina  # guarda a página escolhida
    st.rerun()  # força Streamlit a atualizar a tela

# Página inicial da plataforma.
# Contém apenas interface e botões de navegação, sem lógica de negócio.
def pagina_inicio():
    """Página principal da plataforma."""
    st.markdown("<h1 style='text-align: center;'>Plataforma de Rotina Fitness</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Sua jornada de evolução começa aqui!</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Gerencie sua alimentação, treinos e medições corporais em um só lugar.</p>", unsafe_allow_html=True)

    # Botão de perfil posicionado no canto direito superior.
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("👤", key="btn_perfil"):
            ir_para("perfil")  # navegação usando estado

    st.markdown("---")

    # Botões principais de acesso às áreas do sistema.
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🍎 Alimentação", use_container_width=True):
            ir_para("alimentacao")
    with col_b:
        if st.button("🏋️ Treinos", use_container_width=True):
            ir_para("treinos")
    with col_c:
        if st.button("📏 Medidas", use_container_width=True):
            ir_para("medidas")

# Roteamento baseado no valor da chave 'pagina_atual' dentro do estado.
# Cada página é um módulo independente → modularização do sistema.
pagina = st.session_state["pagina_atual"]

if pagina == "inicio":
    pagina_inicio()
elif pagina == "alimentacao":
    pagina_alimentacao()
elif pagina == "treinos":
    pagina_treinos()
elif pagina == "medidas":
    pagina_medidas()
elif pagina == "perfil":
    pagina_perfil()
elif pagina == "fichas":
    pagina_fichas()
elif pagina == "biblioteca":
    pagina_biblioteca()
elif pagina == "editar_fichas":
    pagina_editar_fichas()
elif pagina == "editar_treino":
    pagina_editar_treino()
elif pagina == "visualizar_ficha":
    pagina_visualizar_ficha()
elif pagina == "visualizar_treino":
    pagina_visualizar_treino()
