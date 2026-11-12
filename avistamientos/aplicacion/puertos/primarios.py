"""Puerto primario (driving): lo que la aplicación ofrece hacia afuera.

Cualquier adaptador primario (el de HTTP con Flask, una prueba, un script por lotes)
maneja la aplicación solo a través de estos métodos. Los datos entran como
diccionarios simples y salen como objetos del modelo, sin tipos de ningún framework."""
from abc import ABC, abstractmethod
from typing import List

from avistamientos.aplicacion.modelo import Avistamiento, ConteoPorEspecie


class GestionDeAvistamientos(ABC):
    @abstractmethod
    def listar(self) -> List[Avistamiento]:
        ...

    @abstractmethod
    def obtener(self, id_: int) -> Avistamiento:
        """Lanza AvistamientoNoEncontrado si no existe."""

    @abstractmethod
    def registrar(self, datos) -> Avistamiento:
        """Lanza DatosInvalidos si los datos no cumplen la regla."""

    @abstractmethod
    def actualizar(self, id_: int, datos) -> Avistamiento:
        """Lanza AvistamientoNoEncontrado o DatosInvalidos, en ese orden de revisión."""

    @abstractmethod
    def eliminar(self, id_: int) -> None:
        """Lanza AvistamientoNoEncontrado si no existe."""

    @abstractmethod
    def resumen(self) -> List[ConteoPorEspecie]:
        """Cantidad por especie, de mayor a menor y luego por nombre."""
