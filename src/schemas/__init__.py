from schemas.urna_schema import UrnaResponse, UrnaComDetalhe
from schemas.candidato_schema import CandidatoResponse, CandidatoDetalhe
from schemas.candidatura_schema import CandidaturaComUrna, CandidaturaComCandidato

UrnaComDetalhe.model_rebuild()
CandidatoDetalhe.model_rebuild()