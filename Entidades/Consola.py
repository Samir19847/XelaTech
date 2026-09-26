from Entidades.Equipo import Equipo
from Entidades.Cliente import Cliente

class Consola(Equipo):
    def __init__(
        self,
        codigoInterno: str,
        numeroSerie: str,
        marca: str,
        modelo: str,
        propietario: Cliente,
        estadoFisico: str,
        accesoriosEntregados: str,
        cantidadMandos: int = 1
    ):
        super().__init__(codigoInterno, numeroSerie, marca, modelo, propietario, "Consola de Videojuegos", estadoFisico, accesoriosEntregados)
        self.cantidadMandos = cantidadMandos

    @property
    def cantidadMandos(self) -> int:
        return self._cantidadMandos
    @cantidadMandos.setter
    def cantidadMandos(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La cantidad de mandos debe ser un número entero mayor o igual a 0.")
        self._cantidadMandos = valor

    def calcular_costo_revision(self) -> float:
        return 135.0
    