from repositories.pessoa_repository import PessoaRepository
from schemas import UrnaResponse
from schemas.pessoa_schema import PessoaCreate, PessoaResponse
from services.permissoes import verificar_se_faz_parte_da_urna, exigir_cargo_admin, exigir_cargo_responsavel


class PessoaService:
    def __init__(self, session, repository: PessoaRepository):
        self.session = session
        self.repository = repository

    def criar_pessoa(self, pessoa: PessoaCreate) -> PessoaResponse:
        try:
            pessoa = self.repository.registar_pessoa(pessoa)
            self.session.commit()
            self.session.refresh(pessoa)
            schema = PessoaResponse.model_validate(pessoa)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def iniciar_sessao(self, cc: str, password: str, urna: UrnaResponse) -> PessoaResponse | None:
        try:
            pessoa = self.repository.iniciar_sessao(cc, password)
            if pessoa is not None:
                schema = PessoaResponse.model_validate(pessoa)
                verificar_se_faz_parte_da_urna(schema, urna)
                return schema
        except Exception:
            raise

    def iniciar_sessao_admin(self, cc: str, password: str) -> PessoaResponse:
        try:
            pessoa = self.repository.iniciar_sessao(cc, password)
            if pessoa is not None:
                schema = PessoaResponse.model_validate(pessoa)
                exigir_cargo_admin(schema)
                return schema
        except Exception:
            raise

    def confirmar_responsavel(self, cc: str, password: str) -> bool:
        pessoa = self.repository.iniciar_sessao(cc, password)
        if pessoa is not None:
            schema = PessoaResponse.model_validate(pessoa)
            exigir_cargo_responsavel(schema)
            return True
        return False
