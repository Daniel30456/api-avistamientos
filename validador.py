import re
from datetime import date, datetime


class RelojSistema:
    def hoy(self):
        return date.today()


class ValidadorDeAvistamiento:
    def __init__(self, reloj=None):
        self.reloj = reloj or RelojSistema()

    def validar(self, datos):
        """Devuelve un mensaje con el campo que falló, o None si es válido."""
        if not isinstance(datos, dict):
            return "El cuerpo debe ser un objeto JSON"
        for campo in ("especie", "lugar", "fecha", "observador"):
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