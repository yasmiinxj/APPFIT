import sqlite3
import os

# Caminho correto para o banco (Persistência)
# Motivo da escolha: usar SQLite facilita a persistência local sem servidor.
DB_PATH = os.path.join(os.path.dirname(__file__), "fitness.db")

def get_conn():
    """Retorna conexão ativa com o banco SQLite.
    - Persistência: garante acesso e criação do banco.
    - Tratamento de Exceções: diretório é criado automaticamente evitando erro FileNotFound.
    """
    # Garante que a pasta existe (Previne exceção ao tentar salvar o banco)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)  # Conexão estabelecida
    conn.row_factory = sqlite3.Row  # Facilita acesso às colunas por nome
    return conn

def init_db():
    """Cria todas as tabelas necessárias.
    - Estrutura de Dados: modelagem das tabelas e relações.
    - Modularização: função isolada apenas para iniciar o banco.
    - Tratamento de Exceções: try/finally garante fechamento da conexão.
    """
    try:
        conn = get_conn()  # Persistência
        cursor = conn.cursor()

        # Estrutura de Dados: tabela para fichas de treino
        # Papel: armazena informações gerais da ficha
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fichas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade_treinos INTEGER DEFAULT 0,
                observacoes TEXT
            )
        """)

        # Tabela de treinos
        # Papel: organiza treinos vinculados a uma ficha (1:N)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ficha_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (ficha_id) REFERENCES fichas(id) ON DELETE CASCADE
            )
        """)

        # Tabela de exercícios
        # Papel: lista exercícios pertencentes a cada treino
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

        # Tabela de séries de cada exercício (estrutura hierárquica)
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

        # Tabela de registros de treino (histórico)
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

        conn.commit()  # Persistência: salva dados
    finally:
        if 'conn' in locals():
            conn.close()  # Tratamento seguro da conexão (independente de erro)


# --- NOVO MÓDULO: criação da tabela registros_treino ---
import sqlite3
from data.database import get_conn  # Modularização: reutiliza função de conexão existente


def criar_tabela_registros():
    """Cria a tabela de registros de treino.
    - Estrutura de Dados: tabela registrar histórico dos treinos.
    - Persistência: usa conexão SQLite para armazenar dados.
    - Tratamento de Exceções: não possui try/except explícito, mas depende de get_conn(),
      que já previne erros criando diretórios quando necessário.
    - Interface: função simples, voltada para inicialização do sistema.
    """
    conn = get_conn()  # Persistência: abre conexão com o banco
    cursor = conn.cursor()  # Manipulação direta no banco

    # Estrutura da tabela de registros (histórico de treinos)
    # Papel: armazenar cada sessão concluída, com data e comentário
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros_treino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  # Identificador único
        ficha_id INTEGER NOT NULL,  # FK para ficha
        treino_id INTEGER NOT NULL,  # FK para o treino
        comentario TEXT,  # Observações do treino
        data TEXT NOT NULL,  # Data do registro
        FOREIGN KEY(ficha_id) REFERENCES fichas(id) ON DELETE CASCADE,  # Cascata mantém integridade
        FOREIGN KEY(treino_id) REFERENCES treinos(id) ON DELETE CASCADE
    )
    """)

    conn.commit()  # Persistência: salva o estado
    conn.close()  # Boas práticas: libera recurso


# Interface do módulo: executa criação automática da tabela
if __name__ == "__main__":
    criar_tabela_registros()  # Ação direta quando o arquivo é executado sozinho