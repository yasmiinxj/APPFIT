from dataclasses import dataclass

@dataclass
class Ficha:
    """Modelo de ficha de treino."""

    # Identificador único da ficha.
    # Pode ser None quando ainda não foi salva no banco.
    id: int | None

    # Nome da ficha, geralmente algo como "Hipertrofia A/B"
    # ou "Treino para superiores".
    nome: str

    # Quantos treinos essa ficha possui (ex.: 3 treinos = A, B e C).
    quantidade_treinos: int

    # Observações gerais, como instruções do treinador.
    # Campo opcional.
    observacoes: str | None = None
