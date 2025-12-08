import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import streamlit as st
from repositories.treinos_repository import buscar_treino_por_id, atualizar_treino
from repositories.exercicios_repository import excluir_exercicio
from utils.exceptions import DatabaseError, ValidationError
from data.database import get_conn
from repositories.series_repository import listar_series_por_exercicio


def mostrar():
    """Página real de edição de treino."""
    treino_id = st.session_state.get("treino_id")
    if not treino_id:
        st.warning("Nenhum treino selecionado.")
        if st.button("⬅ Voltar"):
            st.session_state["pagina_atual"] = "editar_ficha"
            st.rerun()
        return

    treino = buscar_treino_por_id(treino_id)
    if not treino:
        st.error("Treino não encontrado.")
        return

    st.title(f"🏋️ Editar Treino: {treino.nome}")

    # --- Formulário principal de edição do treino ---
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
                if not nome_treino.strip():
                    raise ValidationError("O nome do treino é obrigatório.")
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

    # --- Formulário de novo exercício ---
    st.subheader("➕ Adicionar Novo Exercício")

    if "series_temp" not in st.session_state:
        st.session_state["series_temp"] = []

    # Campos principais do exercício
    nome_exercicio = st.text_input("Nome do Exercício *")
    descanso = st.number_input("Descanso por série (segundos)", min_value=0, value=30)
    observacoes = st.text_area("Observações (opcional)", max_chars=200)

    st.markdown("### 🧱 Séries do Exercício")

    # Campos para adicionar série
    col1, col2 = st.columns(2)
    with col1:
        repeticoes = st.number_input("Repetições", min_value=1, value=10, step=1)
    with col2:
        carga = st.number_input("Carga (kg, opcional)", min_value=0.0, value=0.0, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Série"):
            st.session_state.series_temp.append({
                "repeticoes": repeticoes,
                "carga": carga
            })
    with col2:
        if st.button("🧹 Limpar Séries"):
            st.session_state.series_temp.clear()

    # Exibe séries adicionadas
    if st.session_state.series_temp:
        st.write("#### Séries adicionadas:")
        for i, serie in enumerate(st.session_state.series_temp):
            st.markdown(f"**{i + 1}.** {serie['repeticoes']} repetições — {serie['carga']} kg")

    # Botão final para salvar o exercício com as séries
    if st.button("💾 Salvar Exercício"):
        try:
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

            # Cria as séries associadas
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

    # --- Lista de exercícios existentes ---
    st.subheader("📋 Exercícios do Treino")

    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM exercicios WHERE treino_id = ? ORDER BY id ASC", (treino.id,))
        exercicios = cursor.fetchall()
        conn.close()

        if not exercicios:
            st.info("Nenhum exercício cadastrado para este treino ainda.")
        else:
            for exercicio in exercicios:
                with st.container(border=True):
                    st.markdown(f"**🏋️ {exercicio['nome']}** — descanso: {exercicio['descanso_segundos']}s")
                    st.caption(exercicio['observacoes'] or "Sem observações")

                    # Exibe séries
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

    # --- Botão voltar ---
    if st.button("⬅ Voltar"):
        st.session_state.pop("treino_id", None)
        st.session_state["pagina_atual"] = "editar_fichas"
        st.rerun()
