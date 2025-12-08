import streamlit as st

def mostrar():
    """Tela principal da área de treinos."""
    st.markdown("<h2 style='text-align: left;'>🏋️ Área de Treinos</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: gray;'>Gerencie suas fichas e registre seus treinos realizados.</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Criar/Editar Fichas", use_container_width=True):
            st.session_state["pagina_atual"] = "fichas"
            st.rerun()
    with col2:
        if st.button("📚 Biblioteca de Treinos", use_container_width=True):
            st.session_state["pagina_atual"] = "biblioteca"
            st.rerun()

    st.markdown("---")
    if st.button("⬅️ Voltar", use_container_width=False):
        st.session_state["pagina_atual"] = "inicio"
        st.rerun()
