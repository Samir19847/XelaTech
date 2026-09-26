from Entidades.Cliente import Cliente
from Entidades.Enum import TipoEquipo
class Equipo:
    def __init__(self, codigoInterno: str, numeroSerie: str, marca: str, modelo: str, propietario: Cliente, tipoEquipo: TipoEquipo, estadoFisico: str, accesoriosEntregados: str):
        self.codigoInterno = codigoInterno
        self.numeroSerie = numeroSerie
        self.marca = marca
        self.modelo = modelo
        self.propietario = propietario
        self.tipoEquipo = tipoEquipo
        self.estadoFisico = estadoFisico
        self.accesoriosEntregados = accesoriosEntregados

    @property
    def codigoInterno(self) -> str:
        return self._codigoInterno
    @codigoInterno.setter
    def codigoInterno(self, valor: str):
        if not valor.strip():
            raise ValueError("El código interno no puede estar vacío.")
        self._codigoInterno = valor

    @property
    def numeroSerie(self) -> str:
        return self._numeroSerie
    @numeroSerie.setter
    def numeroSerie(self, valor: str):
        if not valor.strip():
            raise ValueError("El número de serie no puede estar vacío.")
        self._numeroSerie = valor

    @property
    def marca(self) -> str:
        return self._marca
    @marca.setter
    def marca(self, valor: str):
        if not valor.strip():
            raise ValueError("La marca no puede estar vacía.")
        self._marca = valor

    @property
    def modelo(self) -> str:
        return self._modelo
    @modelo.setter
    def modelo(self, valor: str):
        if not valor.strip():
            raise ValueError("El modelo no puede estar vacío.")
        self._modelo = valor

    @property
    def propietario(self) -> Cliente:
        return self._propietario

    @propietario.setter
    def propietario(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise ValueError("El propietario debe ser una instancia de la clase Cliente.")
        self._propietario = valor

    @property
    def tipoEquipo(self) -> str:
        return self._tipoEquipo
    @tipoEquipo.setter
    def tipoEquipo(self, valor: TipoEquipo):
        if not isinstance(valor, TipoEquipo):
            raise ValueError("El tipo de equipo debe ser una opción válida de TipoEquipo.")
        self._tipoEquipo = valor

    @property
    def estadoFisico(self) -> str:
        return self._estadoFisico
    @estadoFisico.setter
    def estadoFisico(self, valor: str):
        if not valor.strip():
            raise ValueError("El estado físico no puede estar vacío.")
        self._estadoFisico = valor

    @property
    def accesoriosEntregados(self) -> str:
        return self._accesoriosEntregados
    @accesoriosEntregados.setter
    def accesoriosEntregados(self, valor: str):
        if not valor.strip():
            raise ValueError("Los accesorios entregados no pueden estar vacíos.")
        self._accesoriosEntregados = valor

    def calcular_costo_revision(self) -> float:
        return 100.0