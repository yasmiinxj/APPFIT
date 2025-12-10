from dataclasses import dataclass

@dataclass
class Treino:
    """Modelo de treino associado a uma ficha."""
    
    id: int | None            # ID único do treino (None enquanto não estiver salvo no banco)
    ficha_id: int             # ID da ficha à qual este treino pertence
    nome: str                 # Nome do treino (ex.: "Treino A", "Peito/Tríceps")

# models/treino.py
class Treino:
    def __init__(self, id, ficha_id, nome, observacoes=None):
        self.id = id                       # ID do treino (None antes de salvar)
        self.ficha_id = ficha_id           # ID da ficha referente a este treino
        self.nome = nome                   # Nome do treino
        self.observacoes = observacoes     # Observações opcionais sobre o treino
