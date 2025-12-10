"""Repositório para registros (histórico) de treinos realizados."""
from typing import List, Dict
from data.database import get_conn
from utils.exceptions import DatabaseError
from datetime import datetime

# Formato padrão utilizado na data dos registros (dia/mês/ano hora:minuto)
DATE_FORMAT = "%d/%m/%Y %H:%M"


def criar_registro(ficha_id: int, treino_id: int, comentario: str | None = None, data_text: str | None = None) -> int:
    """Cria um novo registro de treino no histórico.
    
    - Se data_text não for enviada, a função gera a data atual.
    - Retorna o ID do registro criado.
    - Qualquer erro na escrita do banco é convertido em DatabaseError.
    """
    try:
        conn = get_conn()            # Abre conexão com o banco
        cursor = conn.cursor()

        # Se a data não foi fornecida, gera uma automaticamente
        if data_text is None:
            data_text = datetime.now().strftime(DATE_FORMAT)

        # Insere o registro no banco
        cursor.execute(
            "INSERT INTO registros_treino (ficha_id, treino_id, comentario, data_registro) VALUES (?, ?, ?, ?)",
            (ficha_id, treino_id, comentario, data_text)
        )

        conn.commit()                # Salva as alterações
        return cursor.lastrowid      # Retorna o ID gerado

    except Exception as e:
        # Captura qualquer exceção e transforma em erro da aplicação
        raise DatabaseError(f"Erro ao criar registro de treino: {e}")

    finally:
        conn.close()                 # Fecha a conexão, independente do resultado


def listar_registros_por_ficha(ficha_id: int) -> List[Dict]:
    """Lista todos os registros de uma ficha específica.
    
    - Junta dados da ficha e do treino para exibir nomes diretamente.
    - Ordena do mais recente para o mais antigo.
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Consulta com JOINs para trazer nome da ficha e nome do treino
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
            # Converte cada linha do banco para um dicionário manipulável
            registros.append({
                "id": row[0],
                "ficha_id": row[1],
                "treino_id": row[2],
                "comentario": row[3],
                "data": row[4],
                "treino_nome": row[5] or "—",   # Se estiver NULL, mostra um traço
                "ficha_nome": row[6] or "—",
            })

        return registros

    except Exception as e:
        raise DatabaseError(f"Erro ao listar registros: {e}")

    finally:
        conn.close()


def listar_todos_registros() -> List[Dict]:
    """Lista todos os registros do sistema.
    
    - Utilizado em páginas gerais de histórico.
    - Ordena sempre do mais atual para o mais antigo.
    """
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
