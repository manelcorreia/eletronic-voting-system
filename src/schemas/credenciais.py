from pydantic import BaseModel


class Credenciais(BaseModel):
    cc: str
    password: str