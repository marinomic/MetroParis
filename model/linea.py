from dataclasses import dataclass


@dataclass
class Linea:
    _id_linea: int
    _nome: str
    _velocita: int
    _intervallo: int
    _colore: str

    @property
    def id_linea(self):
        return self._id_linea

    @property
    def nome(self):
        return self._nome

    @property
    def velocita(self):
        return self._velocita

    @property
    def intervallo(self):
        return self._intervallo

    @property
    def colore(self):
        return self._colore

    def __hash__(self):
        return self._id_linea

    def __str__(self):
        return f"{self._nome}"
