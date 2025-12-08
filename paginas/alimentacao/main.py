import streamlit as st

def mostrar():
    """Página de alimentação — placeholder."""
    st.markdown("<h2 style='text-align: center;'>Alimentação</h2>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p style='text-align: center;'>Página em desenvolvimento</p>", unsafe_allow_html=True)
    st.write("")
    if st.button("⬅️ Voltar", use_container_width=True):
        st.session_state["pagina_atual"] = "inicio"
        st.rerun()
