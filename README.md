# API REST de Avistamientos de Aves

Trabajo individual - Ingeniería de Software 2 (Sesiones 17 y 22).
API REST en **Python + Flask** con base de datos **SQLite** (módulo `sqlite3` de la biblioteca estándar). Recibe y responde JSON. La Sesión 22 agrega la regla de validación y las pruebas unitarias y de integración.

## Recurso: avistamiento

| Campo | Descripción |
|---|---|
| `id` | Lo asigna el sistema |
| `especie` | Nombre de la especie (ej. "colibrí"), de 3 a 50 caracteres |
| `lugar` | Dónde se observó (no vacío) |
| `fecha` | Texto `AAAA-MM-DD`, no posterior a hoy |
| `observador` | Quién lo registró (no vacío) |

## Regla de validación

Un avistamiento es válido si: la especie tiene entre 3 y 50 caracteres, la fecha tiene formato `AAAA-MM-DD` y no es posterior a hoy, y el lugar y el observador no están vacíos. Si no es válido, POST y PUT responden 400 con un mensaje que indica qué campo falló. La validación vive en `validador.py` (`ValidadorDeAvistamiento`), separada de los endpoints.

## Requisitos

- Python 3.9 o superior
- pip
- Flask (se instala con `pip install flask`, ver abajo). SQLite ya viene incluido en Python.
- Para las pruebas: `pytest` y `pytest-cov`.

## Instalación y ejecución

```bash
git clone https://github.com/Daniel30456/api-avistamientos.git
cd api-avistamientos

# Crear y activar entorno virtual
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (CMD):
.venv\Scripts\activate.bat

pip install flask
python app.py
```

La API queda en `http://127.0.0.1:5000`. La base de datos (`avistamientos.db`) se crea sola al iniciar.

## Endpoints y ejemplos (curl)

> En Windows CMD usa comillas dobles y escapa las internas: `-d "{\"especie\":\"colibrí\"}"`. En PowerShell usa `curl.exe` en vez de `curl`.

| Método | Ruta | Respuesta |
|---|---|---|
| GET | `/avistamientos` | 200 con la lista |
| GET | `/avistamientos/{id}` | 200, o 404 |
| POST | `/avistamientos` | 201, o 400 si los datos son inválidos |
| PUT | `/avistamientos/{id}` | 200, o 404 (400 si los datos son inválidos) |
| DELETE | `/avistamientos/{id}` | 204, o 404 |
| GET | `/avistamientos/resumen` | 200 con cantidad por especie (bonus) |

**Listar**
```bash
curl http://127.0.0.1:5000/avistamientos
```

**Ver uno**
```bash
curl http://127.0.0.1:5000/avistamientos/1
```

**Registrar**
```bash
curl -X POST http://127.0.0.1:5000/avistamientos \
  -H "Content-Type: application/json" \
  -d '{"especie":"colibrí","lugar":"Parque Nacional","fecha":"2026-09-29","observador":"Ana"}'
```

**Actualizar**
```bash
curl -X PUT http://127.0.0.1:5000/avistamientos/1 \
  -H "Content-Type: application/json" \
  -d '{"especie":"colibrí","lugar":"Humedal Córdoba","fecha":"2026-09-29","observador":"Ana"}'
```

**Eliminar**
```bash
curl -X DELETE http://127.0.0.1:5000/avistamientos/1
```

**Resumen por especie (bonus)**
```bash
curl http://127.0.0.1:5000/avistamientos/resumen
```

## Pruebas

Con el entorno virtual activo:

```bash
pip install pytest pytest-cov
```

**Comando para correr las pruebas:**

```bash
python -m pytest
```

**Comando para generar la cobertura:**

```bash
python -m pytest --cov=app --cov=validador --cov-report=term-missing
```

Para guardar el reporte en un archivo (queda en `docs/cobertura.txt`):

```bash
python -m pytest --cov=app --cov=validador --cov-report=term-missing > docs/cobertura.txt
```

Estructura:

- `tests/test_validador.py`: pruebas unitarias de la validación (partición de equivalencia y valores límite), con el stub `RelojFijo`.
- `tests/test_api.py`: pruebas de integración de los endpoints por HTTP (`test_client` de Flask), con una base SQLite temporal por prueba.
- `tests/dobles.py`: doble de prueba (`RelojFijo`).
- `docs/`: documento de justificación y reporte de cobertura.

## Uso de IA

- IA usada: **Claude** (Anthropic), modelo **Sonnet 5.5**.
- La usé como apoyo para este trabajo: me ayudó a entender cómo funcionan Git, GitHub y Flask, y cómo se conectan las rutas con la base de datos SQLite. En la Sesión 22 tambien como estructurar las pruebas y redactar la justificación.
- Yo probé todos los endpoints con curl, corrí las pruebas, revisé el código y lo entiendo, y soy responsable de lo que publico.

## Autor

Daniel30456 - Universidad El Bosque