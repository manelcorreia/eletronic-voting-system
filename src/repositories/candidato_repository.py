from sqlalchemy import select
from sqlalchemy.orm import Session

from models.candidato_model import Candidato
from schemas.candidato_schema import CandidatoCreate


class CandidatoRepository:
    def __init__(self, session: Session):
        self.session = session

    def adicionar(self, candidato: CandidatoCreate) -> Candidato:
        if self.obter_por_nome(candidato.nome) is not None:
            raise ValueError(f"Candidato '{candidato.nome}' já está registado")
        model = Candidato(**candidato.model_dump())
        self.session.add(model)
        return model

    def obter_por_nome(self, nome: str) -> Candidato | None:
        comando = select(Candidato).where(Candidato.nome == nome)
        return self.session.scalars(comando).one_or_none()

    def obter_por_id(self, candidato_id: int) -> Candidato | None:
        return self.session.get(Candidato, candidato_id)

    def total_votos_candidato(self, nome: str) -> int:
        candidato = self.obter_por_nome(nome)
        if candidato is None:
            raise KeyError(f"Candidato '{nome}' não foi encontrado")
        return candidato.total_votos

    def listar_candidatos(self) -> list[Candidato]:
        comando = select(Candidato).order_by(Candidato.nome)
        return list(self.session.scalars(comando).all())