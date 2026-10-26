import string

from pydantic import BaseModel, field_validator, Field, model_validator, ConfigDict


class PessoaBaseModel(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    cc: str = Field(min_length=8)
    urna_id: int
    votou: bool = Field(default=False)

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, valor):
        if any(l.isdigit() for l in valor):
            raise ValueError("Nome não pode ter números")
        return valor

    @field_validator('cc')
    @classmethod
    def validar_cc(cls, valor):
        if len(valor) != 8 or not valor.isdigit():
            raise ValueError("CC tem de ter sempre 8 dígitos")
        return valor

class PessoaCreate(PessoaBaseModel):
    password: str = Field(min_length=8)

    @field_validator('password')
    @classmethod
    def validar_password(cls, valor):
        if len(valor) < 8:
            raise ValueError("Password tem de ter pelo menos 8 dígitos")

        if not any(l.isdigit() for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 número")

        if not any(l.isupper() for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 letra maiúscula")

        if not any(l in string.punctuation for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 caractere especial")

        return valor

class PessoaUpdate(PessoaBaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=120)
    cc: str | None = Field(default=None, min_length=8)
    urna_id: int | None = None
    votou: bool | None = None
    password: str | None = Field(default=None, min_length=8)

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, valor):
        if valor is None:
            return None

        if any(l.isdigit() for l in valor):
            raise ValueError("Nome não pode ter números")
        return valor

    @field_validator("cc")
    @classmethod
    def validar_cc(cls, valor):
        if valor is None:
            return None
        if len(valor) != 8 or not valor.isdigit():
            raise ValueError("CC tem de ter sempre 8 dígitos")
        return valor

    @field_validator('password')
    @classmethod
    def validar_password(cls, valor):
        if valor is None:
            return None

        if len(valor) < 8:
            raise ValueError("Password tem de ter pelo menos 8 dígitos")

        if not any(l.isdigit() for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 número")

        if not any(l.isupper() for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 letra maiúscula")

        if not any(l in string.punctuation for l in valor):
            raise ValueError("Password tem de ter pelo menos 1 caractere especial")

        return valor

class PessoaResponse(PessoaBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int