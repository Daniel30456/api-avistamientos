"""API de avistamientos organizada con arquitectura hexagonal (puertos y adaptadores).

- aplicacion/: el interior del hexágono. Reglas de negocio y puertos. No importa
  Flask, sqlite3 ni nada de afuera.
- adaptadores/: el exterior. Cada adaptador implementa o usa un puerto.
  Las dependencias de código apuntan siempre hacia aplicacion/.
"""
