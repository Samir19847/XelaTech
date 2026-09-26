from enum import Enum

class TipoCliente(Enum):
    INDIVIDUAL = "Individual"
    CORPORATIVO = "Corporativo"
    FRECUENTE = "FRECUENTE"

class TipoEquipo(Enum):
    COMPUTADORA_PORTATIL = "Computadora Portátil"
    COMPUTADORA_ESCRITORIO = "Computadora de Escritorio"
    IMPRESORA = "Impresora"
    CONSOLA = "Consola de Videojuegos"