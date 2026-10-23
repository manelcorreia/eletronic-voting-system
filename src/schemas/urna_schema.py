from typing import TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from schemas.candidatura_schema import CandidaturaComCandidato

class UrnaBaseModel(BaseModel):
    localidade: str = Field(min_length=3, max_length=120)
    fechada: bool = Field(default=False)

    @field_validator('localidade')
    @classmethod
    def validar_localidade(cls, valor):
        if any(l.isdigit() for l in valor):
            raise ValueError("Localidade não pode ter números")
        return valor

class UrnaCreate(UrnaBaseModel):
    pass

class UrnaUpdate(UrnaBaseModel):
    localidade: str | None = Field(default=None, min_length=3, max_length=120)
    fechada: bool | None = None

    @field_validator('localidade')
    @classmethod
    def validar_localidade(cls, valor):
        if valor is None:
            return None
        if any(l.isdigit() for l in valor):
            raise ValueError("Localidade não pode ter números")
        return valor

class UrnaResponse(UrnaBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UrnaComDetalhe(UrnaResponse):
    model_config = ConfigDict(from_attributes=True)
    candidaturas: list["CandidaturaComCandidato"]