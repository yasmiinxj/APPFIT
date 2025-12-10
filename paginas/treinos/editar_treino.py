import os, sys
# Adiciona o caminho raiz do projeto ao sys.path para permitir imports relativos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import streamlit as st
# Repositórios e funções auxiliares
from repositories.treinos_repository import buscar_treino_por_id, atualizar_treino
from repositories.exercicios_repository import excluir_exercicio
from utils.exceptions import DatabaseError, ValidationError
from data.database import get_conn
from repositories.series_repository import listar_series_por_exercicio


def mostrar():
    """Página real de edição de treino."""
    # Recupera o treino selecionado da sessão
    treino_id = st.session_state.get("treino_id")
    if not treino_id:
        # Nenhum treino selecionado → avisa e mostra botão de voltar
        st.warning("Nenhum treino selecionado.")
        if st.button("⬅ Voltar"):
            st.session_state["pagina_atual"] = "editar_ficha"
            st.rerun()
        return

    # Busca o treino no banco
    treino = buscar_treino_por_id(treino_id)
    if not treino:
        st.error("Treino não encontrado.")
        return

    # Título da página
    st.title(f"🏋️ Editar Treino: {treino.nome}")

    # ---------------- FORMULÁRIO PARA EDITAR TREINO ----------------
    with st.form("form_editar_treino"):
        nome_treino = st.text_input("Nome do Treino", value=treino.nome)
        obs_treino = st.text_area(
            "Observações (máx 200 caracteres)",
            value=treino.observacoes or "",
            max_chars=200,
        )
        salvar = st.form_submit_button("💾 Salvar Alterações")

        if salvar:
            try:
                # Validação simples
                if not nome_treino.strip():
                    raise ValidationError("O nome do treino é obrigatório.")
                # Atualiza o treino no banco
                atualizar_treino(treino.id, nome_treino, obs_treino)
                st.success("Treino atualizado com sucesso!")
                st.rerun()
            except ValidationError as e:
                st.warning(e.message)
            except DatabaseError as e:
                st.error(e.message)
            except Exception:
                st.error("Erro inesperado ao salvar o treino.")

    st.divider()

    # ---------------- FORMULÁRIO PARA CRIAR EXERCÍCIO ----------------

    st.subheader("➕ Adicionar Novo Exercício")

    # Cria lista temporária de séries se não existir
    if "series_temp" not in st.session_state:
        st.session_state["series_temp"] = []

    # Campos principais do exercício
    nome_exercicio = st.text_input("Nome do Exercício *")
    descanso = st.number_input("Descanso por série (segundos)", min_value=0, value=30)
    observacoes = st.text_area("Observações (opcional)", max_chars=200)

    st.markdown("### 🧱 Séries do Exercício")

    # Campos para adicionar nova série à lista temp
    col1, col2 = st.columns(2)
    with col1:
        repeticoes = st.number_input("Repetições", min_value=1, value=10, step=1)
    with col2:
        carga = st.number_input("Carga (kg, opcional)", min_value=0.0, value=0.0, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        # Adiciona série temporária
        if st.button("➕ Adicionar Série"):
            st.session_state.series_temp.append({
                "repeticoes": repeticoes,
                "carga": carga
            })
    with col2:
        # Limpa as séries adicionadas
        if st.button("🧹 Limpar Séries"):
            st.session_state.series_temp.clear()

    # Lista as séries já adicionadas no temp
    if st.session_state.series_temp:
        st.write("#### Séries adicionadas:")
        for i, serie in enumerate(st.session_state.series_temp):
            st.markdown(f"**{i + 1}.** {serie['repeticoes']} repetições — {serie['carga']} kg")

    # Salvar exercício com séries
    if st.button("💾 Salvar Exercício"):
        try:
            # Validações
            if not nome_exercicio.strip():
                raise ValidationError("O nome do exercício é obrigatório.")
            if not st.session_state.series_temp:
                raise ValidationError("Adicione ao menos uma série antes de salvar.")

            conn = get_conn()
            cursor = conn.cursor()

            # Cria o exercício
            cursor.execute(
                "INSERT INTO exercicios (treino_id, nome, descanso_segundos, observacoes) VALUES (?, ?, ?, ?)",
                (treino.id, nome_exercicio, descanso, observacoes),
            )
            exercicio_id = cursor.lastrowid

            # Cria as séries
            for i, serie in enumerate(st.session_state.series_temp):
                cursor.execute(
                    "INSERT INTO series (exercicio_id, numero, repeticoes, carga) VALUES (?, ?, ?, ?)",
                    (exercicio_id, i + 1, serie["repeticoes"], serie["carga"]),
                )

            conn.commit()
            conn.close()

            st.success("✅ Exercício e séries salvos com sucesso!")
            st.session_state.series_temp.clear()
            st.rerun()

        except ValidationError as e:
            st.warning(e.message)
        except DatabaseError as e:
            st.error(e.message)
        except Exception as e:
            st.error(f"Erro ao salvar exercício: {e}")

    st.divider()

    # ---------------- LISTA DE EXERCÍCIOS EXISTENTES ----------------

    st.subheader("📋 Exercícios do Treino")

    try:
        conn = get_conn()
        cursor = conn.cursor()
        # Busca exercícios do treino
        cursor.execute("SELECT * FROM exercicios WHERE treino_id = ? ORDER BY id ASC", (treino.id,))
        exercicios = cursor.fetchall()
        conn.close()

        if not exercicios:
            st.info("Nenhum exercício cadastrado para este treino ainda.")
        else:
            for exercicio in exercicios:
                # Container visual para cada exercício
                with st.container(border=True):
                    st.markdown(f"**🏋️ {exercicio['nome']}** — descanso: {exercicio['descanso_segundos']}s")
                    st.caption(exercicio['observacoes'] or "Sem observações")

                    # Busca séries associadas
                    series = listar_series_por_exercicio(exercicio["id"])
                    if series:
                        for s in series:
                            st.write(f"• {s['repeticoes']} repetições — {s['carga']} kg")
                    else:
                        st.write("_Nenhuma série cadastrada._")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("✏️ Editar (em breve)", key=f"edit_{exercicio['id']}")
                    with col2:
                        # Botão excluir exercício
                        if st.button("🗑️ Excluir", key=f"del_{exercicio['id']}"):
                            try:
                                excluir_exercicio(exercicio["id"])
                                st.success("Exercício excluído com sucesso!")
                                st.rerun()
                            except DatabaseError as e:
                                st.error(e.message)
                            except Exception:
                                st.error("Erro ao excluir exercício.")
    except Exception as e:
        st.error(f"Erro ao carregar exercícios: {e}")

    st.divider()

    # ---------------- BOTÃO VOLTAR ----------------
    if st.button("⬅ Voltar"):
        st.session_state.pop("treino_id", None)
        st.session_state["pagina_atual"] = "editar_fichas"
        st.rerun()
