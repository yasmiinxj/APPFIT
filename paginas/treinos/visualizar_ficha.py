import streamlit as st
from repositories.fichas_repository import buscar_ficha_por_id
from repositories.treinos_repository import listar_treinos_por_ficha

def _entity_to_dict(e):
    # Converte um objeto para dicionário.
    # Se for None → retorna dicionário vazio
    if e is None:
        return {}
    # Se objeto tiver __dict__ e não for um dict → retorna vars(e)
    if hasattr(e, "__dict__") and not isinstance(e, dict):
        return vars(e)
    # Caso já seja dict → força conversão para garantir compatibilidade
    return dict(e)

def mostrar():
    # Pega o ID da ficha salva no estado da sessão
    ficha_id = st.session_state.get("ficha_visualizar_id")

    # Se não houver ficha selecionada → mostra erro e para a execução
    if not ficha_id:
        st.error("Nenhuma ficha selecionada.")
        return

    # Busca a ficha no banco e converte para dict
    ficha_raw = buscar_ficha_por_id(ficha_id)
    ficha = _entity_to_dict(ficha_raw)

    # Título da página com nome da ficha
    st.title(f"📘 Ficha: {ficha.get('nome')}")
    
    # Exibe observações da ficha (se existirem)
    if ficha.get("observacoes"):
        st.caption(ficha.get("observacoes"))

    # Botão de voltar → envia usuário de volta para a biblioteca
    if st.button("⬅ Voltar"):
        st.session_state["pagina_atual"] = "biblioteca"
        st.rerun()

    st.markdown("---")
    st.subheader("🏋️ Treinos da Ficha")

    # Lista treinos associados à ficha
    treinos = listar_treinos_por_ficha(ficha_id)

    # Se não houver treinos → informa e encerra
    if not treinos:
        st.info("Nenhum treino cadastrado nesta ficha.")
        return

    # Loop para exibir cada treino
    for t in treinos:
        tdict = _entity_to_dict(t)  # Converte treino para dict

        with st.container():
            # Nome do treino
            st.write(f"**{tdict.get('nome')}**")

            # Observações do treino (opcional)
            if tdict.get("observacoes"):
                st.caption(tdict.get("observacoes"))

            # Botão para visualizar treino específico
            if st.button(f"Ver treino: {tdict.get('nome')}", key=f"v_{tdict.get('id')}"):
                st.session_state["treino_visualizar_id"] = tdict.get("id")
                st.session_state["pagina_atual"] = "visualizar_treino"
                st.rerun()
