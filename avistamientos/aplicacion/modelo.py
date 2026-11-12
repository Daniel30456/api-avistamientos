from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Avistamiento:
    especie: str
    lugar: str
    fecha: str          # texto AAAA-MM-DD, ya validado
    observador: str
    id: Optional[int] = None   # lo asigna el repositorio al guardar


@dataclass(frozen=True)
class ConteoPorEspecie:
    especie: str
    cantidad: int
