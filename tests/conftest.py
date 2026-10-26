"""
Modelo de conftest.py para projetos com SQLAlchemy + padrão repositório.

Como usar num projeto novo:
  1. Copia este ficheiro para a raiz do projeto (ao lado dos testes).
  2. Muda só as 2 linhas marcadas com "MUDAR".
  3. Escreve os testes a pedir as fixtures `session` e `repo` como argumentos.
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from models.base import Base
  # MUDAR: o teu repositório


@pytest.fixture
def session():
    """Sessão ligada a uma BD SQLite em memória, nova para cada teste."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # O SQLite ignora chaves estrangeiras por defeito; isto faz com que as imponha
    # (como o PostgreSQL faz).
    @event.listens_for(engine, "connect")
    def _ativar_fks(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session      # o teste corre aqui
    engine.dispose()       # limpeza no fim


@pytest.fixture
def repo(session):
    """Repositório já ligado à sessão de teste."""
    return EscolaRepositorio(session)   # MUDAR: o teu repositório