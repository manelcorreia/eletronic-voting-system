from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.dependencies import CandidaturaServiceDep
from schemas.candidatura_schema import CandidaturaResponse, CandidaturaCreate
from schemas.pessoa_schema import PessoaResponse

router = APIRouter(prefix="/candidaturas", tags=["candidaturas"])

@router.post("/nova_candidatura", response_model=CandidaturaResponse, status_code=HTTP_201_CREATED)
def adicionar_nova_candidatura(pessoa: PessoaResponse, candidatura: CandidaturaCreate, service: CandidaturaServiceDep) -> CandidaturaResponse:
    return service.criar_candidatura(pessoa, candidatura)

@router.get("/voto", status_code=HTTP_200_OK)
def votar(pessoa: PessoaResponse, candidato_id: int, service: CandidaturaServiceDep):
    return service.votar(pessoa, candidato_id)

@router.get("/total_votos_em_urna", response_model=int, status_code=HTTP_200_OK)
def ver_total_votos_em_urna(pessoa: PessoaResponse, urna_id: int, service: CandidaturaServiceDep) -> int:
    return service.ver_votos_totais_urna(pessoa, urna_id)

@router.get("/lista_candidaturas", response_model=list[CandidaturaResponse], status_code=HTTP_200_OK)
def ver_lista_candidaturas(pessoa: PessoaResponse, service: CandidaturaServiceDep) -> list[CandidaturaResponse]:
    return service.ver_todas_candidaturas(pessoa)

@router.get("/candidatura/urna_{urna_id}/candidato_{candidato_id}", response_model=CandidaturaResponse, status_code=HTTP_200_OK)
def ver_candidatura_urna_candidato(pessoa: PessoaResponse, urna_id: int, candidato_id: int, service: CandidaturaServiceDep) -> CandidaturaResponse:
    return service.obter_candidatura_por_urna_candidato(pessoa, urna_id, candidato_id)

@router.delete("/apagar/candidatura", status_code=HTTP_204_NO_CONTENT)
def apagar_candidatura(pessoa: PessoaResponse, candidatura_id: int, service: CandidaturaServiceDep):
    return service.apagar_candidatura(pessoa, candidatura_id)

@router.get("/votos/partidos/geral", response_model=dict, status_code=HTTP_200_OK)
def ver_numero_votos_partidos_geral(pessoa: PessoaResponse, service: CandidaturaServiceDep) -> dict:
    return service.votos_por_partido_geral(pessoa)

@router.get("/percentagem_votos/partidos/geral", response_model=dict, status_code=HTTP_200_OK)
def ver_percentagem_votos_partidos_geral(pessoa: PessoaResponse, service: CandidaturaServiceDep):
    return service.percentagem_votos_partido_geral(pessoa)