from sqlalchemy import select
from sqlalchemy.orm import Session

from models.candidatura_model import Candidatura
from repositories.pessoa_repository import PessoaRepository
from schemas.candidatura_schema import CandidaturaCreate


class CandidaturaRepository:
    def __init__(self, session: Session):
        self.session = session

    def adicionar_candidatura(self, candidatura: CandidaturaCreate) -> Candidatura:
        if self.obter_candidatura_urna_candidato(candidatura.urna_id, candidatura.candidato_id):
            raise ValueError("Já existe candidatura desse candidato nesta urna")
        model = Candidatura(**candidatura.model_dump())
        self.session.add(model)
        return model

    def obter_candidatura_urna_candidato(self, urna_id: int, candidato_id: int) -> Candidatura | None:
        comando = select(Candidatura).where(Candidatura.urna_id == urna_id, Candidatura.candidato_id == candidato_id)
        return self.session.scalars(comando).one_or_none()

    def voto(self, pessoa_cc: str, candidato_id: int):
        pessoa = PessoaRepository(self.session).obter_por_cc(pessoa_cc)
        if not pessoa:
            raise ValueError("Não existe pessoa com esse CC")
        if pessoa.votou:
            raise ValueError("Já votou")

        candidatura = self.obter_candidatura_urna_candidato(pessoa.urna_id, candidato_id)

        if candidatura is None:
            raise ValueError("Não pode votar")

        if candidatura.urna.fechada:
            raise ValueError("Urna já está fechada")

        candidatura.votos += 1
        pessoa.votou = True