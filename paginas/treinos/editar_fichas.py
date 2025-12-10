import streamlit as st
from repositories.fichas_repository import atualizar_ficha, buscar_ficha_por_id
from repositories.treinos_repository import listar_treinos_por_ficha, criar_treino, excluir_treino
from utils.exceptions import ValidationError, DatabaseError

# Estado usado para guardar qual treino está aguardando confirmação de exclusão
if "treino_excluir_id" not in st.session_state:
    st.session_state["treino_excluir_id"] = None


def mostrar():
    st.title("📋 Editar Ficha")

    # Recupera o ID da ficha que o usuário selecionou na tela anterior
    ficha_id = st.session_state.get("ficha_id")
    if not ficha_id:
        st.warning("Nenhuma ficha selecionada.")
        if st.button("⬅ Voltar"):
            st.session_state["pagina_atual"] = "fichas"
            st.rerun()
        return

    # Busca a ficha pelo ID
    ficha = buscar_ficha_por_id(ficha_id)
    if not ficha:
        st.error("Ficha não encontrada.")
        return

    # Mostra o nome da ficha no topo
    st.markdown(
        f"<p style='text-align:left; color:gray;'>Ficha selecionada: <b>{ficha.nome}</b></p>",
        unsafe_allow_html=True
    )

    # =============================================================
    # FORMULÁRIO DE EDIÇÃO DA FICHA
    # =============================================================
    st.subheader("✏️ Editar Informações da Ficha")

    with st.form("form_editar_ficha"):
        # Campos preenchidos com o valor atual
        novo_nome = st.text_input("Nome da ficha", value=ficha.nome)
        novas_obs = st.text_area("Observações", value=ficha.observacoes or "")

        # Botão do form
        salvar = st.form_submit_button("💾 Salvar Alterações")

        if salvar:
            try:
                # Validação básica
                if not novo_nome.strip():
                    raise ValidationError("O nome da ficha é obrigatório.")

                # Atualiza a ficha no banco
                atualizar_ficha(ficha.id, novo_nome, novas_obs)
                st.success("Ficha atualizada com sucesso!")

            except ValidationError as e:
                st.warning(e.message)
            except DatabaseError as e:
                st.error(e.message)
            except Exception:
                st.error("Erro inesperado ao salvar a ficha.")

    st.divider()

    # =============================================================
    # LISTAGEM DOS TREINOS DA FICHA
    # =============================================================
    st.subheader("🏋️ Treinos da Ficha")

    # Busca treinos associados à ficha
    treinos = listar_treinos_por_ficha(ficha.id)

    for treino in treinos:
        # Layout: nome do treino + botões editar/excluir
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"**{treino.nome}**")

        with col2:
            # Envia para a tela de editar treino
            if st.button("✏️ Editar", key=f"editar_treino_{treino.id}"):
                st.session_state["treino_id"] = treino.id
                st.session_state["pagina_atual"] = "editar_treino"
                st.rerun()

        with col3:
            # Abrir popup de confirmação de exclusão
            if st.button("🗑️ Excluir", key=f"excluir_treino_{treino.id}"):
                st.session_state["treino_excluir_id"] = treino.id
                st.rerun()

    # =============================================================
    # POPUP DE CONFIRMAÇÃO DE EXCLUSÃO
    # =============================================================
    if st.session_state["treino_excluir_id"] is not None:
        treino_id = st.session_state["treino_excluir_id"]

        # Descobre o nome do treino a partir da lista já carregada
        treino_nome = next((t.nome for t in treinos if t.id == treino_id), "Treino")

        st.markdown("### ⚠️ Confirmar Exclusão")
        st.warning(f"Tem certeza que deseja excluir o treino **{treino_nome}**?")

        colA, colB = st.columns(2)

        with colA:
            # Cancela a exclusão
            if st.button("❌ Cancelar", key="cancelar_excluir_treino"):
                st.session_state["treino_excluir_id"] = None
                st.rerun()

        with colB:
            # Confirma a exclusão no banco
            if st.button("🗑️ Confirmar Exclusão", key="confirmar_excluir_treino"):
                try:
                    excluir_treino(treino_id)
                    st.session_state["treino_excluir_id"] = None
                    st.success("Treino excluído com sucesso!")
                    st.rerun()
                except DatabaseError as e:
                    st.error(e.message)
                except Exception:
                    st.error("Erro ao excluir treino.")

    # =============================================================
    # ADICIONAR NOVO TREINO À FICHA
    # =============================================================
    if len(treinos) < 10:
        if st.button("➕ Adicionar Mais Treinos"):
            try:
                # Cria nome padrão ex: "Treino 3"
                novo_nome = f"Treino {len(treinos) + 1}"
                criar_treino(ficha.id, novo_nome)
                st.success("Novo treino criado com sucesso.")
                st.rerun()

            except DatabaseError as e:
                st.error(e.message)
            except Exception:
                st.error("Erro ao criar novo treino.")
    else:
        st.info("Limite máximo de 10 treinos atingido.")

    st.divider()

    # =============================================================
    # BOTÃO VOLTAR
    # =============================================================
    if st.button("⬅ Voltar"):
        st.session_state["pagina_atual"] = "fichas"
        st.rerun()
