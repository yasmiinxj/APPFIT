"""Repositório de operações relacionadas aos treinos."""
import sqlite3
from data.database import get_conn
from models.treino import Treino
from utils.exceptions import DatabaseError


def listar_treinos_por_ficha(ficha_id: int) -> list[Treino]:
    """Lista todos os treinos associados a uma ficha."""
    try:
        conn = get_conn()  # abre conexão com o banco
        cursor = conn.cursor()
        # busca treinos dessa ficha, ordenados pelo id
        cursor.execute(
            "SELECT id, ficha_id, nome, observacoes FROM treinos WHERE ficha_id = ? ORDER BY id ASC",
            (ficha_id,),
        )
        rows = cursor.fetchall()  # pega resultados
        # cria objetos Treino a partir das linhas retornadas
        return [
            Treino(id=row[0], ficha_id=row[1], nome=row[2], observacoes=row[3])
            for row in rows
        ]
    except sqlite3.Error as e:
        # erro de banco → lança exceção customizada
        raise DatabaseError(f"Erro ao listar treinos: {e}")
    finally:
        conn.close()  # garante fechamento da conexão


def criar_treino(ficha_id: int, nome: str, observacoes: str | None = None) -> int:
    """Cria um novo treino vinculado a uma ficha."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # insere novo treino
        cursor.execute(
            "INSERT INTO treinos (ficha_id, nome, observacoes) VALUES (?, ?, ?)",
            (ficha_id, nome, observacoes),
        )
        conn.commit()  # salva
        return cursor.lastrowid  # retorna id do treino criado
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao criar treino: {e}")
    finally:
        conn.close()


def buscar_treino_por_id(treino_id: int) -> Treino | None:
    """Busca um treino específico pelo ID."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # busca treino pelo id
        cursor.execute(
            "SELECT id, ficha_id, nome, observacoes FROM treinos WHERE id = ?",
            (treino_id,),
        )
        row = cursor.fetchone()  # retorna uma linha ou None
        if row:
            # converte a linha em objeto Treino
            return Treino(id=row[0], ficha_id=row[1], nome=row[2], observacoes=row[3])
        return None  # caso não exista
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao buscar treino: {e}")
    finally:
        conn.close()


def atualizar_treino(treino_id: int, nome: str, observacoes: str | None = None):
    """Atualiza as informações de um treino."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # atualiza nome e observações
        cursor.execute(
            "UPDATE treinos SET nome = ?, observacoes = ? WHERE id = ?",
            (nome, observacoes, treino_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao atualizar treino: {e}")
    finally:
        conn.close()


def excluir_treino(treino_id: int):
    """Exclui um treino e seus exercícios associados."""
    try:
        conn = get_conn()
        cursor = conn.cursor()
        # primeiro apaga os exercícios do treino
        cursor.execute("DELETE FROM exercicios WHERE treino_id = ?", (treino_id,))
        # depois apaga o treino em si
        cursor.execute("DELETE FROM treinos WHERE id = ?", (treino_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Erro ao excluir treino: {e}")
    finally:
        conn.close()
