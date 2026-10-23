from pydantic import BaseModel, ConfigDict

from schemas.candidato_schema import CandidatoResponse
from schemas.urna_schema import UrnaResponse

class CandidaturaCreate(BaseModel):
    urna_id: int
    candidato_id: int

class CandidaturaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    urna_id: int
    candidato_id: int
    votos: int

class CandidaturaComUrna(CandidaturaResponse):
    urna: UrnaResponse

class CandidaturaComCandidato(CandidaturaResponse):
    candidato: CandidatoResponse