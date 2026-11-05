from sqlalchemy.orm import Session

from repositories.candidato_repository import CandidatoRepository
from repositories.urna_repository import UrnaRepository
from schemas.candidato_schema import CandidatoCreate, CandidatoResponse
from schemas.pessoa_schema import PessoaResponse
from services.permissoes import exigir_cargo_responsavel


class CandidatoService:
    def __init__(self, session: Session, repository: CandidatoRepository, urnas_repository: UrnaRepository):
        self.session = session
        self.repository = repository
        self.urnas_repository = urnas_repository

    def criar_candidato(self, pessoa: PessoaResponse, candidato: CandidatoCreate) -> CandidatoResponse:
        exigir_cargo_responsavel(pessoa)
        try:
            candidato = self.repository.adicionar(candidato)
            self.session.commit()
            self.session.refresh(candidato)
            schema = CandidatoResponse.model_validate(candidato)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def contar_votos_candidato(self, candidato_nome: str) -> int:
        urnas = self.urnas_repository.listar_urnas()

        for urna in urnas:
            if not urna.fechada:
                raise ValueError("A urna não está fechada.")

        try:
            votos = self.repository.total_votos_candidato(candidato_nome)
            return votos
        except Exception:
            raise

    def listar_candidatos(self) -> list[CandidatoResponse]:
        lista_candidatos = []
        candidatos = self.repository.listar_candidatos()
        for candidato in candidatos:
            schema = CandidatoResponse.model_validate(candidato)
            lista_candidatos.append(schema)
        return lista_candidatos