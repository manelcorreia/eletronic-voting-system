from sqlalchemy.orm import Session

from api.exceptions import UrnaFechada, UrnasAbertas, OperacaoNaoPermitida, CandidatoJaExiste, CandidatoNaoEncontrado
from repositories.candidato_repository import CandidatoRepository
from repositories.candidatura_repository import CandidaturaRepository
from repositories.urna_repository import UrnaRepository
from schemas.candidato_schema import CandidatoCreate, CandidatoResponse, CandidatoUpdate
from schemas.candidatura_schema import CandidaturaCreate
from schemas.pessoa_schema import PessoaResponse
from services.permissoes import exigir_cargo_admin, exigir_cargo_admin_ou_responsavel


class CandidatoService:
    def __init__(self, session: Session, repository: CandidatoRepository, urnas_repository: UrnaRepository, candidatura_repository: CandidaturaRepository):
        self.session = session
        self.repository = repository
        self.urnas_repository = urnas_repository
        self.candidatura_repository = candidatura_repository

    def criar_candidato(self, pessoa: PessoaResponse, candidato: CandidatoCreate) -> CandidatoResponse:
        exigir_cargo_admin_ou_responsavel(pessoa)
        try:
            if self.repository.obter_por_nome(candidato.nome):
                raise CandidatoJaExiste("Candidato ja existe com esse nome")

            model = self.repository.adicionar(candidato)
            self.session.flush()

            for urna in self.urnas_repository.listar_urnas():
                self.candidatura_repository.adicionar_candidatura(
                    CandidaturaCreate(urna_id=urna.id, candidato_id=model.id),
                )

            self.session.commit()
            self.session.refresh(model)
            schema = CandidatoResponse.model_validate(model)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def contar_votos_candidato(self, candidato_nome: str) -> int:
        if any(not urna.fechada for urna in self.urnas_repository.listar_urnas()):
            raise UrnasAbertas("Os resultados só ficam disponíveis quando todas as urnas estiverem fechadas")
        if self.repository.obter_por_nome(candidato_nome) is None:
            raise CandidatoNaoEncontrado("Candidato com esse nome não existe")
        return self.repository.total_votos_candidato(candidato_nome)

    def listar_candidatos(self) -> list[CandidatoResponse]:
        lista_candidatos = []
        candidatos = self.repository.listar_candidatos()
        for candidato in candidatos:
            schema = CandidatoResponse.model_validate(candidato)
            lista_candidatos.append(schema)
        return lista_candidatos

    def editar_candidato(self, pessoa: PessoaResponse, candidato_update: CandidatoUpdate, candidato_id) -> CandidatoResponse:
        exigir_cargo_admin(pessoa)
        try:
            if self.repository.obter_por_id(candidato_id) is None:
                raise CandidatoNaoEncontrado("Não existe nenhum candidato com esse id")
            candidato = self.repository.dar_update(candidato_update, candidato_id)
            self.session.commit()
            self.session.refresh(candidato)
            schema = CandidatoResponse.model_validate(candidato)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def apagar_candidato(self, pessoa: PessoaResponse, candidato_id: int):
        exigir_cargo_admin(pessoa)
        candidato = self.repository.obter_por_id(candidato_id)
        if candidato is None:
            raise CandidatoNaoEncontrado("Não existe candidato com esse id")

        if candidato.total_votos > 0:
            raise OperacaoNaoPermitida("Não pode apagar um candidato com votos")

        try:
            self.repository.apagar_candidato(candidato_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise