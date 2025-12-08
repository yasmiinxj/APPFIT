import streamlit as st
from repositories.fichas_repository import buscar_ficha_por_id
from repositories.treinos_repository import listar_treinos_por_ficha

def _entity_to_dict(e):
    if e is None:
        return {}
    if hasattr(e, "__dict__") and not isinstance(e, dict):
        return vars(e)
    return dict(e)

def mostrar():
    ficha_id = st.session_state.get("ficha_visualizar_id")

    if not ficha_id:
        st.error("Nenhuma ficha selecionada.")
        return

    ficha_raw = buscar_ficha_por_id(ficha_id)
    ficha = _entity_to_dict(ficha_raw)

    st.title(f"📘 Ficha: {ficha.get('nome')}")
    if ficha.get("observacoes"):
        st.caption(ficha.get("observacoes"))

    # 🔥 VOLTAR → BIBLIOTECA (correção)
    if st.button("⬅ Voltar"):
        st.session_state["pagina_atual"] = "biblioteca"
        st.rerun()

    st.markdown("---")
    st.subheader("🏋️ Treinos da Ficha")

    treinos = listar_treinos_por_ficha(ficha_id)

    if not treinos:
        st.info("Nenhum treino cadastrado nesta ficha.")
        return

    for t in treinos:
        tdict = _entity_to_dict(t)

        with st.container():
            st.write(f"**{tdict.get('nome')}**")
            if tdict.get("observacoes"):
                st.caption(tdict.get("observacoes"))

            if st.button(f"Ver treino: {tdict.get('nome')}", key=f"v_{tdict.get('id')}"):
                st.session_state["treino_visualizar_id"] = tdict.get("id")
                st.session_state["pagina_atual"] = "visualizar_treino"
                st.rerun()
