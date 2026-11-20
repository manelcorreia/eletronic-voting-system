from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from core.engine import SessionLocal
from repositories.candidato_repository import CandidatoRepository
from repositories.candidatura_repository import CandidaturaRepository
from repositories.pessoa_repository import PessoaRepository
from repositories.urna_repository import UrnaRepository
from services.candidato_service import CandidatoService
from services.candidatura_service import CandidaturaService
from services.pessoa_service import PessoaService
from services.urna_service import UrnaService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]

def get_candidato_service(db: DbSession) -> CandidatoService:
    repo = CandidatoRepository(db)
    repo_urna = UrnaRepository(db)
    repo_candidatura = CandidaturaRepository(db)
    return CandidatoService(db, repo, repo_urna, repo_candidatura)

CandidatoServiceDep = Annotated[CandidatoService, Depends(get_candidato_service)]

def get_candidatura_service(db: DbSession) -> CandidaturaService:
    repo = CandidaturaRepository(db)
    repo_pessoas = PessoaRepository(db)
    return CandidaturaService(db, repo, repo_pessoas)

CandidaturaServiceDep = Annotated[CandidaturaService, Depends(get_candidatura_service)]

def get_pessoa_service(db: DbSession) -> PessoaService:
    repo = PessoaRepository(db)
    return PessoaService(db, repo)

PessoaServiceDep = Annotated[PessoaService, Depends(get_pessoa_service)]

def get_urna_service(db: DbSession) -> UrnaService:
    repo = UrnaRepository(db)
    repo_candidatura = CandidaturaRepository(db)
    repo_candidato = CandidatoRepository(db)
    repo_pessoa = PessoaRepository(db)
    return UrnaService(db, repo, repo_candidatura, repo_candidato, repo_pessoa)

UrnaServiceDep = Annotated[UrnaService, Depends(get_urna_service)]