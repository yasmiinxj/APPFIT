from data.database import get_conn

def criar_exercicio(treino_id, nome, descanso, observacoes):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO exercicios (treino_id, nome, descanso_segundos, observacoes) VALUES (?, ?, ?, ?)",
    (treino_id, nome, descanso, observacoes),
)

    conn.commit()
    conn.close()

def listar_exercicios_por_treino(treino_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercicios WHERE treino_id = ? ORDER BY id ASC", (treino_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def excluir_exercicio(exercicio_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM series WHERE exercicio_id = ?", (exercicio_id,))
    cursor.execute("DELETE FROM exercicios WHERE id = ?", (exercicio_id,))
    conn.commit()
    conn.close()
