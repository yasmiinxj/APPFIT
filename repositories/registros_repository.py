"""Repositório para registros (histórico) de treinos realizados."""
from typing import List, Dict
from data.database import get_conn
from utils.exceptions import DatabaseError
from datetime import datetime

DATE_FORMAT = "%d/%m/%Y %H:%M"

def criar_registro(ficha_id: int, treino_id: int, comentario: str | None = None, data_text: str | None = None) -> int:
    """Cria um registro de treino. data_text opcional (já formatada)."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        if data_text is None:
            data_text = datetime.now().strftime(DATE_FORMAT)
        cursor.execute(
            "INSERT INTO registros_treino (ficha_id, treino_id, comentario, data_registro) VALUES (?, ?, ?, ?)",
            (ficha_id, treino_id, comentario, data_text)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        raise DatabaseError(f"Erro ao criar registro de treino: {e}")
    finally:
        conn.close()

def listar_registros_por_ficha(ficha_id: int) -> List[Dict]:
    """Lista registros para uma ficha, ordenados por data (mais recentes primeiro)."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.ficha_id, r.treino_id, r.comentario, r.data_registro,
                   t.nome as treino_nome, f.nome as ficha_nome
            FROM registros_treino r
            LEFT JOIN treinos t ON t.id = r.treino_id
            LEFT JOIN fichas f ON f.id = r.ficha_id
            WHERE r.ficha_id = ?
            ORDER BY r.id DESC
        """, (ficha_id,))
        rows = cursor.fetchall()
        registros = []
        for row in rows:
            registros.append({
                "id": row[0],
                "ficha_id": row[1],
                "treino_id": row[2],
                "comentario": row[3],
                "data": row[4],
                "treino_nome": row[5] or "—",
                "ficha_nome": row[6] or "—",
            })
        return registros
    except Exception as e:
        raise DatabaseError(f"Erro ao listar registros: {e}")
    finally:
        conn.close()

def listar_todos_registros() -> List[Dict]:
    """Lista todos os registros ordenados por data (mais recentes primeiro)."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.ficha_id, r.treino_id, r.comentario, r.data_registro,
                   t.nome as treino_nome, f.nome as ficha_nome
            FROM registros_treino r
            LEFT JOIN treinos t ON t.id = r.treino_id
            LEFT JOIN fichas f ON f.id = r.ficha_id
            ORDER BY r.id DESC
        """)
        rows = cursor.fetchall()
        registros = []
        for row in rows:
            registros.append({
                "id": row[0],
                "ficha_id": row[1],
                "treino_id": row[2],
                "comentario": row[3],
                "data": row[4],
                "treino_nome": row[5] or "—",
                "ficha_nome": row[6] or "—",
            })
        return registros
    except Exception as e:
        raise DatabaseError(f"Erro ao listar registros: {e}")
    finally:
        conn.close()
