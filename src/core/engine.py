from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# carregar as variáveis do ficheiro .env para a memória do sistema
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("A variável de ambiente 'DATABASE_URL' não está definida")

# Parâmetros de produção
connect_args = {}
engine_kwargs = {
    # Testa se a conexão à base de dados continua viva antes de a entregar à sessão
    # (Evita o erro clássico 'MySQL server has gone away' quando a conexão fica inativa)
    "pool_pre_ping": True
}

# SQLite não suporta certos parâmetros de pool de servidores cliente-servidor
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Parâmetros essenciais para MySQL / PostgreSQL:
    engine_kwargs.update({
        "pool_size": 5,        # Mantém até 5 conexões sempre abertas no pool
        "max_overflow": 10,    # Permite criar até mais 10 conexões extra em picos de tráfego
        "pool_recycle": 1800,  # Recicla conexões a cada 30 minutos
    })

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)