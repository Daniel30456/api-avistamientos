from datetime import date, timedelta
import pytest
from validador import ValidadorDeAvistamiento, RelojSistema
from tests.dobles import RelojFijo

HOY = date(2026, 10, 21)


def datos(**cambios):
    base = {"especie": "colibrí", "lugar": "Humedal Córdoba",
            "fecha": "2026-10-01", "observador": "Ana"}
    base.update(cambios)
    return base


@pytest.fixture
def validador():
    return ValidadorDeAvistamiento(RelojFijo(HOY))   # stub del reloj


def test_avistamiento_completo_es_valido(validador):
    # Arrange
    entrada = datos()
    # Act
    error = validador.validar(entrada)
    # Assert
    assert error is None


@pytest.mark.parametrize("especie", ["abc", "a" * 50])
def test_especie_en_el_limite_valido_se_acepta(validador, especie):
    assert validador.validar(datos(especie=especie)) is None


@pytest.mark.parametrize("especie", ["ab", "a" * 51])
def test_especie_fuera_del_limite_se_rechaza_nombrando_el_campo(validador, especie):
    error = validador.validar(datos(especie=especie))
    assert error is not None and error.startswith("especie")


def test_fecha_de_hoy_es_valida(validador):
    assert validador.validar(datos(fecha=HOY.isoformat())) is None


def test_fecha_de_manana_se_rechaza(validador):
    manana = (HOY + timedelta(days=1)).isoformat()
    error = validador.validar(datos(fecha=manana))
    assert error.startswith("fecha")


@pytest.mark.parametrize("fecha", ["29-09-2026", "2026-9-1", "2026-13-45", "ayer"])
def test_fecha_con_formato_invalido_se_rechaza(validador, fecha):
    assert validador.validar(datos(fecha=fecha)).startswith("fecha")


@pytest.mark.parametrize("campo", ["lugar", "observador"])
def test_campo_vacio_se_rechaza_nombrando_el_campo(validador, campo):
    assert validador.validar(datos(**{campo: "  "})).startswith(campo)


def test_cuerpo_que_no_es_objeto_json_se_rechaza(validador):
    assert validador.validar(None) is not None


def test_reloj_sistema_devuelve_la_fecha_de_hoy():
    assert RelojSistema().hoy() == date.today()