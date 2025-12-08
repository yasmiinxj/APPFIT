"""Repositório de operações relacionadas às fichas de treino."""
import sqlite3
from data.database import get_conn, init_db
from models.ficha import Ficha
from utils.exceptions import DatabaseError

# Garante que o banco e tabelas existem antes de qualquer operação
init_db()

def criar_ficha(nome: str, quantidade_treinos: int, observacoes: str | None = None) -> int:
    """Cria uma nova ficha no banco de dados."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fichas (nome, quantidade_treinos, observacoes) VALUES (?, ?, ?)",
            (nome, quantidade_treinos, observacoes),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao criar ficha: {e}")
    finally:
        if conn:
            conn.close()


def listar_fichas() -> list[Ficha]:
    """Retorna todas as fichas cadastradas."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, quantidade_treinos, observacoes FROM fichas ORDER BY id ASC")
        rows = cursor.fetchall()
        return [
            Ficha(id=row[0], nome=row[1], quantidade_treinos=row[2], observacoes=row[3])
            for row in rows
        ]
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao listar fichas: {e}")
    finally:
        if conn:
            conn.close()


def buscar_ficha_por_id(ficha_id: int) -> Ficha | None:
    """Busca uma ficha específica pelo ID."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, quantidade_treinos, observacoes FROM fichas WHERE id = ?",
            (ficha_id,),
        )
        row = cursor.fetchone()
        if row:
            return Ficha(id=row[0], nome=row[1], quantidade_treinos=row[2], observacoes=row[3])
        return None
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao buscar ficha: {e}")
    finally:
        if conn:
            conn.close()


def atualizar_ficha(ficha_id: int, nome: str, observacoes: str | None):
    """Atualiza nome e observações da ficha."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE fichas SET nome = ?, observacoes = ? WHERE id = ?",
            (nome, observacoes, ficha_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao atualizar ficha: {e}")
    finally:
        if conn:
            conn.close()


def excluir_ficha(ficha_id: int):
    """Exclui uma ficha específica."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fichas WHERE id = ?", (ficha_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao excluir ficha: {e}")
    finally:
        if conn:
            conn.close()


def contar_fichas() -> int:
    """Retorna a quantidade total de fichas cadastradas."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM fichas")
        (total,) = cursor.fetchone()
        return total
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao contar fichas: {e}")
    finally:
        if conn:
            conn.close()
