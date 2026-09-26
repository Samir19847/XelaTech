from Entidades.Equipo import Equipo
from Entidades.Cliente import Cliente

class ComputadoraPortatil(Equipo):
    def __init__(
        self,
        codigoInterno: str,
        numeroSerie: str,
        marca: str,
        modelo: str,
        propietario: Cliente,
        estadoFisico: str,
        accesoriosEntregados: str,
        incluyeCargador: bool = True
    ):
        super().__init__(codigoInterno, numeroSerie, marca, modelo, propietario, "Computadora Portátil", estadoFisico, accesoriosEntregados)
        self.incluyeCargador = incluyeCargador

    @property
    def incluyeCargador(self) -> bool:
        return self._incluyeCargador

    @incluyeCargador.setter
    def incluyeCargador(self, valor: bool):
        if not isinstance(valor, bool):
            raise ValueError("El valor de incluyeCargador debe ser booleano (True/False).")
        self._incluyeCargador = valor

    def calcular_costo_revision(self) -> float:
        return 125.0