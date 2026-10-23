from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.pessoa_model import Pessoa
    from models.candidatura_model import Candidatura

class Urna(Base):
    __tablename__ = 'urnas'
    id: Mapped[int] = mapped_column(primary_key=True)
    localidade: Mapped[str] = mapped_column(String(120), unique=True)
    fechada: Mapped[bool] = mapped_column(default=False)

    pessoas: Mapped[list["Pessoa"]] = relationship(back_populates="urna", cascade="all, delete-orphan", lazy="selectin")
    candidaturas: Mapped[list["Candidatura"]] = relationship(back_populates="urna", cascade="all, delete-orphan", lazy="selectin")