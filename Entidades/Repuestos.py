from Entidades.Enum import CategoriaRepuesto
class Repuestos:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: CategoriaRepuesto,
        existencia: int,
        costoUnitario: float,
        precioVenta: float,
        existenciaMinima: int = 1,
        cantidadUtilizada: int = 0,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.existencia = existencia
        self.existenciaMinima = existenciaMinima
        self.costoUnitario = costoUnitario
        self.precioVenta = precioVenta
        self.cantidadUtilizada = cantidadUtilizada

    @property
    def codigo(self) -> str:
        return self._codigo
    @codigo.setter
    def codigo(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código no puede estar vacío.")
        self._codigo = valor

    @property
    def nombre(self) -> str:
        return self._nombre
    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

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

    @property
    def existenciaMinima(self) -> int:
        return self._existenciaMinima
    @existenciaMinima.setter
    def existenciaMinima(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La existencia mínima debe ser un número entero mayor o igual a 0.")
        self._existenciaMinima = valor

    @property
    def costoUnitario(self) -> float:
        return self._costoUnitario
    @costoUnitario.setter
    def costoUnitario(self, valor: float):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor < 0:
            raise ValueError("El costo unitario debe ser un valor numérico mayor o igual a 0.")
        self._costoUnitario = float(valor)

    @property
    def precioVenta(self) -> float:
        return self._precioVenta
    @precioVenta.setter
    def precioVenta(self, valor: float):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor < 0:
            raise ValueError("El precio de venta debe ser un valor numérico mayor o igual a 0.")
        self._precioVenta = float(valor)

    @property
    def cantidadUtilizada(self) -> int:
        return self._cantidadUtilizada
    @cantidadUtilizada.setter
    def cantidadUtilizada(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("La cantidad utilizada debe ser un número entero mayor o igual a 0.")
        self._cantidadUtilizada = valor

    def usar_repuesto(self, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a utilizar debe ser un número entero mayor a 0.")
        if cantidad > self.existencia:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}'\n"
                f"Disponibles: {self.existencia}\n"
                f"Solicitados: {cantidad}."
            )
        self.existencia -= cantidad
        self.cantidadUtilizada += cantidad
    @property
    def bajoMinimo(self) -> bool:
        return self.existencia <= self.existenciaMinima