import streamlit as st

def mostrar():
    """Página de perfil — placeholder."""
    # Título centralizado da página de Perfil
    st.markdown("<h2 style='text-align: center;'>Perfil</h2>", unsafe_allow_html=True)

    st.write("")  # Espaço visual entre seções

    # Texto informando que a página ainda está em desenvolvimento
    st.markdown("<p style='text-align: center;'>Página em desenvolvimento</p>", unsafe_allow_html=True)

    st.write("")  # Outro pequeno espaço visual

    # Botão para voltar ao início
    if st.button("⬅️ Voltar", use_container_width=True):
        # Atualiza o estado da aplicação para retornar à página inicial
        st.session_state["pagina_atual"] = "inicio"
        # Recarrega a página para aplicar a mudança imediatamente
        st.rerun()
