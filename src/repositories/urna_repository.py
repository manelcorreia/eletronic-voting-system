from sqlalchemy import select
from sqlalchemy.orm import Session

from models.urna_model import Urna
from schemas.urna_schema import UrnaCreate


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