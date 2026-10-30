from repositories.candidatura_repository import CandidaturaRepository
from schemas.candidatura_schema import CandidaturaCreate, CandidaturaResponse


class CandidaturaService:
    def __init__(self, session, repository: CandidaturaRepository):
        self.session = session
        self.repository = repository

    def criar_candidatura(self, candidatura: CandidaturaCreate) -> CandidaturaResponse:
        try:
            candidatura = self.repository.adicionar_candidatura(candidatura)
            self.session.commit()
            self.session.refresh(candidatura)
            schema = CandidaturaResponse.model_validate(candidatura)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def adicionar_voto_a_candidatura(self, pessoa_cc: str, candidato_id: int):
        try:
            self.repository.voto(pessoa_cc, candidato_id)
        except Exception:
            self.session.rollback()
            raise