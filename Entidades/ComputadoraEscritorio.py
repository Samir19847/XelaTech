from Entidades.Equipo import Equipo
from Entidades.Cliente import Cliente

class ComputadoraEscritorio(Equipo):
    def __init__(
        self,
        codigoInterno: str,
        numeroSerie: str,
        marca: str,
        modelo: str,
        propietario: Cliente,
        estadoFisico: str,
        accesoriosEntregados: str,
        tipoGabinete: str = "Mid Tower"
    ):
        super().__init__(codigoInterno, numeroSerie, marca, modelo, propietario, "Computadora de Escritorio", estadoFisico, accesoriosEntregados)
        self.tipoGabinete = tipoGabinete

    @property
    def tipoGabinete(self) -> str:
        return self._tipoGabinete
    @tipoGabinete.setter
    def tipoGabinete(self, valor: str):
        if not valor.strip():
            raise ValueError("El tipo de gabinete no puede estar vacío.")
        self._tipoGabinete = valor

    def calcular_costo_revision(self) -> float:
        return 150.0