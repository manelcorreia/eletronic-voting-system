from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.candidato_model import Candidato
    from models.urna_model import Urna

class Candidatura(Base):
    __tablename__ = 'candidaturas'
    urna_id: Mapped[int] = mapped_column(ForeignKey('urnas.id', ondelete='CASCADE'), primary_key=True)
    candidato_id: Mapped[int] = mapped_column(ForeignKey('candidatos.id', ondelete='CASCADE'), primary_key=True)

    votos: Mapped[int] = mapped_column(default=0)

    urna: Mapped["Urna"] = relationship(back_populates="candidaturas")
    candidato: Mapped["Candidato"] = relationship(back_populates="candidaturas")

