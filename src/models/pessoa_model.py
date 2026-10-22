from dataclasses import dataclass

@dataclass
class Pessoa:
    nome: str
    cc: str
    localidade: str
    votou: bool = False

    def __repr__(self):
        return f'Pessoa({self.nome}, {self.cc}, {self.localidade})'