class Persona:
    def __init__(self, código: str, nombreCompleto: str):
        # Al asignar sin guión bajo, obligas a ejecutar las validaciones del @setter
        self.código = código
        self.nombreCompleto = nombreCompleto

    @property
    def código(self) -> str:
        return self._código

    @código.setter
    def código(self, código: str):
        if not código.strip():
            raise ValueError("El código no puede estar vacío")
        self._código = código

    @property
    def nombreCompleto(self) -> str:
        return self._nombreCompleto

    @nombreCompleto.setter
    def nombreCompleto(self, nombreCompleto: str):
        if not nombreCompleto.strip():
            raise ValueError("El nombre completo no puede estar vacío")
        self._nombreCompleto = nombreCompleto