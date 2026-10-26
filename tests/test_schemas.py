from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from schemas import UrnaResponse, UrnaComDetalhe
from schemas.candidato_schema import CandidatoCreate, CandidatoUpdate, CandidatoResponse, CandidatoDetalhe
from schemas.candidatura_schema import CandidaturaCreate, CandidaturaResponse
from schemas.pessoa_schema import PessoaCreate, PessoaUpdate, PessoaResponse
from schemas.urna_schema import UrnaCreate, UrnaUpdate

VALIDO_PESSOA = dict(nome="test", cc="12345678", urna_id=1, password="Abcvdfjfa1#")
VALIDO_CANDIDATO = dict(nome="test")
VALIDO_URNA = dict(localidade="test")
VALIDO_CANDIDATURA = dict(urna_id=1,candidato_id=1)

def test_create_pessoa_valido():
    pessoa = PessoaCreate(**VALIDO_PESSOA)

    assert pessoa is not None
    assert pessoa.nome == "test"
    assert pessoa.cc == "12345678"
    assert pessoa.urna_id == 1
    assert pessoa.password == "Abcvdfjfa1#"

@pytest.mark.parametrize("campo, valor", [
    ("nome", "te"),
    ("nome", "Ana1"),
    ("cc", "1234567"),
    ("cc", "1234567a"),
    ("password", "Abcdefgh#"),   # sem número
    ("password", "abcdefg1#"),   # sem maiúscula
    ("password", "Abcdefg12"),   # sem caractere especial
    ("password", "Ab1#"),        # curta
])
def test_create_pessoa_invalido(campo, valor):
    with pytest.raises(ValidationError):
        PessoaCreate(**{**VALIDO_PESSOA, campo: valor})

def test_update_pessoa_completo():
    pessoa = PessoaUpdate(nome="test", cc="12345678", urna_id=1, password="Abcvdfjfa1#")

    assert pessoa is not None
    assert pessoa.nome == "test"
    assert pessoa.cc == "12345678"
    assert pessoa.urna_id == 1
    assert pessoa.password == "Abcvdfjfa1#"

def test_update_pessoa_invalido():
    with pytest.raises(ValidationError):
        PessoaUpdate(nome="te", cc="1234567", urna_id=1, password="abcvdfjfa")

def test_update_pessoa_incompleto():
    dados = {"nome": None, "cc": None, "urna_id": None, "votou": True, "password": None}

    pessoa = PessoaUpdate(**dados)

    assert pessoa is not None
    assert pessoa.nome is None
    assert pessoa.cc is None
    assert pessoa.urna_id is None
    assert pessoa.password is None
    assert pessoa.votou is True

def test_update_pessoa_exclude_unset():
    dados = {"votou": True}

    pessoa = PessoaUpdate(**dados)
    update = PessoaUpdate.model_dump(pessoa)

    assert pessoa is not None
    assert update == {"nome": None, "cc": None, "urna_id": None, "votou": True, "password": None}

    campos_exclude = pessoa.model_dump(exclude_unset=True)

    assert campos_exclude == {"votou": True}

def test_response_a_partir_de_objeto():
    obj = SimpleNamespace(id=1, nome="test", cc="12345678", urna_id=1, password="Abcvdfjfa1#")

    schema = PessoaResponse.model_validate(obj)
    assert schema is not None
    assert schema.nome == "test"
    assert schema.cc == "12345678"
    assert schema.urna_id == 1
    assert schema.votou is False
    assert schema.id == obj.id

def test_create_candidato_valido():
    candidato = CandidatoCreate(**VALIDO_CANDIDATO)

    assert candidato is not None
    assert candidato.nome == "test"

@pytest.mark.parametrize("campo, valor", [
    ("nome", "te"),
    ("nome", "test3"),
])
def test_create_candidato_invalido(campo, valor):
    with pytest.raises(ValidationError):
        PessoaCreate(**{**VALIDO_CANDIDATO, campo: valor})

def test_update_candidato_valido():
    candidato = CandidatoUpdate(**VALIDO_CANDIDATO)

    assert candidato is not None
    assert candidato.nome == "test"

@pytest.mark.parametrize("campo, valor", [
    ("nome", "te"),
    ("nome", "test3"),
])
def test_update_candidato_invalido(campo, valor):
    with pytest.raises(ValidationError):
        CandidatoUpdate(**{**VALIDO_CANDIDATO, campo: valor})

def test_update_candidato_vazio():
    candidato = CandidatoUpdate()

    assert candidato is not None
    assert candidato.nome is None

def test_response_candidato_a_partir_de_objeto():
    obj = SimpleNamespace(id=1, nome="test")

    schema = CandidatoResponse.model_validate(obj)

    assert schema is not None
    assert schema.nome == "test"
    assert schema.id == obj.id

def test_candidato_com_detalhe():
    obj = SimpleNamespace(id=1, nome="test", candidaturas=[
        SimpleNamespace(urna_id=1,candidato_id=1,votos=1,urna=SimpleNamespace(id=1,localidade="test")),
        SimpleNamespace(urna_id=2, candidato_id=1, votos=1, urna=SimpleNamespace(id=2, localidade="teste")),
    ])

    schema = CandidatoDetalhe.model_validate(obj)

    assert schema is not None
    assert len(schema.candidaturas) == 2

def test_create_urna_valida():
    urna = UrnaCreate(**VALIDO_URNA)

    assert urna is not None
    assert urna.localidade == "test"
    assert urna.fechada is False

@pytest.mark.parametrize("campo, valor", [
    ("localidade", "te"),
    ("localidade", "test3"),
])
def test_create_urna_invalido(campo, valor):
    with pytest.raises(ValidationError):
        UrnaCreate(**{**VALIDO_URNA, campo: valor})

def test_update_urna_completa():
    urna = UrnaUpdate(localidade="test", fechada=True)

    assert urna is not None
    assert urna.localidade == "test"
    assert urna.fechada is True

def test_update_urna_incompleta():
    urna = UrnaUpdate(fechada=True)

    assert urna is not None
    assert urna.localidade is None
    assert urna.fechada is True

@pytest.mark.parametrize("campo, valor", [
    ("localidade", "te"),
    ("localidade", "test3"),
])
def test_update_urna_invalida(campo, valor):
    with pytest.raises(ValidationError):
        UrnaUpdate(**{**VALIDO_URNA, campo: valor})

def test_update_urna_exclude_unset():
    dados = {"fechada":True}

    update = UrnaUpdate(**dados)

    assert update is not None
    assert update.fechada is True
    assert update.localidade is None

    exclude = update.model_dump(exclude_unset=True)

    assert exclude is not None
    assert exclude == {"fechada":True}

def test_update_urna_vazio():
    update = UrnaUpdate()

    assert update is not None
    assert update.localidade is None
    assert update.fechada is None

def test_response_urna_a_partir_de_objeto():
    obj = SimpleNamespace(id=1, localidade="test")

    urna = UrnaResponse.model_validate(obj)

    assert urna is not None
    assert urna.localidade == "test"
    assert urna.fechada is False
    assert urna.id == obj.id

def test_urna_com_detalhe():
    obj = SimpleNamespace(id=1, localidade="test", candidaturas=[
        SimpleNamespace(urna_id=1, candidato_id=1,votos=1,candidato=SimpleNamespace(id=1,nome="test")),
        SimpleNamespace(urna_id=1, candidato_id=2,votos=1,candidato=SimpleNamespace(id=2,nome="test")),
    ])

    com_detalhe = UrnaComDetalhe.model_validate(obj)

    assert com_detalhe is not None
    assert len(com_detalhe.candidaturas) == 2

def test_create_candidatura_valida():
    candidatura = CandidaturaCreate(**VALIDO_CANDIDATURA)

    assert candidatura is not None
    assert candidatura.urna_id == 1
    assert candidatura.candidato_id == 1

def test_response_candidatura_a_partir_de_objeto():
    obj = SimpleNamespace(urna_id=1, candidato_id=1, votos=1)

    candidatura = CandidaturaResponse.model_validate(obj)

    assert candidatura is not None
    assert candidatura.urna_id == obj.urna_id
    assert candidatura.votos == 1
    assert candidatura.candidato_id == obj.candidato_id