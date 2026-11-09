from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.dependencies import CandidatoServiceDep
from schemas import CandidatoResponse
from schemas.candidato_schema import CandidatoCreate, CandidatoUpdate
from schemas.pessoa_schema import PessoaResponse

router = APIRouter(prefix="/candidatos", tags=["candidatos"])

@router.post("/novo_candidato", response_model=CandidatoResponse, status_code=HTTP_201_CREATED)
def adicionar_novo_candidato(pessoa: PessoaResponse, candidato: CandidatoCreate, service: CandidatoServiceDep) -> CandidatoResponse:
    return service.criar_candidato(pessoa, candidato)

@router.get("/votos/{candidato_nome", response_model=int, status_code=HTTP_200_OK)
def numero_votos_x_candidato(candidato_nome: str, service: CandidatoServiceDep) -> int:
    return service.contar_votos_candidato(candidato_nome)

@router.get("/lista_candidatos", response_model=list[CandidatoResponse], status_code=HTTP_200_OK)
def lista_candidatos(service: CandidatoServiceDep) -> list[CandidatoResponse]:
    return service.listar_candidatos()

@router.patch("/update/candidato/{candidato_id}", response_model=CandidatoResponse, status_code=HTTP_200_OK)
def editar_candidato(pessoa: PessoaResponse, candidato_update: CandidatoUpdate, candidato_id: int, service: CandidatoServiceDep) -> CandidatoResponse:
    return service.editar_candidato(pessoa, candidato_update, candidato_id)

@router.delete("/apagar/candidato", status_code=HTTP_204_NO_CONTENT)
def apagar_candidato(pessoa: PessoaResponse, candidato_id: int, service: CandidatoServiceDep):
    return service.apagar_candidato(pessoa, candidato_id)