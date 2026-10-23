from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models.base import Base

if TYPE_CHECKING:
    from models.candidatura_model import Candidatura

class Candidato(Base):
    __tablename__ = 'candidatos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))

    candidaturas: Mapped[list["Candidatura"]] = relationship(back_populates="candidato", cascade="all, delete-orphan", lazy="selectin")

    @property
    def total_votos(self) -> int:
        return sum(c.votos for c in self.candidaturas)