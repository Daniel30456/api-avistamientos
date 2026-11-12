from avistamientos.aplicacion.puertos.secundarios import Reloj


class RelojFijo(Reloj):
    """Adaptador de prueba para el puerto Reloj: siempre devuelve la misma fecha."""

    def __init__(self, fecha):
        self._fecha = fecha

    def hoy(self):
        return self._fecha
