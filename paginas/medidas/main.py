import streamlit as st

def mostrar():
    """Página de medidas — placeholder."""
    # Título centralizado da página
    st.markdown("<h2 style='text-align: center;'>Medições</h2>", unsafe_allow_html=True)

    st.write("")  # Espaço visual para separar os elementos

    # Texto indicando que a funcionalidade ainda está em desenvolvimento
    st.markdown("<p style='text-align: center;'>Página em desenvolvimento</p>", unsafe_allow_html=True)

    st.write("")  # Mais um espaço visual

    # Botão para voltar à página inicial
    if st.button("⬅️ Voltar", use_container_width=True):
        # Define a página atual como "inicio"
        st.session_state["pagina_atual"] = "inicio"
        # Força recarregamento da página para refletir a mudança
        st.rerun()
