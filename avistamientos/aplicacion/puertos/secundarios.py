"""Puertos secundarios (driven): los define la aplicación y los implementan
adaptadores de afuera. Así la aplicación guarda datos o pregunta la fecha sin
saber si detrás hay SQLite, una lista en memoria, el reloj del sistema o uno fijo."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from avistamientos.aplicacion.modelo import Avistamiento


class RepositorioDeAvistamientos(ABC):
    @abstractmethod
    def listar(self) -> List[Avistamiento]:
        """Todos los avistamientos, ordenados por id."""

    @abstractmethod
    def buscar(self, id_: int) -> Optional[Avistamiento]:
        """El avistamiento con ese id, o None si no existe."""

    @abstractmethod
    def agregar(self, avistamiento: Avistamiento) -> Avistamiento:
        """Guarda uno nuevo y lo devuelve con el id asignado."""

    @abstractmethod
    def reemplazar(self, avistamiento: Avistamiento) -> Avistamiento:
        """Sobrescribe el avistamiento con el mismo id y lo devuelve."""

    @abstractmethod
    def eliminar(self, id_: int) -> None:
        """Borra el avistamiento con ese id."""


class Reloj(ABC):
    @abstractmethod
    def hoy(self) -> date:
        """La fecha de hoy, según quien implemente el puerto."""
