from typing import Iterable

from models.candidato_model import Candidato
from models.pessoa_model import Pessoa


class GravadorFicheiro:
    @staticmethod
    def guardar_ficheiro_pessoas(dados: Iterable[Pessoa], ficheiro_saida: str = "recenseamento.csv"):
        with open(ficheiro_saida, "w", encoding="utf-8") as f:
            f.write("nome,cc,localidade,votou\n")

            for pessoa in dados:
                linha = f"{pessoa.nome},{pessoa.cc},{pessoa.localidade},{pessoa.votou}\n"
                f.write(linha)

    @staticmethod
    def guardar_ficheiro_candidato(dados: Iterable[Candidato], ficheiro_saida: str = "candidatos.csv"):
        with open(ficheiro_saida, "w", encoding="utf-8") as f:
            f.write("nome,votos\n")

            for candidato in dados:
                linha = f"{candidato.nome},{candidato.votos}\n"
                f.write(linha)