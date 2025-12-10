from data.database import get_conn

def criar_exercicio(treino_id, nome, descanso, observacoes):
    # Abre conexão com o banco usando o helper centralizado.
    conn = get_conn()
    cursor = conn.cursor()

    # Inserção de um novo exercício.
    # Cada exercício pertence a um treino (FK treino_id).
    # descanso_segundos e observacoes são informações adicionais do exercício.
    cursor.execute(
        "INSERT INTO exercicios (treino_id, nome, descanso_segundos, observacoes) VALUES (?, ?, ?, ?)",
        (treino_id, nome, descanso, observacoes),
    )

    # Grava a alteração no banco.
    conn.commit()

    # Fecha a conexão — evita conexões abertas e travamento de arquivos.
    conn.close()

def listar_exercicios_por_treino(treino_id):
    # Abre conexão com o banco.
    conn = get_conn()
    cursor = conn.cursor()

    # Busca todos os exercícios vinculados a um treino específico.
    # ORDER BY garante que os exercícios apareçam sempre na mesma ordem.
    cursor.execute("SELECT * FROM exercicios WHERE treino_id = ? ORDER BY id ASC", (treino_id,))
    rows = cursor.fetchall()  # retorna lista de linhas (estrutura como dict por row_factory)

    conn.close()  # sempre fechar conexão após consulta
    return rows  # devolve lista completa dos exercícios encontrados

def excluir_exercicio(exercicio_id):
    # Abre a conexão.
    conn = get_conn()
    cursor = conn.cursor()

    # Remove primeiro as séries do exercício (dependências FK).
    # Isso evita erros de integridade, caso a FK não esteja com CASCADE.
    cursor.execute("DELETE FROM series WHERE exercicio_id = ?", (exercicio_id,))

    # Depois remove o próprio exercício.
    cursor.execute("DELETE FROM exercicios WHERE id = ?", (exercicio_id,))

    # Salva alterações no banco.
    conn.commit()

    # Fecha conexão.
    conn.close()
