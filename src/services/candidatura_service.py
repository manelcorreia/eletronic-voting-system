from repositories.candidatura_repository import CandidaturaRepository
from schemas.candidatura_schema import CandidaturaCreate, CandidaturaResponse
from schemas.pessoa_schema import PessoaResponse
from services.permissoes import exigir_cargo_admin, exigir_cargo_admin_ou_responsavel


class CandidaturaService:
    def __init__(self, session, repository: CandidaturaRepository):
        self.session = session
        self.repository = repository

    def criar_candidatura(self, pessoa: PessoaResponse, candidatura: CandidaturaCreate) -> CandidaturaResponse:
        exigir_cargo_admin(pessoa)
        try:
            candidatura = self.repository.adicionar_candidatura(candidatura)
            self.session.commit()
            self.session.refresh(candidatura)
            schema = CandidaturaResponse.model_validate(candidatura)
            return schema
        except Exception:
            self.session.rollback()
            raise

    def votar(self, pessoa: PessoaResponse, candidato_id: int):
        try:
            self.repository.voto(pessoa.cc, candidato_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def ver_votos_totais_urna(self, pessoa: PessoaResponse, urna_id: int) -> int:
        exigir_cargo_admin(pessoa)
        return self.repository.contar_votos_na_urna(urna_id)

    def ver_todas_candidaturas(self, pessoa: PessoaResponse) -> list[CandidaturaResponse]:
        exigir_cargo_admin_ou_responsavel(pessoa)
        candidaturas = self.repository.obter_candidaturas()
        schemas = []
        for candidatura in candidaturas:
            schemas.append(CandidaturaResponse.model_validate(candidatura))
        return schemas

    def obter_candidatura_por_urna_candidato(self, pessoa: PessoaResponse, urna_id: int, candidato_id: int) -> CandidaturaResponse:
        exigir_cargo_admin_ou_responsavel(pessoa)
        candidatura = self.repository.obter_candidatura_urna_candidato(urna_id, candidato_id)
        schema = CandidaturaResponse.model_validate(candidatura)
        return schema

    def apagar_candidatura(self, pessoa: PessoaResponse, candidatura_id: int):
        exigir_cargo_admin(pessoa)
        try:
            self.repository.apagar_candidatura(candidatura_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def votos_por_partido_geral(self, pessoa: PessoaResponse) -> dict[str, int]:
        exigir_cargo_admin(pessoa)
        return self.repository.votos_por_partido()

    def percentagem_votos_partido_geral(self, pessoa: PessoaResponse) -> dict[str, float]:
        exigir_cargo_admin(pessoa)
        dicionario_final: dict[str, float] = {}
        dicionario = self.repository.votos_por_partido()
        total_votos = sum(dicionario.values())

        if total_votos == 0:
            for chave in dicionario.keys():
                dicionario_final[chave] = 0.0

        for chave, valor in dicionario.items():
            dicionario_final[chave] = round((valor / total_votos) * 100, 2)

        return dicionario_final