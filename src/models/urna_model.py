from dataclasses import dataclass

@dataclass
class Urna:
    localidade: str
    fechada: bool = False

    def __repr__(self):
        return f"Urna({self.localidade})"