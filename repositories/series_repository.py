from data.database import get_conn

def listar_series_por_exercicio(exercicio_id):
    conn = get_conn()  # abre conexão com o banco
    cursor = conn.cursor()
    # busca todas as séries desse exercício, ordenadas pelo número da série
    cursor.execute("SELECT * FROM series WHERE exercicio_id = ? ORDER BY numero ASC", (exercicio_id,))
    rows = cursor.fetchall()  # pega todos os resultados
    conn.close()  # fecha conexão
    return rows  # retorna as séries encontradas

def criar_serie(exercicio_id):
    conn = get_conn()
    cursor = conn.cursor()
    # conta quantas séries já existem para esse exercício
    cursor.execute("SELECT COUNT(*) FROM series WHERE exercicio_id = ?", (exercicio_id,))
    numero = cursor.fetchone()[0] + 1  # define o número da nova série (sequencial)
    # insere série nova com repeticoes = 0 e carga = "não informado"
    cursor.execute(
        "INSERT INTO series (exercicio_id, numero, repeticoes, carga) VALUES (?, ?, ?, ?)",
        (exercicio_id, numero, 0, 'não informado'),
    )
    conn.commit()  # salva no banco
    conn.close()  # fecha conexão

def excluir_serie(serie_id):
    conn = get_conn()
    cursor = conn.cursor()
    # apaga a série pelo id
    cursor.execute("DELETE FROM series WHERE id = ?", (serie_id,))
    conn.commit()
    conn.close()

def duplicar_serie(serie_id):
    conn = get_conn()
    cursor = conn.cursor()
    # busca dados da série que será duplicada
    cursor.execute("SELECT exercicio_id, numero, repeticoes, carga FROM series WHERE id = ?", (serie_id,))
    row = cursor.fetchone()
    if row:
        exercicio_id, numero, repeticoes, carga = row  # dados da série original
        # pega quantidade atual de séries para saber o novo número sequencial
        cursor.execute("SELECT COUNT(*) FROM series WHERE exercicio_id = ?", (exercicio_id,))
        novo_numero = cursor.fetchone()[0] + 1
        # cria nova série copiando repetições e carga da original
        cursor.execute(
            "INSERT INTO series (exercicio_id, numero, repeticoes, carga) VALUES (?, ?, ?, ?)",
            (exercicio_id, novo_numero, repeticoes, carga),
        )
    conn.commit()  # aplica mudanças
    conn.close()  # fecha conexão
