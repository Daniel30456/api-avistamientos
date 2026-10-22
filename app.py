import os
import sqlite3

from flask import Flask, g, jsonify, request

from validador import ValidadorDeAvistamiento

CAMPOS = ("especie", "lugar", "fecha", "observador")


def create_app(db_path=None, reloj=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "avistamientos.db"
    )
    validador = ValidadorDeAvistamiento(reloj)

    # ---------- Base de datos (SQLite) ----------
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with sqlite3.connect(app.config["DB_PATH"]) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS avistamientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                especie TEXT NOT NULL,
                lugar TEXT NOT NULL,
                fecha TEXT NOT NULL,
                observador TEXT NOT NULL
            )"""
        )

    # ---------- Utilidades ----------
    def buscar(id_):
        fila = get_db().execute(
            "SELECT * FROM avistamientos WHERE id = ?", (id_,)
        ).fetchone()
        return dict(fila) if fila else None

    def no_encontrado():
        return jsonify({"error": "Avistamiento no encontrado"}), 404

    # ---------- Endpoints ----------
    @app.get("/avistamientos")
    def listar():
        filas = get_db().execute("SELECT * FROM avistamientos ORDER BY id").fetchall()
        return jsonify([dict(f) for f in filas]), 200

    # Bonus: resumen por especie
    @app.get("/avistamientos/resumen")
    def resumen():
        filas = get_db().execute(
            "SELECT especie, COUNT(*) AS cantidad FROM avistamientos "
            "GROUP BY especie ORDER BY cantidad DESC, especie"
        ).fetchall()
        return jsonify([dict(f) for f in filas]), 200

    @app.get("/avistamientos/<int:id_>")
    def ver(id_):
        av = buscar(id_)
        return (jsonify(av), 200) if av else no_encontrado()

    @app.post("/avistamientos")
    def crear():
        datos = request.get_json(silent=True)
        error = validador.validar(datos)
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        cur = db.execute(
            "INSERT INTO avistamientos (especie, lugar, fecha, observador) "
            "VALUES (?, ?, ?, ?)",
            tuple(datos[c].strip() for c in CAMPOS),
        )
        db.commit()
        return jsonify(buscar(cur.lastrowid)), 201

    @app.put("/avistamientos/<int:id_>")
    def actualizar(id_):
        if not buscar(id_):
            return no_encontrado()
        datos = request.get_json(silent=True)
        error = validador.validar(datos)
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        db.execute(
            "UPDATE avistamientos SET especie=?, lugar=?, fecha=?, observador=? "
            "WHERE id=?",
            (*(datos[c].strip() for c in CAMPOS), id_),
        )
        db.commit()
        return jsonify(buscar(id_)), 200

    @app.delete("/avistamientos/<int:id_>")
    def eliminar(id_):
        if not buscar(id_):
            return no_encontrado()
        db = get_db()
        db.execute("DELETE FROM avistamientos WHERE id = ?", (id_,))
        db.commit()
        return "", 204

    return app


if __name__ == "__main__":
    create_app().run(port=5000)