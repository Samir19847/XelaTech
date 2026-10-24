from typing import List, Optional, Callable, Any
from Entidades.Cliente import Cliente
from Entidades.Técnicos import Tecnico
from Entidades.Equipo import Equipo
from Entidades.ComputadoraPortatil import ComputadoraPortatil
from Entidades.ComputadoraEscritorio import ComputadoraEscritorio
from Entidades.Impresora import Impresora
from Entidades.Consola import Consola
from Entidades.Repuestos import Repuestos
from Entidades.Solicitudes import Solicitud
from Entidades.Enum import TipoCliente, TipoEquipo, NivelPrioridad, CategoriaRepuesto
from Algoritmos.AlgoritmosBusqueda import AlgoritmosBusqueda


class GestorXelaTech:
    CLASES_EQUIPO = {
        TipoEquipo.COMPUTADORA_PORTATIL: ComputadoraPortatil,
        TipoEquipo.COMPUTADORA_ESCRITORIO: ComputadoraEscritorio,
        TipoEquipo.IMPRESORA: Impresora,
        TipoEquipo.CONSOLA: Consola,
    }

    def __init__(self):
        self._clientes: List[Cliente] = []
        self._tecnicos: List[Tecnico] = []
        self._equipos: List[Equipo] = []
        self._solicitudes: List[Solicitud] = []
        self._repuestos: List[Repuestos] = []
    @staticmethod
    def _limpiar(valor: Any, campo: str) -> str:
        if not isinstance(valor, str):
            raise ValueError(f"{campo} debe ser texto.")
        return valor.strip()

    @staticmethod
    def _obtener(lista: List[Any], valor: str, key: Callable[[Any], str]) -> Optional[Any]:
        coincidencias = AlgoritmosBusqueda.busqueda_secuencial(
            lista, valor.strip(), key=key, busqueda_parcial=False
        )
        return coincidencias[0] if coincidencias else None

    def _exigir(self, lista: List[Any], valor: str, key: Callable[[Any], str], que: str) -> Any:
        encontrado = self._obtener(lista, valor, key)
        if encontrado is None:
            raise ValueError(f"No existe {que} con '{valor}'.")
        return encontrado

    def _exigir_libre(self, lista: List[Any], valor: str, key: Callable[[Any], str], que: str):
        if self._obtener(lista, valor, key) is not None:
            raise ValueError(f"Ya existe {que} '{valor}'.")

    def _solicitud_activa_de(self, equipo: Equipo) -> Optional[Solicitud]:
        for solicitud in self._solicitudes:
            if solicitud.equipo is equipo and solicitud.estado not in Solicitud.ESTADOS_FINALES:
                return solicitud
        return None

    @classmethod
    def especialidades_validas(cls) -> List[str]:
        """Las especialidades salen de las clases de equipo: una sola fuente de verdad."""
        especialidades: List[str] = []
        for clase in cls.CLASES_EQUIPO.values():
            if clase.ESPECIALIDAD_REQUERIDA not in especialidades:
                especialidades.append(clase.ESPECIALIDAD_REQUERIDA)
        return especialidades
    
    def registrar_cliente(self, codigo: str, nombre: str, telefono: str,
                          correo: str, tipo: TipoCliente) -> Cliente:
        cliente = Cliente(
            self._limpiar(codigo, "El código"), self._limpiar(nombre, "El nombre"),
            self._limpiar(telefono, "El teléfono"), self._limpiar(correo, "El correo"), tipo
        )
        self._exigir_libre(self._clientes, cliente.código, lambda c: c.código, "un cliente con código")
        self._clientes.append(cliente)
        return cliente

    def actualizar_cliente(self, codigo: str, nombre: Optional[str] = None, telefono: Optional[str] = None,
                           correo: Optional[str] = None, tipo: Optional[TipoCliente] = None) -> Cliente:
        cliente = self._exigir(self._clientes, codigo, lambda c: c.código, "un cliente")
        borrador = Cliente(
            cliente.código,
            cliente.nombreCompleto if nombre is None else self._limpiar(nombre, "El nombre"),
            cliente.telefono if telefono is None else self._limpiar(telefono, "El teléfono"),
            cliente.correoElectronico if correo is None else self._limpiar(correo, "El correo"),
            cliente.tipoCliente if tipo is None else tipo,
        )
        cliente.nombreCompleto = borrador.nombreCompleto
        cliente.telefono = borrador.telefono
        cliente.correoElectronico = borrador.correoElectronico
        cliente.tipoCliente = borrador.tipoCliente
        return cliente

    def obtener_cliente(self, codigo: str) -> Optional[Cliente]:
        return self._obtener(self._clientes, codigo, lambda c: c.código)

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes)
    def registrar_tecnico(self, codigo: str, nombre: str, especialidad: str) -> Tecnico:
        especialidad = self._limpiar(especialidad, "La especialidad")
        if especialidad not in self.especialidades_validas():
            raise ValueError(
                f"Especialidad no válida. Opciones: {', '.join(self.especialidades_validas())}."
            )
        tecnico = Tecnico(
            self._limpiar(codigo, "El código"), self._limpiar(nombre, "El nombre"), especialidad
        )
        self._exigir_libre(self._tecnicos, tecnico.código, lambda t: t.código, "un técnico con código")
        self._tecnicos.append(tecnico)
        return tecnico

    def obtener_tecnico(self, codigo: str) -> Optional[Tecnico]:
        return self._obtener(self._tecnicos, codigo, lambda t: t.código)

    def listar_tecnicos(self) -> List[Tecnico]:
        return list(self._tecnicos)

    def registrar_equipo(self, tipo: TipoEquipo, codigo: str, serie: str, marca: str, modelo: str,
                         codigo_cliente: str, estado_fisico: str, accesorios: str, **extras) -> Equipo:
        if tipo not in self.CLASES_EQUIPO:
            raise ValueError("Tipo de equipo no válido.")
        propietario = self._exigir(self._clientes, codigo_cliente, lambda c: c.código, "un cliente")
        try:
            equipo = self.CLASES_EQUIPO[tipo](
                self._limpiar(codigo, "El código interno"), self._limpiar(serie, "El número de serie"),
                self._limpiar(marca, "La marca"), self._limpiar(modelo, "El modelo"),
                propietario, self._limpiar(estado_fisico, "El estado físico"),
                self._limpiar(accesorios, "Los accesorios"), **extras
            )
        except TypeError as ex:
            raise ValueError(f"Datos adicionales no válidos para {tipo.value}: {ex}")
        self._exigir_libre(self._equipos, equipo.codigoInterno, lambda e: e.codigoInterno, "un equipo con código interno")
        self._exigir_libre(self._equipos, equipo.numeroSerie, lambda e: e.numeroSerie, "un equipo con número de serie")
        self._equipos.append(equipo)
        return equipo

    def obtener_equipo(self, codigo: str) -> Optional[Equipo]:
        return self._obtener(self._equipos, codigo, lambda e: e.codigoInterno)

    def listar_equipos(self) -> List[Equipo]:
        return list(self._equipos)
    def registrar_repuesto(self, codigo: str, nombre: str, categoria: CategoriaRepuesto, existencia: int,
                           costo_unitario: float, precio_venta: float, existencia_minima: int = 1) -> Repuestos:
        repuesto = Repuestos(
            self._limpiar(codigo, "El código"), self._limpiar(nombre, "El nombre"), categoria,
            existencia, costo_unitario, precio_venta, existencia_minima
        )
        if repuesto.precioVenta < repuesto.costoUnitario:
            raise ValueError("El precio de venta no puede ser menor que el costo unitario.")
        self._exigir_libre(self._repuestos, repuesto.codigo, lambda r: r.codigo, "un repuesto con código")
        self._repuestos.append(repuesto)
        return repuesto

    def obtener_repuesto(self, codigo: str) -> Optional[Repuestos]:
        return self._obtener(self._repuestos, codigo, lambda r: r.codigo)

    def listar_repuestos(self) -> List[Repuestos]:
        return list(self._repuestos)

    def crear_solicitud(self, codigo: str, codigo_cliente: str, codigo_equipo: str,
                        descripcion: str, prioridad: NivelPrioridad = NivelPrioridad.NORMAL) -> Solicitud:
        codigo = self._limpiar(codigo, "El código de la solicitud")
        cliente = self._exigir(self._clientes, codigo_cliente, lambda c: c.código, "un cliente")
        equipo = self._exigir(self._equipos, codigo_equipo, lambda e: e.codigoInterno, "un equipo")
        if equipo.propietario is not cliente:
            raise ValueError("El equipo no pertenece al cliente indicado.")
        self._exigir_libre(self._solicitudes, codigo, lambda s: s.codigoSolicitud, "una solicitud con código")
        activa = self._solicitud_activa_de(equipo)
        if activa is not None:
            raise ValueError(f"El equipo ya tiene una solicitud activa ('{activa.codigoSolicitud}').")
        solicitud = Solicitud(codigo, cliente, equipo, descripcion, prioridad)
        self._solicitudes.append(solicitud)
        return solicitud

    def obtener_solicitud(self, codigo: str) -> Optional[Solicitud]:
        return self._obtener(self._solicitudes, codigo, lambda s: s.codigoSolicitud)

    def listar_solicitudes(self) -> List[Solicitud]:
        return list(self._solicitudes)
