from Entidades.Enum import CategoriaRepuesto
class Repuestos():
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: CategoriaRepuesto,
        existencia: int,
        costoUnitario: float,
        precioVenta: float,
        cantidadUtilizada: int,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.existencia = existencia
        self.existenciaMinima = 1
        self.costoUnitario = costoUnitario
        self.precioVenta = precioVenta
        self.cantidadUtilizada = 0
    @property
    def categoria(self) -> CategoriaRepuesto:
        return self._categoria
    @categoria.setter
    def categoria(self, valor: CategoriaRepuesto):
        if not isinstance(valor, CategoriaRepuesto):
            raise ValueError("La categoría debe ser una instancia válida de CategoriaRepuesto.")
        self._categoria = valor

    @property
    def existencia(self) -> int:
        return self._existencia
    @existencia.setter
    def existencia(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La existencia debe ser un número entero mayor o igual a 0.")
        self._existencia = valor

    def usar_repuesto(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a utilizar debe ser un número entero mayor a 0.")
        if cantidad > self.existencia:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}'\nDisponibles: {self.existencia}\nSolicitados: {cantidad}."
            )
        self.existencia -= cantidad
        self.cantidadUtilizada += cantidad
        if self.existencia <= self.existenciaMinima:
            print(
                f"⚠️ ALERTA DE STOCK: El repuesto '{self.nombre}' está en o por debajo del mínimo\n"
                f"(Stock actual: {self.existencia}, Mínimo: {self.existenciaMinima})."
            )