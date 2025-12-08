import streamlit as st
from repositories.fichas_repository import listar_fichas, buscar_ficha_por_id
from repositories.treinos_repository import listar_treinos_por_ficha, buscar_treino_por_id
from repositories.registros_repository import criar_registro, listar_todos_registros
from typing import Any

def _entity_to_dict(e: Any):
    """Normaliza objeto dataclass/dict/tuple para dict com chaves comuns usadas aqui."""
    if e is None:
        return {}
    # dataclass / object with attributes
    if hasattr(e, "__dict__") and not isinstance(e, dict):
        d = vars(e)
        # possíveis nomes diferentes
        return {
            "id": d.get("id"),
            "nome": d.get("nome"),
            "qtd_treinos": d.get("qtd_treinos") or d.get("quantidade_treinos") or d.get("qtdTreinos"),
            "observacoes": d.get("observacoes"),
            "quantidade_treinos": d.get("quantidade_treinos") or d.get("qtd_treinos") or d.get("qtdTreinos"),
        }
    # dict-like
    if isinstance(e, dict):
        return {
            "id": e.get("id"),
            "nome": e.get("nome"),
            "qtd_treinos": e.get("qtd_treinos") or e.get("quantidade_treinos"),
            "observacoes": e.get("observacoes"),
            "quantidade_treinos": e.get("quantidade_treinos") or e.get("qtd_treinos"),
        }
    # fallback
    return {"id": None, "nome": str(e), "qtd_treinos": None, "observacoes": None, "quantidade_treinos": None}

def mostrar():
    st.title("📚 Biblioteca de Treinos")

    # Voltar para a página 'treinos'
    if st.button("⬅ Voltar"):
        st.session_state["pagina_atual"] = "treinos"
        st.rerun()

    st.subheader("📘 Fichas (visualização)")

    fichas_raw = listar_fichas()
    fichas = [_entity_to_dict(f) for f in fichas_raw]

    if not fichas:
        st.info("Nenhuma ficha cadastrada ainda.")
        return

    # Cards de fichas (clicáveis)
    for f in fichas:
        with st.container():
            st.markdown(f"### 📄 {f['nome']}")
            qtd = f.get("quantidade_treinos") or f.get("qtd_treinos") or 0
            st.write(f"Treinos: {qtd}")
            if f.get("observacoes"):
                st.caption(f.get("observacoes"))

            if st.button("🔎 Ver Ficha", key=f"ver_ficha_{f['id']}"):
                st.session_state["pagina_atual"] = "visualizar_ficha"
                st.session_state["ficha_visualizar_id"] = f["id"]
                st.rerun()

    st.markdown("---")
    st.subheader("🟢 Registrar Treino Feito")

    # Formulário geral de registro
    ficha_map = {f["nome"]: f["id"] for f in fichas}
    ficha_names = list(ficha_map.keys())
    ficha_sel = st.selectbox("Escolha a ficha", options=ficha_names)
    ficha_id = ficha_map[ficha_sel]

    # Busca treinos dessa ficha (padroniza)
    treinos_raw = listar_treinos_por_ficha(ficha_id)
    treinos = []
    for t in treinos_raw:
        if isinstance(t, dict):
            treinos.append({"id": t.get("id"), "nome": t.get("nome"), "observacoes": t.get("observacoes")})
        else:
            # objeto
            try:
                treinos.append({"id": getattr(t, "id", None), "nome": getattr(t, "nome", str(t)), "observacoes": getattr(t, "observacoes", None)})
            except Exception:
                treinos.append({"id": None, "nome": str(t), "observacoes": None})

    if not treinos:
        st.warning("A ficha selecionada não tem treinos cadastrados.")
    treino_map = {t["nome"]: t["id"] for t in treinos} if treinos else {}
    treino_sel = st.selectbox("Escolha o treino", options=list(treino_map.keys()) if treino_map else ["-"])
    treino_id = treino_map.get(treino_sel)

    comentario = st.text_area("Comentário sobre o treino (opcional)", max_chars=500)

    if st.button("💾 Registrar"):
        if not treino_id:
            st.warning("Selecione um treino válido antes de registrar.")
        else:
            try:
                criar_registro(ficha_id=ficha_id, treino_id=treino_id, comentario=comentario)
                st.success("Registro salvo com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar registro: {e}")

    st.markdown("---")
    st.subheader("📅 Histórico de Registros (mais recentes primeiro)")

    try:
        from repositories.registros_repository import listar_todos_registros
        registros = listar_todos_registros()
        if not registros:
            st.info("Nenhum registro salvo ainda.")
        else:
            for reg in registros:
                with st.container():
                    st.markdown("**" + (reg.get("treino_nome") or "—") + "**")
                    st.write(f"**Ficha:** {reg.get('ficha_nome') or '—'}")
                    if reg.get("comentario"):
                        st.markdown(f"💬 {reg.get('comentario')}")
                    st.caption(f"📅 {reg.get('data')}")
                    st.markdown("---")
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
