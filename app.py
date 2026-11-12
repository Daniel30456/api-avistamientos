import os
from collections import Counter
from dataclasses import asdict

from flask import Flask, jsonify, request

from avistamientos.aplicacion.modelo import Avistamiento
from avistamientos.aplicacion.validador import CAMPOS, ValidadorDeAvistamiento
from avistamientos.adaptadores.secundarios.reloj_sistema import RelojSistema
from avistamientos.adaptadores.secundarios.repositorio_sqlite import RepositorioSQLite


def create_app(db_path=None, reloj=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "avistamientos.db"
    )
    validador = ValidadorDeAvistamiento(reloj or RelojSistema())
    repositorio = RepositorioSQLite(app.config["DB_PATH"])

    # ---------- Utilidades ----------
    def no_encontrado():
        return jsonify({"error": "Avistamiento no encontrado"}), 404

    def construir(datos, id_=None):
        return Avistamiento(id=id_, **{c: datos[c].strip() for c in CAMPOS})

    # ---------- Endpoints ----------
    @app.get("/avistamientos")
    def listar():
        return jsonify([asdict(a) for a in repositorio.listar()]), 200

    # Bonus: resumen por especie
    @app.get("/avistamientos/resumen")
    def resumen():
        conteo = Counter(a.especie for a in repositorio.listar())
        orden = sorted(conteo.items(), key=lambda par: (-par[1], par[0]))
        return jsonify([{"especie": e, "cantidad": n} for e, n in orden]), 200

    @app.get("/avistamientos/<int:id_>")
    def ver(id_):
        av = repositorio.buscar(id_)
        return (jsonify(asdict(av)), 200) if av else no_encontrado()

    @app.post("/avistamientos")
    def crear():
        datos = request.get_json(silent=True)
        error = validador.validar(datos)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(asdict(repositorio.agregar(construir(datos)))), 201

    @app.put("/avistamientos/<int:id_>")
    def actualizar(id_):
        if not repositorio.buscar(id_):
            return no_encontrado()
        datos = request.get_json(silent=True)
        error = validador.validar(datos)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(asdict(repositorio.reemplazar(construir(datos, id_)))), 200

    @app.delete("/avistamientos/<int:id_>")
    def eliminar(id_):
        if not repositorio.buscar(id_):
            return no_encontrado()
        repositorio.eliminar(id_)
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(port=5000)
