import os
from dataclasses import asdict

from flask import Flask, jsonify, request

from avistamientos.aplicacion.errores import AvistamientoNoEncontrado, DatosInvalidos
from avistamientos.aplicacion.servicio import ServicioDeAvistamientos
from avistamientos.aplicacion.validador import ValidadorDeAvistamiento
from avistamientos.adaptadores.secundarios.reloj_sistema import RelojSistema
from avistamientos.adaptadores.secundarios.repositorio_sqlite import RepositorioSQLite


def create_app(db_path=None, reloj=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "avistamientos.db"
    )
    servicio = ServicioDeAvistamientos(
        RepositorioSQLite(app.config["DB_PATH"]),
        ValidadorDeAvistamiento(reloj or RelojSistema()),
    )

    @app.errorhandler(AvistamientoNoEncontrado)
    def no_encontrado(_e):
        return jsonify({"error": "Avistamiento no encontrado"}), 404

    @app.errorhandler(DatosInvalidos)
    def datos_invalidos(e):
        return jsonify({"error": str(e)}), 400

    # ---------- Endpoints ----------
    @app.get("/avistamientos")
    def listar():
        return jsonify([asdict(a) for a in servicio.listar()]), 200

    # Bonus: resumen por especie
    @app.get("/avistamientos/resumen")
    def resumen():
        return jsonify([asdict(c) for c in servicio.resumen()]), 200

    @app.get("/avistamientos/<int:id_>")
    def ver(id_):
        return jsonify(asdict(servicio.obtener(id_))), 200

    @app.post("/avistamientos")
    def crear():
        datos = request.get_json(silent=True)
        return jsonify(asdict(servicio.registrar(datos))), 201

    @app.put("/avistamientos/<int:id_>")
    def actualizar(id_):
        datos = request.get_json(silent=True)
        return jsonify(asdict(servicio.actualizar(id_, datos))), 200

    @app.delete("/avistamientos/<int:id_>")
    def eliminar(id_):
        servicio.eliminar(id_)
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(port=5000)
