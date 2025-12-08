import streamlit as st
from repositories.fichas_repository import listar_fichas, criar_ficha, excluir_ficha, contar_fichas
from utils.exceptions import LimiteFichasError

# Estado para popup de confirmação
if "ficha_excluir_id" not in st.session_state:
    st.session_state["ficha_excluir_id"] = None


def mostrar():
    st.markdown("<h2 style='text-align: left;'>📄 Fichas de Treino</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: gray;'>Gerencie suas fichas de treino cadastradas.</p>", unsafe_allow_html=True)
    st.write("")

    # --------------- FORMULÁRIO DE CRIAÇÃO -----------------
    with st.form("form_criar_ficha", clear_on_submit=True):
        nome = st.text_input("Nome da ficha")
        qtd_treinos = st.number_input("Quantidade de treinos (máx: 10)", min_value=1, max_value=10, step=1)
        observacoes = st.text_area("Observações (opcional)")
        criar = st.form_submit_button("✅ Criar ficha")

        if criar:
            total = contar_fichas()
            if total >= 10:
                st.error("Limite máximo de 10 fichas atingido.")
                raise LimiteFichasError("Não é possível criar mais de 10 fichas.")

            if nome.strip():
                criar_ficha(nome, qtd_treinos, observacoes)
                st.success("Ficha criada com sucesso!")
                st.rerun()
            else:
                st.warning("O nome da ficha é obrigatório.")

    st.markdown("---")

    # --------------- LISTAGEM DE FICHAS -----------------
    fichas = listar_fichas()
    if not fichas:
        st.info("Nenhuma ficha cadastrada ainda.")
    else:
        for ficha in fichas:
            st.markdown(f"**🏋️ {ficha.nome}** — {ficha.quantidade_treinos} treinos")

            if ficha.observacoes:
                st.markdown(f"🗒️ _{ficha.observacoes}_")

            col1, col2, col3 = st.columns(3)

            # VER FICHA
            with col1:
                if st.button("👁️ Ver ficha", key=f"ver_{ficha.id}"):
                    st.session_state["ficha_visualizar_id"] = ficha.id
                    st.session_state["pagina_atual"] = "visualizar_ficha"
                    st.rerun()

            # EDITAR
            with col2:
                if st.button("✏️ Editar", key=f"editar_{ficha.id}"):
                    st.session_state["ficha_id"] = ficha.id
                    st.session_state["pagina_atual"] = "editar_fichas"
                    st.rerun()

            # EXCLUIR
            with col3:
                if st.button("🗑️ Excluir", key=f"excluir_{ficha.id}"):
                    st.session_state["ficha_excluir_id"] = ficha.id
                    st.rerun()

            st.markdown("---")

    # --------------- POPUP DE CONFIRMAÇÃO -----------------
    if st.session_state["ficha_excluir_id"] is not None:
        st.markdown("### ⚠️ Confirmar exclusão")
        st.warning("Tem certeza que deseja excluir esta ficha? Essa ação não pode ser desfeita.")

        colA, colB = st.columns(2)

        with colA:
            if st.button("❌ Cancelar", key="cancelar_excluir"):
                st.session_state["ficha_excluir_id"] = None
                st.rerun()

        with colB:
            if st.button("🗑️ Confirmar Exclusão", key="confirmar_excluir"):
                excluir_ficha(st.session_state["ficha_excluir_id"])
                st.session_state["ficha_excluir_id"] = None
                st.success("Ficha excluída com sucesso!")
                st.rerun()

    # --------------- VOLTAR -----------------
    if st.button("⬅️ Voltar"):
        st.session_state["pagina_atual"] = "treinos"
        st.rerun()
