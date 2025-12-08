"""Módulo de exceções personalizadas da aplicação."""


class ValidationError(Exception):
    """Erro de validação amigável para feedback ao usuário."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RepositoryError(Exception):
    """Erro genérico de acesso ao repositório."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DatabaseError(Exception):
    """Erro relacionado ao banco de dados."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class LimiteFichasError(Exception):
    """Erro lançado ao atingir o limite máximo de fichas permitidas."""
    def __init__(self, message: str = "Você atingiu o limite máximo de fichas permitidas (10)."):
        super().__init__(message)
        self.message = message
