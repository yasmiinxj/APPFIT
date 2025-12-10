import streamlit as st

def mostrar():
    """Página de alimentação — placeholder."""
    # Título centralizado da página
    st.markdown("<h2 style='text-align: center;'>Alimentação</h2>", unsafe_allow_html=True)

    st.write("")  # Espaço visual

    # Texto indicando que a página ainda está em desenvolvimento
    st.markdown("<p style='text-align: center;'>Página em desenvolvimento</p>", unsafe_allow_html=True)

    st.write("")  # Outro espaço visual

    # Botão para voltar para a página inicial
    if st.button("⬅️ Voltar", use_container_width=True):
        # Muda o estado da página atual para "inicio"
        st.session_state["pagina_atual"] = "inicio"
        # Recarrega a página para aplicar a mudança
        st.rerun()
