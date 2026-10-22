from datetime import date
import pytest
from app import create_app
from tests.dobles import RelojFijo

VALIDO = {"especie": "colibrí", "lugar": "Parque Nacional",
          "fecha": "2026-10-01", "observador": "Ana"}


@pytest.fixture
def client(tmp_path):
    # BD nueva por prueba => pruebas independientes
    app = create_app(db_path=str(tmp_path / "test.db"),
                     reloj=RelojFijo(date(2026, 10, 21)))
    return app.test_client()


def crear(client, **cambios):
    return client.post("/avistamientos", json={**VALIDO, **cambios})


def test_post_valido_responde_201_y_queda_guardado(client):
    r = crear(client)
    assert r.status_code == 201
    cuerpo = r.get_json()
    assert cuerpo["id"] == 1 and cuerpo["especie"] == "colibrí"
    g = client.get(f"/avistamientos/{cuerpo['id']}")
    assert g.status_code == 200 and g.get_json() == cuerpo


def test_post_con_especie_corta_responde_400_con_mensaje(client):
    r = crear(client, especie="ab")
    assert r.status_code == 400
    assert "especie" in r.get_json()["error"]
    assert client.get("/avistamientos").get_json() == []   # no se guardó


def test_post_con_fecha_futura_responde_400(client):
    assert crear(client, fecha="2026-10-22").status_code == 400


def test_get_lista_devuelve_lo_registrado(client):
    crear(client); crear(client, especie="águila")
    r = client.get("/avistamientos")
    assert r.status_code == 200
    assert [a["especie"] for a in r.get_json()] == ["colibrí", "águila"]


def test_get_por_id_inexistente_responde_404(client):
    assert client.get("/avistamientos/999").status_code == 404


def test_put_valido_actualiza_y_el_cambio_persiste(client):
    crear(client)
    r = client.put("/avistamientos/1", json={**VALIDO, "lugar": "Humedal"})
    assert r.status_code == 200 and r.get_json()["lugar"] == "Humedal"
    assert client.get("/avistamientos/1").get_json()["lugar"] == "Humedal"


def test_put_con_datos_invalidos_responde_400(client):
    crear(client)
    assert client.put("/avistamientos/1", json={**VALIDO, "especie": "x"}).status_code == 400


def test_put_inexistente_responde_404(client):
    assert client.put("/avistamientos/999", json=VALIDO).status_code == 404


def test_delete_responde_204_y_luego_el_id_da_404(client):
    crear(client)
    assert client.delete("/avistamientos/1").status_code == 204
    assert client.get("/avistamientos/1").status_code == 404


def test_delete_inexistente_responde_404(client):
    assert client.delete("/avistamientos/999").status_code == 404


def test_resumen_cuenta_avistamientos_por_especie(client):
    crear(client); crear(client); crear(client, especie="águila")
    r = client.get("/avistamientos/resumen")
    assert r.status_code == 200
    assert r.get_json() == [
        {"especie": "colibrí", "cantidad": 2},
        {"especie": "águila", "cantidad": 1},
    ]