from schemas import UrnaResponse
from schemas.pessoa_schema import PessoaResponse


class PermissaoError(Exception):
    pass

def exigir_cargo_responsavel(pessoa: PessoaResponse) -> None:
    if pessoa.cargo != "responsavel":
        raise PermissaoError("Só um responsável pode realizar essa ação!")

def exigir_cargo_admin(pessoa: PessoaResponse) -> None:
    if pessoa.cargo != "admin":
        raise PermissaoError("Só um admin pode realizar essa ação!")

def verificar_se_faz_parte_da_urna(pessoa: PessoaResponse, urna: UrnaResponse) -> None:
    if pessoa.urna_id != urna.id:
        raise PermissaoError("Não tem permissão para realizar esta ação nesta urna")