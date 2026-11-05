from sqlalchemy.orm import Session

from repositories.urna_repository import UrnaRepository
from schemas.pessoa_schema import PessoaResponse
from schemas.urna_schema import UrnaCreate, UrnaResponse
from services.permissoes import exigir_cargo_responsavel, verificar_se_faz_parte_da_urna


class UrnaService:
    def __init__(self, session: Session, repository: UrnaRepository):
        self.session = session
        self.repository = repository

    def criar_urna(self, urna: UrnaCreate) -> UrnaResponse:
        try:
            model = self.repository.adicionar_urna(urna)
            self.session.commit()
            self.session.refresh(model)
            schema = UrnaResponse.model_validate(urna)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def fechar_urna(self, pessoa: PessoaResponse, urna_id: int):
        urna = self.repository.obter_urna_por_id(urna_id)
        if urna is None:
            raise ValueError("Não existe urna com esse ID")
        schema_urna = UrnaResponse.model_validate(urna)
        exigir_cargo_responsavel(pessoa)
        verificar_se_faz_parte_da_urna(pessoa, schema_urna)

        try:
            self.repository.fechar_urna(urna_id)
            self.session.commit()
            self.session.refresh(urna)
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