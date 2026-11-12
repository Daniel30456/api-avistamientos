class AvistamientoNoEncontrado(Exception):
    """No existe un avistamiento con el id pedido."""


class DatosInvalidos(Exception):
    """Los datos no cumplen la regla de validación. El mensaje dice qué campo falló."""
