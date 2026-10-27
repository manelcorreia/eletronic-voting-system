from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pessoa_model import Pessoa
from schemas.pessoa_schema import PessoaCreate


class PessoaRepository:
    def __init__(self, session: Session):
        self.session = session

    def adicionar_pessoa(self, pessoa: PessoaCreate) -> Pessoa:
        if self.obter_por_cc(pessoa.cc) is not None:
            raise ValueError("Pessoa já está registada")
        model = Pessoa(**pessoa.model_dump())
        self.session.add(model)
        return model

    def obter_por_cc(self, cc: str) -> Pessoa | None:
        comando = select(Pessoa).where(Pessoa.cc == cc)
        return self.session.scalars(comando).one_or_none()