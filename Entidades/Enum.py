from enum import Enum

class TipoCliente(Enum):
    INDIVIDUAL = "Individual"
    CORPORATIVO = "Corporativo"
    FRECUENTE = "Frecuente"

class TipoEquipo(Enum):
    COMPUTADORA_PORTATIL = "Computadora Portátil"
    COMPUTADORA_ESCRITORIO = "Computadora de Escritorio"
    IMPRESORA = "Impresora"
    CONSOLA = "Consola de Videojuegos"

class NivelPrioridad(Enum):
    NORMAL = "Normal"
    URGENTE = "Urgente"

class EstadoSolicitud(Enum):
    RECIBIDA = "Recibida"
    EN_ESPERA = "En espera"
    ASIGNADA = "Asignada"
    EN_DIAGNOSTICO = "En diagnóstico"
    EN_REPARACION = "En reparación"
    LISTA_PARA_ENTREGAR = "Lista para entregar"
    ENTREGADA = "Entregada"
    CANCELADA = "Cancelada"
class CategoriaRepuesto(Enum):
    ALMACENAMIENTO = "Almacenamiento"
    MEMORIA_RAM = "Memoria RAM"
    PANTALLAS = "Pantallas y Displays"
    PERIFERICOS = "Periféricos y Consumibles"
    COMPONENTES_INTERNOS = "Componentes Internos"
    ACCESORIOS_CONSOLAS = "Accesorios y Repuestos de Consolas"