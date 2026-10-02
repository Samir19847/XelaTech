from typing import List
from Entidades.Cliente import Cliente
from Algoritmos.AlgoritmosBusqueda import AlgoritmosBusqueda

class ClienteService:
    
    def __init__(self):
        self.clientes: List[Cliente] = []

    def registrar_cliente(self, id_cliente: str, nombre: str, telefono: str, correo: str) -> Cliente:
        if not id_cliente or not nombre or not telefono:
            raise ValueError("Error: El ID, nombre y teléfono son obligatorios.")
        for c in self.clientes:
            if c.id_cliente == id_cliente:
                raise ValueError(f"Error: Ya existe un cliente registrado con el ID {id_cliente}.")
        nuevo_cliente = Cliente(id_cliente, nombre, telefono, correo)
        self.clientes.append(nuevo_cliente)  
        return nuevo_cliente

    def buscar_clientes_por_nombre(self, nombre_parcial: str) -> List[Cliente]:
        resultados = AlgoritmosBusqueda.busqueda_secuencial(
            lista=self.clientes,
            termino_busqueda=nombre_parcial,
            key=lambda c: c.nombre,
            busqueda_parcial=True
        )
        return resultados

    def obtener_todos_los_clientes(self) -> List[Cliente]:
        return self.clientes.copy()