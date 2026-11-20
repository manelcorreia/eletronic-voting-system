from api.exceptions import PermissaoError
from schemas import UrnaResponse
from schemas.pessoa_schema import PessoaResponse

def exigir_cargo_responsavel(pessoa: PessoaResponse) -> None:
    if pessoa.cargo != "responsavel":
        raise PermissaoError("Só um responsável pode realizar essa ação!")

def exigir_cargo_admin(pessoa: PessoaResponse) -> None:
    if pessoa.cargo != "admin":
        raise PermissaoError("Só um admin pode realizar essa ação!")

def verificar_se_faz_parte_da_urna(pessoa: PessoaResponse, urna: UrnaResponse) -> None:
    if pessoa.urna_id != urna.id:
        raise PermissaoError("Não tem permissão para realizar esta ação nesta urna")

def exigir_cargo_admin_ou_responsavel(pessoa: PessoaResponse) -> None:
    if pessoa.cargo not in ("admin", "responsavel"):
        raise PermissaoError("Não tem permissão para realizar esta ação")

def exigir_responsavel_admin_e_da_urna(pessoa: PessoaResponse, urna_id: int) -> None:
    if pessoa.cargo not in ("admin", "responsavel") and pessoa.urna_id != urna_id:
        raise PermissaoError("Não tem permissão para realizar esta ação")