import re
from datetime import datetime

from avistamientos.aplicacion.puertos.secundarios import Reloj

CAMPOS = ("especie", "lugar", "fecha", "observador")


class ValidadorDeAvistamiento:
    def __init__(self, reloj: Reloj):
        # El reloj llega por el puerto: el real lo pone la composición (app.py)
        # y las pruebas ponen RelojFijo. La aplicación no conoce a ninguno.
        self.reloj = reloj

    def validar(self, datos):
        """Devuelve un mensaje con el campo que falló, o None si es válido."""
        if not isinstance(datos, dict):
            return "El cuerpo debe ser un objeto JSON"
        for campo in CAMPOS:
            valor = datos.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                return f"{campo}: es obligatorio y no puede estar vacío"

        if not 3 <= len(datos["especie"].strip()) <= 50:
            return "especie: debe tener entre 3 y 50 caracteres"

        fecha = datos["fecha"].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
            return "fecha: debe tener formato AAAA-MM-DD"
        try:
            f = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return "fecha: no es una fecha real"
        if f > self.reloj.hoy():
            return "fecha: no puede ser posterior a hoy"
        return None
