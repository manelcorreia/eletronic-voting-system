import pandas as pd
import os

class Pessoa:
    def __init__(self, nome, cc):
        self.nome = nome
        self.cc = cc

    def para_dict(self):
        return {
            "nome": self.nome,
            "cc": self.cc
        }

class Candidato:
    def __init__(self, nome):
        self.nome = nome
        self.votos = 0

    def receber_votos(self):
        self.votos += 1

    def __str__(self):
        return f"nome: {self.nome}: {self.votos} votos"

    def to_dict(self):
            return {
                "nome": self.nome,
                "votos": self.votos
            }

class Urna:
    def __init__(self):
        self.lista_candidatos = []

    def adicionar_candidato(self, candidato):
        self.lista_candidatos.append(candidato)

    def votar(self, nome_candidato):
        nome_voto_limpo = nome_candidato.strip().title()

        # é voto em branco? (pessoa deu enter sem escrever nada)
        if nome_voto_limpo == "":
            for candidato in self.lista_candidatos:
                if candidato.nome == "Em Branco":
                    candidato.receber_votos()
                    return True, "Voto em branco registado com sucesso."

        # é um voto válido? (procura na lista de candidatos)
        for candidato in self.lista_candidatos:
            if candidato.nome == nome_voto_limpo:
                    candidato.receber_votos()
                    return True, f"Voto registado com sucesso no candidato {candidato.nome}!"

        # se chegou aqui, é um voto nulo (não encontrou nenhum candidato no ciclo acima)
        for candidato in self.lista_candidatos:
            if candidato.nome == "Nulo":
                candidato.receber_votos()
                return False, f"Candidato '{nome_candidato}' não existe no boletim. Voto considerado NULO."

        return False, "Erro crítico!"

    def mostrar_resultados(self):
        return self.lista_candidatos

    def to_csv(self, nome_ficheiro):
        lista_dict = []
        for c in self.lista_candidatos:
            lista_dict.append(c.to_dict())

        df = pd.DataFrame(lista_dict)

        df = df.groupby('nome', as_index=False).sum()

        df.to_csv(nome_ficheiro, index=False, header=True)

    def carregar_csv(self, nome_ficheiro):
        if os.path.exists(nome_ficheiro):
            df = pd.read_csv(nome_ficheiro)
            for _, linha in df.iterrows():
                candidato = Candidato(linha['nome'])
                candidato.votos = linha['votos']
                self.adicionar_candidato(candidato)
        else:
            # Se for a 1ª vez que o programa corre (não há ficheiro), cria por defeito
            self.adicionar_candidato(Candidato("André Ventura"))
            self.adicionar_candidato(Candidato("António José Seguro"))
            self.adicionar_candidato(Candidato("António Filipe"))
            self.adicionar_candidato(Candidato("Cotrim"))
            self.adicionar_candidato(Candidato("Em Branco"))
            self.adicionar_candidato(Candidato("Nulo"))

class Caderneta:
    def __init__(self):
        self.votantes = []

    def adicionar_votante(self, votante):
        self.votantes.append(votante)

    def pessoa_to_csv(self, nome_ficheiro):
        lista_dicionario = []
        for v in self.votantes:
            lista_dicionario.append(v.para_dict())

        df = pd.DataFrame(lista_dicionario)

        df.to_csv(nome_ficheiro, index=False, header=True)

    def verificar_cc(self, pessoa_cc):
        for cc in self.votantes:
            if cc.cc == pessoa_cc:
                return True   # sim já votou
        return False     # não votou

    def mostrar_votantes(self):
        return self.votantes

    def carregar_csv(self, nome_ficheiro):
        if os.path.exists(nome_ficheiro):
            df = pd.read_csv(nome_ficheiro)
            for _, linha in df.iterrows():
                pessoa = Pessoa(linha['nome'], linha['cc'])
                self.adicionar_votante(pessoa)

class Recenseamento:
    def __init__(self):
        self.eleitores = []

    def adicionar_eleitor(self, eleitor):
        self.eleitores.append(eleitor)

    def carregar_csv(self, nome_ficheiro):
        if os.path.exists(nome_ficheiro):
            df = pd.read_csv(nome_ficheiro)
            for _, linha in df.iterrows():
                eleitor = Pessoa(linha['nome'], linha['cc'])
                self.adicionar_eleitor(eleitor)

    def verificar_cc(self, pessoa_cc):
        for cc in self.eleitores:
            if cc.cc == pessoa_cc:
                return True   # sim faz parte
        return False     # não faz parte

    def mostrar_eleitores(self):
        return self.eleitores