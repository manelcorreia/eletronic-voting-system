from typing import Generator

from models.candidato_model import Candidato


class LeitorCandidatos:
    def __init__(self, ficheiro_entrada: str = "candidatos.csv"):
        self.ficheiro_entrada = ficheiro_entrada

    def ler_ficheiro_candidatos(self) -> Generator[Candidato, None, None]:
        with open(self.ficheiro_entrada, "r", encoding="utf-8") as f:
            next(f, None)

            for linha in f:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue

                colunas = linha_limpa.split(",")

                candidato = Candidato(colunas[0], int(colunas[1]))

                yield candidato