import streamlit as st
# Importa operações do repositório de fichas (listar, criar, excluir e contar)
from repositories.fichas_repository import listar_fichas, criar_ficha, excluir_ficha, contar_fichas
# Exceção personalizada para limite de fichas
from utils.exceptions import LimiteFichasError

# Estado usado para guardar qual ficha será excluída
if "ficha_excluir_id" not in st.session_state:
    st.session_state["ficha_excluir_id"] = None


def mostrar():
    # Título da página
    st.markdown("<h2 style='text-align: left;'>📄 Fichas de Treino</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: gray;'>Gerencie suas fichas de treino cadastradas.</p>", unsafe_allow_html=True)
    st.write("")

    # ---------------- FORMULÁRIO DE CRIAÇÃO ----------------
    with st.form("form_criar_ficha", clear_on_submit=True):
        # Entrada: nome da ficha
        nome = st.text_input("Nome da ficha")
        # Entrada: quantidade de treinos limitada de 1 a 10
        qtd_treinos = st.number_input("Quantidade de treinos (máx: 10)", min_value=1, max_value=10, step=1)
        # Entrada: observações opcionais
        observacoes = st.text_area("Observações (opcional)")
        # Botão de submit
        criar = st.form_submit_button("✅ Criar ficha")

        if criar:
            # Conta quantas fichas já existem no sistema
            total = contar_fichas()
            if total >= 10:
                # Se já há 10 fichas, bloqueia criação
                st.error("Limite máximo de 10 fichas atingido.")
                raise LimiteFichasError("Não é possível criar mais de 10 fichas.")

            # Valida nome obrigatório
            if nome.strip():
                # Cria a ficha no banco
                criar_ficha(nome, qtd_treinos, observacoes)
                st.success("Ficha criada com sucesso!")
                st.rerun()
            else:
                st.warning("O nome da ficha é obrigatório.")

    st.markdown("---")

    # ---------------- LISTAGEM DE FICHAS ----------------
    fichas = listar_fichas()

    # Se não houver fichas cadastradas
    if not fichas:
        st.info("Nenhuma ficha cadastrada ainda.")
    else:
        # Exibe cada ficha cadastrada
        for ficha in fichas:
            st.markdown(f"**🏋️ {ficha.nome}** — {ficha.quantidade_treinos} treinos")

            # Exibe observações, caso existam
            if ficha.observacoes:
                st.markdown(f"🗒️ _{ficha.observacoes}_")

            # Três botões: ver, editar e excluir
            col1, col2, col3 = st.columns(3)

            # Botão de visualizar ficha
            with col1:
                if st.button("👁️ Ver ficha", key=f"ver_{ficha.id}"):
                    # Guarda id e muda de página
                    st.session_state["ficha_visualizar_id"] = ficha.id
                    st.session_state["pagina_atual"] = "visualizar_ficha"
                    st.rerun()

            # Botão de editar ficha
            with col2:
                if st.button("✏️ Editar", key=f"editar_{ficha.id}"):
                    st.session_state["ficha_id"] = ficha.id
                    st.session_state["pagina_atual"] = "editar_fichas"
                    st.rerun()

            # Botão de excluir ficha → ativa popup
            with col3:
                if st.button("🗑️ Excluir", key=f"excluir_{ficha.id}"):
                    st.session_state["ficha_excluir_id"] = ficha.id
                    st.rerun()

            st.markdown("---")

    # ---------------- POPUP DE CONFIRMAÇÃO ----------------
    if st.session_state["ficha_excluir_id"] is not None:
        # Título e alerta de exclusão
        st.markdown("### ⚠️ Confirmar exclusão")
        st.warning("Tem certeza que deseja excluir esta ficha? Essa ação não pode ser desfeita.")

        colA, colB = st.columns(2)

        # Botão cancelar
        with colA:
            if st.button("❌ Cancelar", key="cancelar_excluir"):
                st.session_state["ficha_excluir_id"] = None
                st.rerun()

        # Botão confirmar exclusão
        with colB:
            if st.button("🗑️ Confirmar Exclusão", key="confirmar_excluir"):
                excluir_ficha(st.session_state["ficha_excluir_id"])
                st.session_state["ficha_excluir_id"] = None
                st.success("Ficha excluída com sucesso!")
                st.rerun()

    # ---------------- VOLTAR ----------------
    if st.button("⬅️ Voltar"):
        st.session_state["pagina_atual"] = "treinos"
        st.rerun()
