from data.database import get_conn

def listar_series_por_exercicio(exercicio_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM series WHERE exercicio_id = ? ORDER BY numero ASC", (exercicio_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def criar_serie(exercicio_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM series WHERE exercicio_id = ?", (exercicio_id,))
    numero = cursor.fetchone()[0] + 1
    cursor.execute(
        "INSERT INTO series (exercicio_id, numero, repeticoes, carga) VALUES (?, ?, ?, ?)",
        (exercicio_id, numero, 0, 'não informado'),
    )
    conn.commit()
    conn.close()

def excluir_serie(serie_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM series WHERE id = ?", (serie_id,))
    conn.commit()
    conn.close()

def duplicar_serie(serie_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT exercicio_id, numero, repeticoes, carga FROM series WHERE id = ?", (serie_id,))
    row = cursor.fetchone()
    if row:
        exercicio_id, numero, repeticoes, carga = row
        cursor.execute("SELECT COUNT(*) FROM series WHERE exercicio_id = ?", (exercicio_id,))
        novo_numero = cursor.fetchone()[0] + 1
        cursor.execute(
            "INSERT INTO series (exercicio_id, numero, repeticoes, carga) VALUES (?, ?, ?, ?)",
            (exercicio_id, novo_numero, repeticoes, carga),
        )
    conn.commit()
    conn.close()
