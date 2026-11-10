from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.candidato_model import Candidato
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

    def obter_candidatura_por_id(self, candidatura_id: int) -> Candidatura | None:
        return self.session.get(Candidatura, candidatura_id)

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

    def obter_candidaturas(self) -> list[Candidatura]:
        comando = select(Candidatura)
        return list(self.session.scalars(comando).all())

    def contar_votos_na_urna(self, urna_id: int) -> int:
        comando = select(func.sum(Candidatura.votos)).where(Candidatura.urna_id == urna_id)
        return self.session.execute(comando).scalar() or 0

    def apagar_candidatura(self, candidatura_id: int):
        candidatura = self.obter_candidatura_por_id(candidatura_id)
        if not candidatura:
            raise ValueError("Não existe candidatura com esse id")

        self.session.delete(candidatura)

    def votos_por_partido(self) -> dict[str, int]:
        comando = select(
            Candidato.partido,
            func.coalesce(func.sum(Candidatura.votos), 0),
        ).join(Candidatura, Candidatura.candidato_id == Candidato.id).group_by(Candidato.partido)

        resultados = self.session.execute(comando).all()

        return dict(resultados)