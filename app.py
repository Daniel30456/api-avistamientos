"""Punto de arranque y composición (fuera del hexágono).

Aquí, y solo aquí, se eligen los adaptadores concretos y se conectan con la
aplicación: SQLite y el reloj del sistema para los puertos secundarios, y Flask
como adaptador primario. Las pruebas usan create_app con otra base y RelojFijo.
"""
import os

from avistamientos.aplicacion.servicio import ServicioDeAvistamientos
from avistamientos.aplicacion.validador import ValidadorDeAvistamiento
from avistamientos.adaptadores.primarios.http_flask import crear_app_flask
from avistamientos.adaptadores.secundarios.reloj_sistema import RelojSistema
from avistamientos.adaptadores.secundarios.repositorio_sqlite import RepositorioSQLite


def create_app(db_path=None, reloj=None):
    ruta = db_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "avistamientos.db"
    )
    servicio = ServicioDeAvistamientos(
        repositorio=RepositorioSQLite(ruta),
        validador=ValidadorDeAvistamiento(reloj or RelojSistema()),
    )
    app = crear_app_flask(servicio)
    app.config["DB_PATH"] = ruta
    return app


if __name__ == "__main__":
    create_app().run(port=5000)
