from typing import Generator

from models.pessoa_model import Pessoa


class LeitorPessoas:
    def __init__(self, ficheiro_entrada: str = "recenseamento.csv"):
        self.ficheiro_entrada = ficheiro_entrada

    def ler_ficheiro_pessoas(self) -> Generator[Pessoa, None, None]:
        with open(self.ficheiro_entrada, "r", encoding="utf-8") as f:
            next(f, None)

            for linha in f:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue

                colunas = linha_limpa.split(",")

                pessoa = Pessoa(colunas[0], colunas[1], colunas[2], bool(colunas[3]))

                yield pessoa