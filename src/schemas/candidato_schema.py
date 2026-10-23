from typing import TYPE_CHECKING
from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from schemas.candidatura_schema import CandidaturaComUrna

class CandidatoBaseModel(BaseModel):
    nome: str = Field(min_length=3, max_length=120)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if any(l.isdigit() for l in valor):
            raise ValueError("nome deve conter apenas letras")
        return valor

class CandidatoCreate(CandidatoBaseModel):
    pass

class CandidatoUpdate(CandidatoBaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=120)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if valor is None:
            return None
        if any(l.isdigit() for l in valor):
            raise ValueError("nome deve conter apenas letras")
        return valor

class CandidatoResponse(CandidatoBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CandidatoDetalhe(CandidaturaComUrna):
    urnas: list["CandidaturaComUrna"]