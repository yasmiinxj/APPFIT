import streamlit as st
from repositories.treinos_repository import buscar_treino_por_id
from repositories.exercicios_repository import listar_exercicios_por_treino
from repositories.series_repository import listar_series_por_exercicio

def _entity_to_dict(e):
    # Converte qualquer entidade (objeto ou dict) para dicionário.
    if e is None:
        return {}
    # Se for objeto com __dict__ → converte usando vars()
    if hasattr(e, "__dict__") and not isinstance(e, dict):
        return vars(e)
    # Se já for dict → força conversão
    return dict(e)

def mostrar():
    # Pega o ID do treino e da ficha que está sendo visualizada
    treino_id = st.session_state.get("treino_visualizar_id")
    ficha_id = st.session_state.get("ficha_visualizar_id")

    # Se treino não estiver definido → erro
    if not treino_id:
        st.error("Nenhum treino selecionado.")
        return

    # Busca o treino no banco
    treino_raw = buscar_treino_por_id(treino_id)
    treino = _entity_to_dict(treino_raw)

    # Título do treino
    st.title(f"🏋️ Treino: {treino.get('nome')}")

    # Observações do treino (se houver)
    if treino.get("observacoes"):
        st.caption(treino.get("observacoes"))

    # Botão para voltar à visualização da ficha correspondente
    if st.button("⬅ Voltar"):
        # Reforça ficha_visualizar_id caso não tenha sido perdida
        if ficha_id:
            st.session_state["ficha_visualizar_id"] = ficha_id
        # Volta para a tela de visualizar ficha
        st.session_state["pagina_atual"] = "visualizar_ficha"
        st.rerun()

    st.markdown("---")
    st.subheader("📋 Exercícios")

    # Busca exercícios associados ao treino
    exercicios = listar_exercicios_por_treino(treino_id)

    # Se não houver exercícios → avisa
    if not exercicios:
        st.info("Nenhum exercício cadastrado neste treino.")
        return

    # Loop para exibir cada exercício
    for ex in exercicios:
        e = _entity_to_dict(ex)

        with st.container():
            # Nome do exercício + descanso (pode vir de descanso_segundos ou descanso)
            st.markdown(
                f"**{e.get('nome')}** — descanso: {e.get('descanso_segundos') or e.get('descanso') or 0}s"
            )

            # Observações do exercício (opcional)
            if e.get("observacoes"):
                st.caption(e.get("observacoes"))

            # Busca séries do exercício
            series = listar_series_por_exercicio(e.get("id"))

            # Se houver séries → lista cada uma
            if series:
                for s in series:
                    # Cada série vem como tupla
                    serie_id = s[0]       # ID da série
                    numero = s[1]         # Número da série (ordem)
                    repeticoes = s[2]     # Número de repetições
                    carga = s[3]          # Carga aplicada

                    st.write(f"• Série {numero}: {repeticoes} repetições — {carga} kg")

            # Se não houver séries → mensagem padrão
            else:
                st.write("_Nenhuma série cadastrada._")
