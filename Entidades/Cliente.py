from Entidades.Persona import Persona

class Cliente(Persona):
    def __init__(self, código: str, nombreCompleto: str, telefono: str, correoElectronico: str, tipoCliente: str, cantidadSolicitudes: int = 0):
        super().__init__(código, nombreCompleto)
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.tipoCliente = tipoCliente
        self.cantidadSolicitudes = cantidadSolicitudes
    @property
    def telefono(self) -> str:
        return self._telefono
    @telefono.setter
    def telefono(self, telefono: str):
        if not telefono.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        self._telefono = telefono

    @property
    def correoElectronico(self) -> str:
        return self._correoElectronico
    @correoElectronico.setter
    def correoElectronico(self, correoElectronico: str):
        if not correoElectronico.strip():
            raise ValueError("El correo electrónico no puede estar vacío.")
        if "@" not in correoElectronico:
            raise ValueError("El correo electrónico debe contener un '@'.")
        self._correoElectronico = correoElectronico

    @property
    def tipoCliente(self) -> str:
        return self._tipoCliente
    @tipoCliente.setter
    def tipoCliente(self, tipoCliente: str):
        if not tipoCliente.strip():
            raise ValueError("El tipo de cliente no puede estar vacío.")
        self._tipoCliente = tipoCliente

    @property
    def cantidadSolicitudes(self) -> int:
        return self._cantidadSolicitudes

    @cantidadSolicitudes.setter
    def cantidadSolicitudes(self, cantidadSolicitudes: int):
        if not isinstance(cantidadSolicitudes, int) or cantidadSolicitudes < 0:
            raise ValueError("La cantidad de solicitudes debe ser un número entero mayor o igual a 0.")
        self._cantidadSolicitudes = cantidadSolicitudes