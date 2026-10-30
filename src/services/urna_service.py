from sqlalchemy.orm import Session

from repositories.urna_repository import UrnaRepository
from schemas.urna_schema import UrnaCreate, UrnaResponse


class UrnaService:
    def __init__(self, session: Session, repository: UrnaRepository):
        self.session = session
        self.repository = repository

    def criar_urna(self, urna: UrnaCreate) -> UrnaResponse:
        try:
            self.repository.adicionar_urna(urna)
            self.session.commit()
            self.session.refresh(urna)
            schema = UrnaResponse.model_validate(urna)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def fechar_urna(self, urna_id: int):
        try:
            self.repository.fechar_urna(urna_id)
            self.session.commit()
            self.session.refresh(urna_id)
        except Exception:
            self.session.rollback()
            raise

    def mostrar_todas_urnas(self) -> list[UrnaResponse]:
        urnas_response = []
        urnas = self.repository.listar_urnas()
        for urna in urnas:
            schema = UrnaResponse.model_validate(urna)
            urnas_response.append(schema)
        return urnas_response