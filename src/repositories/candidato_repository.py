from typing import Iterable, Optional

from models.candidato_model import Candidato


class CandidatoRepository:
    def __init__(self, candidatos: Iterable[Candidato] = ()):
        self._candidatos = list(candidatos)

    def adicionar(self, candidato: Candidato) -> None:
        if self.obter_por_nome(candidato.nome) is not None:
            raise ValueError(f"Candidato '{candidato.nome}' já está registado")
        self._candidatos.append(candidato)

    def obter_por_nome(self, nome: str) -> Optional[Candidato]:
        return next((c for c in self._candidatos if c.nome == nome), None)

    def listar_candidatos(self) -> list[Candidato]:
        return self._candidatos

    def receber_voto(self, nome: str):
        candidato = self.obter_por_nome(nome)
        if candidato is None:
            raise KeyError(f"Candidato '{nome}' não foi encontrado")
        candidato.votos += 1

    def total_votos_candidato(self, nome: str) -> int:
        candidato = self.obter_por_nome(nome)
        if candidato is None:
            raise KeyError(f"Candidato '{nome}' não foi encontrado")
        return candidato.votos