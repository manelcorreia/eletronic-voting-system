from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.dependencies import UrnaServiceDep
from schemas import UrnaResponse
from schemas.pessoa_schema import PessoaResponse
from schemas.urna_schema import UrnaCreate, UrnaUpdate

router = APIRouter(prefix="/urnas", tags=["urnas"])

@router.post("/nova_urna", response_model=UrnaResponse, status_code=HTTP_201_CREATED)
def adicionar_nova_urna(pessoa: PessoaResponse, urna: UrnaCreate, service: UrnaServiceDep) -> UrnaResponse:
    return service.criar_urna(pessoa, urna)

@router.patch("/fechar_urna/{urna_id}", status_code=HTTP_200_OK)
def fechar_urna(pessoa: PessoaResponse, urna_id: int, service: UrnaServiceDep):
    return service.fechar_urna(pessoa, urna_id)

@router.get("/lista_urnas", response_model=list[UrnaResponse], status_code=HTTP_200_OK)
def lista_urnas(service: UrnaServiceDep) -> list[UrnaResponse]:
    return service.mostrar_todas_urnas()

@router.get("/{urna_id}", response_model=UrnaResponse, status_code=HTTP_200_OK)
def obter_urna_por_id(urna_id: int, service: UrnaServiceDep) -> UrnaResponse:
    return service.obter_urna_por_id(urna_id)

@router.get("/taxa_abstencao/{urna_id}", response_model=float, status_code=HTTP_200_OK)
def ver_taxa_abstencao(urna_id: int, service: UrnaServiceDep) -> float:
    return service.ver_abstencao(urna_id)

@router.get("/nao_votantes/{urna_id}", response_model=int, status_code=HTTP_200_OK)
def ver_numero_nao_votantes(urna_id: int, service: UrnaServiceDep) -> int:
    return service.ver_quantos_nao_votaram(urna_id)

@router.get("/votantes/{urna_id}", response_model=int, status_code=HTTP_200_OK)
def ver_numero_votantes(urna_id: int, service: UrnaServiceDep) -> int:
    return service.ver_quantos_votaram(urna_id)

@router.patch("/updates/urna/{urna_id}", response_model=UrnaResponse, status_code=HTTP_200_OK)
def editar_urna(pessoa: PessoaResponse, update: UrnaUpdate, urna_id: int, service: UrnaServiceDep) -> UrnaResponse:
    return service.editar_urna(pessoa, update, urna_id)

@router.delete("/apagar/urna", status_code=HTTP_204_NO_CONTENT)
def apagar_urna(pessoa: PessoaResponse, urna_id: int, service: UrnaServiceDep):
    return service.apagar_urna(pessoa, urna_id)

@router.get("/votos/partidos/urna_{urna_id}", response_model=dict, status_code=HTTP_200_OK)
def ver_votos_partido(pessoa: PessoaResponse, urna_id: int, service: UrnaServiceDep) -> dict:
    return service.votos_por_partido(pessoa, urna_id)

@router.get("/votos/partido_{partido}/urna_{urna_id}", response_model=int, status_code=HTTP_200_OK)
def ver_votos_na_urna_partido_especifico(pessoa: PessoaResponse, partido: str, urna_id: int, service: UrnaServiceDep) -> int:
    return service.votos_partido_na_urna(pessoa, partido, urna_id)

@router.get("/percentagem_votos_partidos/urna_{urna_id}", response_model=dict, status_code=HTTP_200_OK)
def ver_percentagem_votos_partidos_na_urna(pessoa: PessoaResponse, urna_id: int, service: UrnaServiceDep) -> dict:
    return service.percentagem_partido_urna(pessoa, urna_id)