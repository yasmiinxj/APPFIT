import streamlit as st

def mostrar():
    """Tela principal da área de treinos."""
    
    # Título da página com HTML para formatação
    st.markdown("<h2 style='text-align: left;'>🏋️ Área de Treinos</h2>", unsafe_allow_html=True)
    
    # Subtítulo descritivo
    st.markdown("<p style='text-align: left; color: gray;'>Gerencie suas fichas e registre seus treinos realizados.</p>", unsafe_allow_html=True)
    
    st.write("")  # Espaçamento visual

    # Cria duas colunas lado a lado
    col1, col2 = st.columns(2)

    # Botão para ir para a página de criação/edição de fichas
    with col1:
        if st.button("📄 Criar/Editar Fichas", use_container_width=True):
            st.session_state["pagina_atual"] = "fichas"  # Atualiza o estado da página
            st.rerun()  # Recarrega a página para aplicar a mudança

    # Botão para ir para a biblioteca de treinos
    with col2:
        if st.button("📚 Biblioteca de Treinos", use_container_width=True):
            st.session_state["pagina_atual"] = "biblioteca"
            st.rerun()

    st.markdown("---")  # Linha divisória
    
    # Botão para voltar para a página inicial
    if st.button("⬅️ Voltar", use_container_width=False):
        st.session_state["pagina_atual"] = "inicio"
        st.rerun()
