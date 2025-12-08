import sqlite3
import os

# Caminho correto para o banco
DB_PATH = os.path.join(os.path.dirname(__file__), "fitness.db")

def get_conn():
    """Retorna conexão ativa com o banco SQLite. Cria o banco se não existir."""
    # Garante que a pasta existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria todas as tabelas necessárias, caso não existam."""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fichas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade_treinos INTEGER DEFAULT 0,
                observacoes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (ficha_id) REFERENCES fichas(id) ON DELETE CASCADE
            )
        """)

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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_treino (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha_id INTEGER NOT NULL,
                treino_id INTEGER NOT NULL,
                comentario TEXT,
                data_registro TEXT NOT NULL,
                FOREIGN KEY (ficha_id) REFERENCES fichas(id) ON DELETE CASCADE,
                FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
    finally:
        if 'conn' in locals():
            conn.close()
