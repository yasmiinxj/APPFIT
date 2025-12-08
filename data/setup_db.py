import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sqlite3
import os
from utils.exceptions import DatabaseError

# Caminho único do banco
DB_PATH = os.path.join(os.path.dirname(__file__), "fitness.db")

def get_conn():
    """Retorna conexão ativa com o banco SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def column_exists(cursor, table_name, column_name):
    """Verifica se uma coluna existe em uma tabela."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

def init_db():
    """Cria o banco e todas as tabelas necessárias, migrando colunas se precisar."""
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # --- FICHAS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fichas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade_treinos INTEGER DEFAULT 0,
                observacoes TEXT
            )
        """)
        # Migração de colunas antigas
        if not column_exists(cursor, "fichas", "quantidade_treinos"):
            cursor.execute("ALTER TABLE fichas ADD COLUMN quantidade_treinos INTEGER DEFAULT 0")
        if not column_exists(cursor, "fichas", "observacoes"):
            cursor.execute("ALTER TABLE fichas ADD COLUMN observacoes TEXT")

        # --- TREINOS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (ficha_id) REFERENCES fichas(id) ON DELETE CASCADE
            )
        """)
        if not column_exists(cursor, "treinos", "observacoes"):
            cursor.execute("ALTER TABLE treinos ADD COLUMN observacoes TEXT")

        # --- EXERCICIOS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                treino_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                descanso INTEGER DEFAULT 30,
                observacoes TEXT,
                FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE
            )
        """)
        if not column_exists(cursor, "exercicios", "descanso"):
            cursor.execute("ALTER TABLE exercicios ADD COLUMN descanso INTEGER DEFAULT 30")
        if not column_exists(cursor, "exercicios", "observacoes"):
            cursor.execute("ALTER TABLE exercicios ADD COLUMN observacoes TEXT")

        # --- SERIES ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercicio_id INTEGER NOT NULL,
                numero INTEGER NOT NULL,
                repeticoes INTEGER DEFAULT 10,
                carga REAL,
                FOREIGN KEY (exercicio_id) REFERENCES exercicios(id) ON DELETE CASCADE
            )
        """)
        if not column_exists(cursor, "series", "carga"):
            try:
                cursor.execute("ALTER TABLE series ADD COLUMN carga REAL")
            except Exception:
                pass

        # --- REGISTROS DE TREINO ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_treino (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha_id INTEGER NOT NULL,
                treino_id INTEGER NOT NULL,
                comentario TEXT,
                data_registro TEXT NOT NULL,
                FOREIGN KEY(ficha_id) REFERENCES fichas(id) ON DELETE CASCADE,
                FOREIGN KEY(treino_id) REFERENCES treinos(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("🎯 Banco inicializado/migrado com sucesso!")

    except Exception as e:
        raise DatabaseError(f"Erro ao inicializar/migrar banco: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()
