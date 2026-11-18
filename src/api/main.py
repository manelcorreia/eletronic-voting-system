import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from api.exceptions import UrnaFechada, UrnaNaoEncontrada, PermissaoError
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

@app.exception_handler(UrnaFechada)
def urna_esta_fechada(request: Request, exc: UrnaFechada):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(UrnaNaoEncontrada)
def urna_nao_encontrada(request: Request, exc: UrnaNaoEncontrada):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(PermissaoError)
def erro_de_permissao(request: Request, exc: PermissaoError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)