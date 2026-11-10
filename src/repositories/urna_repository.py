from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.candidato_model import Candidato
from models.candidatura_model import Candidatura
from models.urna_model import Urna
from schemas.urna_schema import UrnaCreate, UrnaUpdate


class UrnaRepository:
    def __init__(self, session: Session):
        self.session = session

    def adicionar_urna(self, urna: UrnaCreate) -> Urna:
        if self.obter_urna_por_localidade(urna.localidade) is not None:
            raise ValueError("Já existe urna nessa localidade")
        model = Urna(**urna.model_dump())
        self.session.add(model)
        return model

    def obter_urna_por_id(self, urna_id: int) -> Urna | None:
        return self.session.get(Urna, urna_id)

    def obter_urna_por_localidade(self, localidade: str) -> Urna | None:
        comando = select(Urna).where(Urna.localidade == localidade)
        return self.session.scalars(comando).one_or_none()

    def fechar_urna(self, urna_id: int):
        urna = self.obter_urna_por_id(urna_id)

        if urna is None:
            raise ValueError("Não existe urna com esse id")

        urna.fechada = True

    def listar_urnas(self) -> list[Urna]:
        comando = select(Urna).order_by(Urna.localidade)
        return list(self.session.scalars(comando).all())

    def update_urna(self, urna_update: UrnaUpdate, urna_id: int) -> Urna:
        urna = self.obter_urna_por_id(urna_id)
        if urna is None:
            raise ValueError("Não existe urna com esse id")

        for chave, valor in urna_update.model_dump().items():
            setattr(urna, chave, valor)

        return urna

    def apagar_urna(self, urna_id: int):
        urna = self.obter_urna_por_id(urna_id)
        if urna is None:
            raise ValueError("Não existe urna com esse id")

        self.session.delete(urna)

    def votos_por_partido(self, urna_id: int) -> dict:
        dicionario: dict[str,int] = {}
        urna = self.obter_urna_por_id(urna_id)
        if urna is None:
            raise ValueError("Não existe urna com esse id")

        for candidatura in urna.candidaturas:
            partido = candidatura.candidato.partido
            dicionario[partido] += dicionario.get(partido, 0) + candidatura.votos

        return dicionario

    def votos_partido_especifico_na_urna(self, partido: str, urna_id: int) -> int:
        comando = select(
            func.sum(Candidatura.votos),
        ).join(Candidato, Candidatura.candidato_id == Candidato.id).where(
            Candidatura.urna_id == urna_id,
            Candidato.partido == partido,
        )

        resultado = self.session.execute(comando).scalar()
        return resultado or 0