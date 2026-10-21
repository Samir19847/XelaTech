from Entidades.Equipo import Equipo
from Entidades.Cliente import Cliente
from Entidades.Enum import TipoEquipo

class Impresora(Equipo):
    ESPECIALIDAD_REQUERIDA = "Impresoras"
    def __init__(
        self,
        codigoInterno: str,
        numeroSerie: str,
        marca: str,
        modelo: str,
        propietario: Cliente,
        estadoFisico: str,
        accesoriosEntregados: str,
        tipoInyeccion: str = "Tinta Contínua",
    ):
        super().__init__(codigoInterno, numeroSerie, marca, modelo, propietario, TipoEquipo.IMPRESORA, estadoFisico, accesoriosEntregados)
        self.tipoInyeccion = tipoInyeccion

    @property
    def tipoInyeccion(self) -> str:
        return self._tipoInyeccion
    @tipoInyeccion.setter
    def tipoInyeccion(self, valor: str):
        if not valor.strip():
            raise ValueError("El tipo de inyección no puede estar vacío.")
        self._tipoInyeccion = valor

    def calcular_costo_revision(self) -> float:
        return 110.0