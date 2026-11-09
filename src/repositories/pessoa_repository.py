from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pessoa_model import Pessoa
from schemas.pessoa_schema import PessoaCreate, PessoaResponse, PessoaUpdate
from services.permissoes import exigir_cargo_admin


class PessoaRepository:
    def __init__(self, session: Session):
        self.session = session

    def registar_pessoa(self, pessoa: PessoaCreate) -> Pessoa:
        if self.obter_por_cc(pessoa.cc) is not None:
            raise ValueError("Pessoa já está registada")
        model = Pessoa(**pessoa.model_dump())
        self.session.add(model)
        return model

    def obter_por_cc(self, cc: str) -> Pessoa | None:
        comando = select(Pessoa).where(Pessoa.cc == cc)
        return self.session.scalars(comando).one_or_none()

    def iniciar_sessao(self, cc: str, password: str) -> Pessoa | None:
        comando = select(Pessoa).where(Pessoa.cc == cc, Pessoa.password == password)
        return self.session.scalars(comando).one_or_none()

    def ver_se_votou(self, pessoa: Pessoa) -> bool:
        if pessoa.votou:
            return True
        return False

    def editar_pessoa(self, update: PessoaUpdate, pessoa_cc: str) -> Pessoa:
        pessoa = self.obter_por_cc(pessoa_cc)
        if not pessoa:
            raise ValueError("Não existe pessoa com esse cc")

        for chave, valor in update.model_dump().items():
            setattr(pessoa, chave, valor)

        return pessoa

    def apagar_pessoa(self, pessoa_cc: str):
        pessoa = self.obter_por_cc(pessoa_cc)

        if not pessoa:
            raise ValueError("Não existe pessoa com esse cc")

        self.session.delete(pessoa)