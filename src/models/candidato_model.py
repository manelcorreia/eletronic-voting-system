from dataclasses import dataclass

@dataclass
class Candidato:
    nome: str
    votos: int = 0

    def __repr__(self):
        return f"Candidato({self.nome}, {self.votos})"