from typing import Iterable, Optional

from models.candidato_model import Candidato
from models.pessoa_model import Pessoa
from repositories.candidato_repository import CandidatoRepository


class PessoaRepository:
    def __init__(self, pessoas: Iterable[Pessoa], candidatos: CandidatoRepository):
        self._pessoas = list(pessoas)
        self._candidatos = candidatos

    def adicionar_pessoa(self, pessoa: Pessoa):
        if self.obter_por_cc(pessoa.cc) is not None:
            raise ValueError("Pessoa já está registada")
        self._pessoas.append(pessoa)

    def obter_por_cc(self, cc: str) -> Optional[Pessoa]:
        return next((c for c in self._pessoas if c.cc == cc), None)

    def votar(self, pessoa: Pessoa, candidato: Candidato):
        pessoa = self.obter_por_cc(pessoa.cc)

        if pessoa is None:
            raise KeyError("Não existe pessoa registada com esse cc")

        if pessoa.votou:
            raise ValueError("Pessoa já votou")

        if self.repository.obter_por_nome(candidato.nome) is None:
            raise KeyError("Não existe candidato registado com esse nome")

        self.repository.receber_voto(candidato.nome)
        pessoa.votou = True