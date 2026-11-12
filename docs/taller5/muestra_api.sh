#!/usr/bin/env bash
# Recorre todos los endpoints con curl e imprime el código HTTP y el cuerpo de cada respuesta.
# Se corre con la API levantada (python app.py) y una base de datos vacía.
# Se usó igual antes y después del refactor para comprobar que la API responde lo mismo.
#   bash docs/taller5/muestra_api.sh > docs/taller5/api_antes.txt
URL=${URL:-http://127.0.0.1:5000}
J="Content-Type: application/json"

pedir() {  # pedir METODO RUTA [CUERPO]
  echo "### $1 $2 ${3:-}"
  if [ -n "$3" ]; then
    curl -s -w "\n-> HTTP %{http_code}\n\n" -X "$1" "$URL$2" -H "$J" -d "$3"
  else
    curl -s -w "\n-> HTTP %{http_code}\n\n" -X "$1" "$URL$2"
  fi
}

pedir GET    /avistamientos
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"Parque Nacional","fecha":"2026-09-29","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"  águila  ","lugar":"Humedal Córdoba","fecha":"2026-10-01","observador":"Luis"}'
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"Cerros Orientales","fecha":"2026-10-05","observador":"Ana"}'
pedir GET    /avistamientos
pedir GET    /avistamientos/1
pedir GET    /avistamientos/999
pedir GET    /avistamientos/resumen
pedir PUT    /avistamientos/1 '{"especie":"colibrí","lugar":"Humedal Córdoba","fecha":"2026-09-29","observador":"Ana"}'
pedir PUT    /avistamientos/999 '{"especie":"colibrí","lugar":"Humedal Córdoba","fecha":"2026-09-29","observador":"Ana"}'
pedir PUT    /avistamientos/1 '{"especie":"ab","lugar":"Humedal Córdoba","fecha":"2026-09-29","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"ab","lugar":"Parque","fecha":"2026-09-29","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"Parque","fecha":"2999-01-01","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"Parque","fecha":"29-09-2026","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"Parque","fecha":"2026-02-30","observador":"Ana"}'
pedir POST   /avistamientos '{"especie":"colibrí","lugar":"   ","fecha":"2026-09-29","observador":"Ana"}'
pedir POST   /avistamientos '["no","es","un","objeto"]'
pedir DELETE /avistamientos/2
pedir DELETE /avistamientos/2
pedir GET    /avistamientos
pedir GET    /avistamientos/resumen
