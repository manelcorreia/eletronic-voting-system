from sqlalchemy.orm import Session

from repositories.candidato_repository import CandidatoRepository
from schemas.candidato_schema import CandidatoCreate, CandidatoResponse


class CandidatoService:
    def __init__(self, session: Session, repository: CandidatoRepository):
        self.session = session
        self.repository = repository

    def criar_candidato(self, candidato: CandidatoCreate) -> CandidatoResponse:
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