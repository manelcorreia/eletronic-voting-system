from models.pessoa_model import Pessoa
from repositories.pessoa_repository import PessoaRepository
from schemas.pessoa_schema import PessoaCreate, PessoaResponse


class PessoaService:
    def __init__(self, session, repository: PessoaRepository):
        self.session = session
        self.repository = repository

    def criar_pessoa(self, pessoa: PessoaCreate) -> PessoaResponse:
        try:
            pessoa = self.repository.adicionar_pessoa(pessoa)
            self.session.commit()
            self.session.refresh(pessoa)
            schema = PessoaResponse.model_validate(pessoa)
            return schema
        except Exception:
            self.session.rollback()
            raise