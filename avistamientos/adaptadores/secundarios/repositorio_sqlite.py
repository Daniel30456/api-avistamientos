import sqlite3
from contextlib import contextmanager

from avistamientos.aplicacion.modelo import Avistamiento
from avistamientos.aplicacion.puertos.secundarios import RepositorioDeAvistamientos


class RepositorioSQLite(RepositorioDeAvistamientos):
    """Adaptador del puerto RepositorioDeAvistamientos sobre SQLite.

    Es el único lugar del proyecto donde hay SQL. Convierte las filas de la base
    de datos en objetos Avistamiento, para que ninguna fila cruce hacia la aplicación.
    """

    def __init__(self, ruta):
        self._ruta = ruta
        with self._conexion() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS avistamientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    especie TEXT NOT NULL,
                    lugar TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    observador TEXT NOT NULL
                )"""
            )

    @contextmanager
    def _conexion(self):
        conn = sqlite3.connect(self._ruta)
        conn.row_factory = sqlite3.Row
        try:
            with conn:          # commit si todo sale bien, rollback si hay error
                yield conn
        finally:
            conn.close()

    @staticmethod
    def _a_avistamiento(fila):
        return Avistamiento(
            id=fila["id"],
            especie=fila["especie"],
            lugar=fila["lugar"],
            fecha=fila["fecha"],
            observador=fila["observador"],
        )

    def listar(self):
        with self._conexion() as conn:
            filas = conn.execute("SELECT * FROM avistamientos ORDER BY id").fetchall()
        return [self._a_avistamiento(f) for f in filas]

    def buscar(self, id_):
        with self._conexion() as conn:
            fila = conn.execute(
                "SELECT * FROM avistamientos WHERE id = ?", (id_,)
            ).fetchone()
        return self._a_avistamiento(fila) if fila else None

    def agregar(self, avistamiento):
        with self._conexion() as conn:
            cur = conn.execute(
                "INSERT INTO avistamientos (especie, lugar, fecha, observador) "
                "VALUES (?, ?, ?, ?)",
                (avistamiento.especie, avistamiento.lugar,
                 avistamiento.fecha, avistamiento.observador),
            )
            nuevo_id = cur.lastrowid
        return self.buscar(nuevo_id)

    def reemplazar(self, avistamiento):
        with self._conexion() as conn:
            conn.execute(
                "UPDATE avistamientos SET especie=?, lugar=?, fecha=?, observador=? "
                "WHERE id=?",
                (avistamiento.especie, avistamiento.lugar, avistamiento.fecha,
                 avistamiento.observador, avistamiento.id),
            )
        return self.buscar(avistamiento.id)

    def eliminar(self, id_):
        with self._conexion() as conn:
            conn.execute("DELETE FROM avistamientos WHERE id = ?", (id_,))
