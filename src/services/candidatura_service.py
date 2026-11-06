from repositories.candidatura_repository import CandidaturaRepository
from schemas.candidatura_schema import CandidaturaCreate, CandidaturaResponse
from schemas.pessoa_schema import PessoaResponse


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

    def votar(self, pessoa: PessoaResponse, candidato_id: int):
        try:
            self.repository.voto(pessoa.cc, candidato_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def ver_votos_totais_urna(self, urna_id: int) -> int:
        return self.repository.contar_votos_na_urna(urna_id)