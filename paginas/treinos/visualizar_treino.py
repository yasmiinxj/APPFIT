import streamlit as st
from repositories.treinos_repository import buscar_treino_por_id
from repositories.exercicios_repository import listar_exercicios_por_treino
from repositories.series_repository import listar_series_por_exercicio

def _entity_to_dict(e):
    if e is None:
        return {}
    if hasattr(e, "__dict__") and not isinstance(e, dict):
        return vars(e)
    return dict(e)

def mostrar():
    treino_id = st.session_state.get("treino_visualizar_id")
    ficha_id = st.session_state.get("ficha_visualizar_id")

    if not treino_id:
        st.error("Nenhum treino selecionado.")
        return

    treino_raw = buscar_treino_por_id(treino_id)
    treino = _entity_to_dict(treino_raw)

    st.title(f"🏋️ Treino: {treino.get('nome')}")
    if treino.get("observacoes"):
        st.caption(treino.get("observacoes"))

    # Voltar para a página de visualização da ficha (biblioteca -> visualizar_ficha)
    if st.button("⬅ Voltar"):
        # garante que a ficha ainda está definida (não deveria perder)
        if ficha_id:
            st.session_state["ficha_visualizar_id"] = ficha_id
        st.session_state["pagina_atual"] = "visualizar_ficha"
        st.rerun()

    st.markdown("---")
    st.subheader("📋 Exercícios")

    exercicios = listar_exercicios_por_treino(treino_id)
    if not exercicios:
        st.info("Nenhum exercício cadastrado neste treino.")
        return

    for ex in exercicios:
        e = _entity_to_dict(ex)

        with st.container():
            st.markdown(
                f"**{e.get('nome')}** — descanso: {e.get('descanso_segundos') or e.get('descanso') or 0}s"
            )
            if e.get("observacoes"):
                st.caption(e.get("observacoes"))

            # --- SÉRIES ---
            series = listar_series_por_exercicio(e.get("id"))

            if series:
                for s in series:
                    # s é tupla → indexação simples
                    serie_id = s[0]
                    numero = s[1]
                    repeticoes = s[2]
                    carga = s[3]

                    st.write(f"• Série {numero}: {repeticoes} repetições — {carga} kg")
            else:
                st.write("_Nenhuma série cadastrada._")
