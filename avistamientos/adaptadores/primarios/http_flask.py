from dataclasses import asdict

from flask import Flask, jsonify, request

from avistamientos.aplicacion.errores import AvistamientoNoEncontrado, DatosInvalidos
from avistamientos.aplicacion.puertos.primarios import GestionDeAvistamientos


def crear_app_flask(gestion: GestionDeAvistamientos) -> Flask:
    """Adaptador primario HTTP: traduce peticiones JSON a llamadas al puerto primario
    y las respuestas (o errores) de la aplicación a JSON con su código HTTP.
    Es el único lugar del proyecto que conoce Flask."""
    app = Flask(__name__)

    @app.errorhandler(AvistamientoNoEncontrado)
    def no_encontrado(_e):
        return jsonify({"error": "Avistamiento no encontrado"}), 404

    @app.errorhandler(DatosInvalidos)
    def datos_invalidos(e):
        return jsonify({"error": str(e)}), 400

    @app.get("/avistamientos")
    def listar():
        return jsonify([asdict(a) for a in gestion.listar()]), 200

    # Bonus: resumen por especie
    @app.get("/avistamientos/resumen")
    def resumen():
        return jsonify([asdict(c) for c in gestion.resumen()]), 200

    @app.get("/avistamientos/<int:id_>")
    def ver(id_):
        return jsonify(asdict(gestion.obtener(id_))), 200

    @app.post("/avistamientos")
    def crear():
        datos = request.get_json(silent=True)
        return jsonify(asdict(gestion.registrar(datos))), 201

    @app.put("/avistamientos/<int:id_>")
    def actualizar(id_):
        datos = request.get_json(silent=True)
        return jsonify(asdict(gestion.actualizar(id_, datos))), 200

    @app.delete("/avistamientos/<int:id_>")
    def eliminar(id_):
        gestion.eliminar(id_)
        return "", 204

    return app
