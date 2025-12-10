"""Módulo de exceções personalizadas da aplicação."""


class ValidationError(Exception):
    """Erro de validação amigável para feedback ao usuário."""
    def __init__(self, message: str):
        super().__init__(message)   # Passa a mensagem para a classe Exception
        self.message = message      # Armazena a mensagem para acesso direto


class RepositoryError(Exception):
    """Erro genérico de acesso ao repositório."""
    def __init__(self, message: str):
        super().__init__(message)   # Chama Exception com a mensagem
        self.message = message      # Guarda a mensagem da exceção


class DatabaseError(Exception):
    """Erro relacionado ao banco de dados."""
    def __init__(self, message: str):
        super().__init__(message)   # Inicializa a exceção base com a mensagem
        self.message = message      # Salva a mensagem para uso interno


class LimiteFichasError(Exception):
    """Erro lançado ao atingir o limite máximo de fichas permitidas."""
    def __init__(self, message: str = "Você atingiu o limite máximo de fichas permitidas (10)."):
        super().__init__(message)   # Envia a mensagem para a Exception padrão
        self.message = message      # Mantém a mensagem como atributo da classe
