from datetime import date

from avistamientos.aplicacion.puertos.secundarios import Reloj


class RelojSistema(Reloj):
    """Adaptador del puerto Reloj que usa la fecha real del sistema operativo."""

    def hoy(self):
        return date.today()
