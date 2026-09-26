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