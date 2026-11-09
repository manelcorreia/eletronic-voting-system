from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from api.dependencies import UrnaServiceDep
from schemas import UrnaResponse
from schemas.pessoa_schema import PessoaResponse
from schemas.urna_schema import UrnaCreate

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