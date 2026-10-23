from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from models.base import Base

if TYPE_CHECKING:
    from models.urna_model import Urna

class Pessoa(Base):
    __tablename__ = 'pessoas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    cc: Mapped[str] = mapped_column(String(8), unique=True)
    password: Mapped[str] = mapped_column(String(120))
    urna_id: Mapped[int] = mapped_column(ForeignKey("urnas.id", ondelete="CASCADE"))
    votou: Mapped[bool] = mapped_column(default=False)

    urna: Mapped["Urna"] = relationship(back_populates="pessoas")

    @property
    def localidade(self) -> str:
        return self.urna.localidade