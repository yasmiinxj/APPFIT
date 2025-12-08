import sqlite3
from data.database import get_conn

def criar_tabela_registros():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros_treino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ficha_id INTEGER NOT NULL,
        treino_id INTEGER NOT NULL,
        comentario TEXT,
        data TEXT NOT NULL,
        FOREIGN KEY(ficha_id) REFERENCES fichas(id) ON DELETE CASCADE,
        FOREIGN KEY(treino_id) REFERENCES treinos(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela_registros()
