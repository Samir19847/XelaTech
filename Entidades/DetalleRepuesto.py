from Entidades.Repuestos import Repuestos
class DetalleRepuesto:

    def __init__(self, repuesto: Repuestos, cantidad: int):
        if not isinstance(repuesto, Repuestos):
            raise ValueError("El repuesto debe ser una instancia de la clase Repuestos.")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un número entero mayor a 0.")
        self._repuesto = repuesto
        self._cantidad = cantidad

    @property
    def repuesto(self) -> Repuestos:
        return self._repuesto
    @property
    def cantidad(self) -> int:
        return self._cantidad
    @property
    def subtotal(self) -> float:
        return self._repuesto.precioVenta * self._cantidad