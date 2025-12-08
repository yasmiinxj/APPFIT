from dataclasses import dataclass

@dataclass
class Ficha:
    """Modelo de ficha de treino."""
    id: int | None
    nome: str
    quantidade_treinos: int
    observacoes: str | None = None
