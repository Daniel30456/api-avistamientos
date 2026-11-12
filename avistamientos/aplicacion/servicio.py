from collections import Counter

from avistamientos.aplicacion.errores import AvistamientoNoEncontrado, DatosInvalidos
from avistamientos.aplicacion.modelo import Avistamiento, ConteoPorEspecie
from avistamientos.aplicacion.puertos.primarios import GestionDeAvistamientos
from avistamientos.aplicacion.puertos.secundarios import RepositorioDeAvistamientos
from avistamientos.aplicacion.validador import CAMPOS, ValidadorDeAvistamiento


class ServicioDeAvistamientos(GestionDeAvistamientos):
    """Implementa el puerto primario. Recibe sus dependencias por el constructor
    (el repositorio es un puerto secundario), así no sabe qué hay detrás."""

    def __init__(self, repositorio: RepositorioDeAvistamientos,
                 validador: ValidadorDeAvistamiento):
        self._repositorio = repositorio
        self._validador = validador

    def listar(self):
        return self._repositorio.listar()

    def obtener(self, id_):
        avistamiento = self._repositorio.buscar(id_)
        if avistamiento is None:
            raise AvistamientoNoEncontrado(id_)
        return avistamiento

    def registrar(self, datos):
        self._validar(datos)
        return self._repositorio.agregar(self._construir(datos))

    def actualizar(self, id_, datos):
        self.obtener(id_)          # primero 404, luego 400, como antes del refactor
        self._validar(datos)
        return self._repositorio.reemplazar(self._construir(datos, id_))

    def eliminar(self, id_):
        self.obtener(id_)
        self._repositorio.eliminar(id_)

    def resumen(self):
        conteo = Counter(a.especie for a in self._repositorio.listar())
        orden = sorted(conteo.items(), key=lambda par: (-par[1], par[0]))
        return [ConteoPorEspecie(especie=e, cantidad=n) for e, n in orden]

    def _validar(self, datos):
        error = self._validador.validar(datos)
        if error:
            raise DatosInvalidos(error)

    @staticmethod
    def _construir(datos, id_=None):
        return Avistamiento(id=id_, **{c: datos[c].strip() for c in CAMPOS})
