from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from api.dependencies import CandidaturaServiceDep
from schemas.candidatura_schema import CandidaturaResponse, CandidaturaCreate
from schemas.pessoa_schema import PessoaResponse

router = APIRouter(prefix="/candidaturas", tags=["candidaturas"])

@router.post("/nova_candidatura", response_model=CandidaturaResponse, status_code=HTTP_201_CREATED)
def adicionar_nova_candidatura(candidatura: CandidaturaCreate, service: CandidaturaServiceDep) -> CandidaturaResponse:
    return service.criar_candidatura(candidatura)

@router.get("/voto", status_code=HTTP_200_OK)
def votar(pessoa: PessoaResponse, candidato_id: int, service: CandidaturaServiceDep):
    return service.votar(pessoa, candidato_id)

@router.get("/total_votos_em_urna", response_model=int, status_code=HTTP_200_OK)
def ver_total_votos_em_urna(urna_id: int, service: CandidaturaServiceDep) -> int:
    return service.ver_votos_totais_urna(urna_id)