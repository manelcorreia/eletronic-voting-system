import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from api.exceptions import UrnaFechada, UrnaNaoEncontrada, PermissaoError, UrnasAbertas, OperacaoNaoPermitida, \
    CandidatoNaoEncontrado, PessoaNaoEncontrada, CandidaturaNaoEncontrada, CandidaturaJaExiste, JaVotou, \
    CandidatoJaExiste, PessoaJaRegistada, UrnaJaExiste
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

@app.exception_handler(UrnasAbertas)
def urnas_ainda_abertas(request: Request, exc: UrnasAbertas):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(OperacaoNaoPermitida)
def operacao_nao_permitida(request: Request, exc: OperacaoNaoPermitida):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(CandidatoNaoEncontrado)
def candidato_nao_encontrado(request: Request, exc: CandidatoNaoEncontrado):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(PessoaNaoEncontrada)
def pessoa_nao_encontrada(request: Request, exc: PessoaNaoEncontrada):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(CandidaturaNaoEncontrada)
def candidatura_nao_encontrada(request: Request, exc: CandidaturaNaoEncontrada):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(CandidaturaJaExiste)
def candidatura_ja_existe(request: Request, exc: CandidaturaJaExiste):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(JaVotou)
def ja_votou(request: Request, exc: JaVotou):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(CandidatoJaExiste)
def candidato_ja_existe(request: Request, exc: CandidatoJaExiste):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(PessoaJaRegistada)
def pessoa_ja_registada(request: Request, exc: PessoaJaRegistada):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(UrnaJaExiste)
def urna_ja_existe(request: Request, exc: UrnaJaExiste):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)