from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from api.dependencies import PessoaServiceDep
from schemas import UrnaResponse
from schemas.credenciais import Credenciais
from schemas.pessoa_schema import PessoaResponse, PessoaCreate, PessoaUpdate

router = APIRouter(prefix="/pessoa", tags=["pessoa"])

@router.post("/nova_pessoa", response_model=PessoaResponse, status_code=HTTP_201_CREATED)
def adicionar_pessoa(pessoa_logada: PessoaResponse, pessoa: PessoaCreate, service: PessoaServiceDep) -> PessoaResponse:
    return service.criar_pessoa(pessoa_logada, pessoa)

@router.get("/inicio_sessao}", response_model=PessoaResponse, status_code=HTTP_200_OK)
def iniciar_sessao(credenciais: Credenciais, urna: UrnaResponse, service: PessoaServiceDep) -> PessoaResponse:
    return service.iniciar_sessao(credenciais.cc, credenciais.password, urna)

@router.get("/inicio_sessao/admin", response_model=PessoaResponse, status_code=HTTP_200_OK)
def iniciar_sessao_admin(credenciais: Credenciais, service: PessoaServiceDep) -> PessoaResponse:
    return service.iniciar_sessao_admin(credenciais)

@router.get("/confirmacao_responsavel", response_model=bool, status_code=HTTP_200_OK)
def confirmar_responsavel(credenciais: Credenciais, service: PessoaServiceDep) -> bool:
    return service.confirmar_responsavel(credenciais)

@router.patch("/editar/pessoa", response_model=PessoaResponse, status_code=HTTP_200_OK)
def editar_pessoa(pessoa_logada: PessoaResponse, update: PessoaUpdate, pessoa_cc: str, service: PessoaServiceDep) -> PessoaResponse:
    return service.editar_pessoa(pessoa_logada, update, pessoa_cc)

@router.delete("/apagar/pessoa", status_code=HTTP_204_NO_CONTENT)
def apagar_pessoa(pessoa_logada: PessoaResponse, pessoa_cc: str, service: PessoaServiceDep) -> PessoaResponse:
    return service.apagar_pessoa(pessoa_logada, pessoa_cc)