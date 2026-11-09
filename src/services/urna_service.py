from sqlalchemy.orm import Session

from repositories.candidato_repository import CandidatoRepository
from repositories.candidatura_repository import CandidaturaRepository
from repositories.pessoa_repository import PessoaRepository
from repositories.urna_repository import UrnaRepository
from schemas.candidatura_schema import CandidaturaCreate
from schemas.pessoa_schema import PessoaResponse
from schemas.urna_schema import UrnaCreate, UrnaResponse, UrnaUpdate
from services.permissoes import exigir_cargo_responsavel, exigir_cargo_admin


class UrnaService:
    def __init__(self, session: Session, repository: UrnaRepository, candidatura_repository: CandidaturaRepository, candidatos_repository: CandidatoRepository, pessoas_repository: PessoaRepository):
        self.session = session
        self.repository = repository
        self.candidatura_repository = candidatura_repository
        self.candidatos_repository = candidatos_repository
        self.pessoas_repository = pessoas_repository

    def criar_urna(self, pessoa: PessoaResponse, urna: UrnaCreate) -> UrnaResponse:
        exigir_cargo_admin(pessoa)
        try:
            model = self.repository.adicionar_urna(urna)
            self.session.flush()

            for candidato in self.candidatos_repository.listar_candidatos():
                self.candidatura_repository.adicionar_candidatura(
                    CandidaturaCreate(urna_id=model.id, candidato_id=candidato.id),
                )

            self.session.commit()
            self.session.refresh(model)
            schema = UrnaResponse.model_validate(model)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def fechar_urna(self, pessoa: PessoaResponse, urna_id: int):
        exigir_cargo_responsavel(pessoa)

        urna = self.repository.obter_urna_por_id(urna_id)
        if urna is None:
            raise ValueError("Não existe urna com esse ID")

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

    def obter_urna_por_id(self, urna_id: int) -> UrnaResponse:
        try:
            urna = self.repository.obter_urna_por_id(urna_id)
            return UrnaResponse.model_validate(urna)
        except Exception:
            raise

    def ver_abstencao(self, urna_id: int) -> float:
        total = 0
        total_nao_votantes = 0
        urna = self.repository.obter_urna_por_id(urna_id)

        for p in urna.pessoas:
            total += 1
            if not self.pessoas_repository.ver_se_votou(p):
                total_nao_votantes += 1

        return round(((total_nao_votantes * 100) / total), 2)

    def ver_quantos_votaram(self, urna_id: int) -> int:
        total = 0
        urna = self.repository.obter_urna_por_id(urna_id)

        for p in urna.pessoas:
            if self.pessoas_repository.ver_se_votou(p):
                total += 1

        return total

    def ver_quantos_nao_votaram(self, urna_id: int) -> int:
        total = 0
        urna = self.repository.obter_urna_por_id(urna_id)

        for p in urna.pessoas:
            if not self.pessoas_repository.ver_se_votou(p):
                total += 1

        return total

    def editar_urna(self, pessoa: PessoaResponse, update: UrnaUpdate, urna_id: int):
        exigir_cargo_admin(pessoa)
        try:
            self.repository.update_urna(update, urna_id)
            self.session.commit()
            self.session.refresh(update)
        except Exception:
            self.session.rollback()
            raise

    def apagar_urna(self, pessoa: PessoaResponse, urna_id: int):
        exigir_cargo_admin(pessoa)
        try:
            self.repository.apagar_urna(urna_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise