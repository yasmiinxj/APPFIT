from dataclasses import dataclass

@dataclass
class Treino:
    """Modelo de treino associado a uma ficha."""
    id: int | None
    ficha_id: int
    nome: str
# models/treino.py
class Treino:
    def __init__(self, id, ficha_id, nome, observacoes=None):
        self.id = id
        self.ficha_id = ficha_id
        self.nome = nome
        self.observacoes = observacoes  # ✅ adicionamos este campo
