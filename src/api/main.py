import uvicorn
from fastapi import FastAPI
from api.routers.urna_router import router as urna_router
from api.routers.candidatura_router import router as candidatura_router
from api.routers.candidato_router import router as candidato_router
from api.routers.pessoa_router import router as pessoa_router

app = FastAPI(
    title="API Gestão de um sistema de votos eletrónico"
)

app.include_router(urna_router)
app.include_router(candidatura_router)
app.include_router(candidato_router)
app.include_router(pessoa_router)

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)