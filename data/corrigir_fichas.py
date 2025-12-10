import sqlite3
import os

# Caminho absoluto para o banco de dados SQLite
DB_PATH = r"C:\Users\Yasmin\Desktop\APPFIT - Copia\data\fitness.db"

# Abre conexão com o banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Renomeia a tabela antiga para "fichas_old" (necessário para recriar com nova estrutura)
cursor.execute("ALTER TABLE fichas RENAME TO fichas_old")

# Cria a nova tabela "fichas" com estrutura atualizada
cursor.execute("""
CREATE TABLE fichas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade_treinos INTEGER NOT NULL DEFAULT 1,
    observacoes TEXT
)
""")

# Copia os dados da tabela antiga para a nova
# - IFNULL(qtd_treinos,1): garante que valores nulos virem 1
cursor.execute("""
INSERT INTO fichas (id, nome, quantidade_treinos, observacoes)
SELECT id, nome, IFNULL(qtd_treinos,1), observacoes FROM fichas_old
""")

# Exclui a tabela antiga agora que os dados já foram migrados
cursor.execute("DROP TABLE fichas_old")

# Salva as mudanças no banco
conn.commit()

# Fecha a conexão
conn.close()

# Mensagem final de sucesso
print("✅ Banco atualizado com sucesso!")
