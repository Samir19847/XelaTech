from datetime import datetime
from typing import List, Optional, Callable, Any, Dict, Tuple
from Entidades.Cliente import Cliente
from Entidades.Técnicos import Tecnico
from Entidades.Equipo import Equipo
from Entidades.ComputadoraPortatil import ComputadoraPortatil
from Entidades.ComputadoraEscritorio import ComputadoraEscritorio
from Entidades.Impresora import Impresora
from Entidades.Consola import Consola
from Entidades.Repuestos import Repuestos
from Entidades.Solicitudes import Solicitud
from Entidades.Enum import TipoCliente, TipoEquipo, NivelPrioridad, CategoriaRepuesto, EstadoSolicitud
from Estructuras.ColaSolicitudes import ColaSolicitudes
from Estructuras.MatrizCargaSemanal import MatrizCargaSemanal
from Estructuras.EstadisticasCalificaciones import EstadisticasCalificaciones
from Algoritmos.AlgoritmosBusqueda import AlgoritmosBusqueda
from Algoritmos.AlgoritmosOrdenamiento import AlgoritmosOrdenamiento


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
        # Estructuras del flujo de atención
        self._cola = ColaSolicitudes()
        self._matriz = MatrizCargaSemanal([])
        self._estadisticas = EstadisticasCalificaciones()
        self._asignaciones: Dict[str, Tuple[int, int]] = {}

    @staticmethod
    def _limpiar(valor: Any, campo: str) -> str:
        if not isinstance(valor, str):
            raise ValueError(f"{campo} debe ser texto.")
        return valor.strip()

    @staticmethod
    def _obtener(lista: List[Any], valor: str, key: Callable[[Any], str]) -> Optional[Any]:
        """Búsqueda secuencial exacta (sin distinguir mayúsculas) sobre datos reales."""
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

    def _exigir_solicitud(self, codigo: str) -> Solicitud:
        return self._exigir(self._solicitudes, codigo, lambda s: s.codigoSolicitud, "una solicitud")

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
        self._matriz.agregar_tecnico(tecnico)
        return tecnico

    def establecer_disponibilidad(self, codigo: str, disponible: bool) -> Tecnico:
        tecnico = self._exigir(self._tecnicos, codigo, lambda t: t.código, "un técnico")
        tecnico.disponible = disponible
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

    def historial_de(self, codigo: str) -> List[EstadoSolicitud]:
        return self._exigir_solicitud(codigo).historialEstados


    def encolar_solicitud(self, codigo: str) -> Solicitud:
        solicitud = self._exigir_solicitud(codigo)
        if solicitud.estado != EstadoSolicitud.RECIBIDA:
            raise ValueError(
                f"Solo se puede encolar una solicitud 'Recibida' (estado actual: '{solicitud.estado.value}')."
            )
        solicitud.CambiarEstado(EstadoSolicitud.EN_ESPERA)
        self._cola.Encolar(solicitud)
        return solicitud

    def _elegir_tecnico(self, equipo: Equipo) -> Optional[Tecnico]:
        elegido = None
        for tecnico in self._tecnicos:
            if tecnico.especialidad == equipo.especialidadRequerida and tecnico.puede_recibir_solicitud():
                if elegido is None or tecnico.trabajosActivos < elegido.trabajosActivos:
                    elegido = tecnico
        return elegido

    @staticmethod
    def _indice_dia(dia: Optional[int]) -> int:
        dias = len(MatrizCargaSemanal.DIAS_SEMANA)
        if dia is None:
            hoy = datetime.now().weekday()
            return hoy if hoy < dias else 0
        if isinstance(dia, bool) or not isinstance(dia, int) or not (0 <= dia < dias):
            raise ValueError(f"El día debe ser un número entre 0 (lunes) y {dias - 1} (viernes).")
        return dia

    def atender_siguiente(self, dia: Optional[int] = None) -> Tuple[Solicitud, Tecnico]:
        indice_dia = self._indice_dia(dia)
        solicitud = self._cola.Siguiente()
        if solicitud is None:
            raise ValueError("No hay solicitudes en espera.")
        tecnico = self._elegir_tecnico(solicitud.equipo)
        if tecnico is None:
            raise ValueError(
                f"No hay técnico disponible con especialidad '{solicitud.equipo.especialidadRequerida}'. "
                f"La solicitud '{solicitud.codigoSolicitud}' sigue en la cola."
            )
        solicitud.asignar_tecnico(tecnico)
        self._cola.Desencolar() 
        indice_tecnico = self._tecnicos.index(tecnico)
        self._matriz.registrar_asignacion(indice_tecnico, indice_dia)
        self._asignaciones[solicitud.codigoSolicitud] = (indice_tecnico, indice_dia)
        return solicitud, tecnico

    def cambiar_estado(self, codigo: str, nuevo_estado: EstadoSolicitud) -> Solicitud:
        solicitud = self._exigir_solicitud(codigo)
        if nuevo_estado in (EstadoSolicitud.EN_ESPERA, EstadoSolicitud.ASIGNADA):
            raise ValueError("Ese cambio se hace con encolar_solicitud() y atender_siguiente().")
        if nuevo_estado == EstadoSolicitud.ENTREGADA:
            raise ValueError("Para entregar use entregar_solicitud() (requiere calificación).")
        if nuevo_estado == EstadoSolicitud.CANCELADA:
            raise ValueError("Para cancelar use cancelar_solicitud().")
        if nuevo_estado == EstadoSolicitud.LISTA_PARA_ENTREGAR:
            solicitud.finalizar_solicitud()
        else:
            solicitud.CambiarEstado(nuevo_estado)
        return solicitud

    def registrar_diagnostico(self, codigo: str, diagnostico: str, costo_mano_obra: float) -> Solicitud:
        solicitud = self._exigir_solicitud(codigo)
        diagnostico = self._limpiar(diagnostico, "El diagnóstico")
        if not diagnostico:
            raise ValueError("El diagnóstico no puede estar vacío.")
        if solicitud.estado not in (EstadoSolicitud.EN_DIAGNOSTICO, EstadoSolicitud.EN_REPARACION):
            raise ValueError(
                f"Solo se registra diagnóstico en 'En diagnóstico' o 'En reparación' (estado actual: '{solicitud.estado.value}')."
            )
        solicitud.costoManoObra = costo_mano_obra
        solicitud.diagnostico = diagnostico
        return solicitud

    def usar_repuesto(self, codigo_solicitud: str, codigo_repuesto: str, cantidad: int) -> Optional[str]:
        solicitud = self._exigir_solicitud(codigo_solicitud)
        repuesto = self._exigir(self._repuestos, codigo_repuesto, lambda r: r.codigo, "un repuesto")
        solicitud.agregar_repuesto(repuesto, cantidad)
        if repuesto.bajoMinimo:
            estado = "AGOTADO" if repuesto.existencia == 0 else "en o por debajo del mínimo"
            return (f"ALERTA DE STOCK: '{repuesto.nombre}' está {estado} "
                    f"(existencia: {repuesto.existencia}, mínimo: {repuesto.existenciaMinima}).")
        return None

    def entregar_solicitud(self, codigo: str, calificacion: int) -> Solicitud:
        """Lista para entregar -> Entregada. Registra la calificación del técnico."""
        solicitud = self._exigir_solicitud(codigo)
        solicitud.registrar_entrega(calificacion)
        self._estadisticas.RegistrarCalificaciones(calificacion)
        return solicitud

    def cancelar_solicitud(self, codigo: str) -> Solicitud:
        solicitud = self._exigir_solicitud(codigo)
        estaba_en_cola = solicitud.estado == EstadoSolicitud.EN_ESPERA
        solicitud.cancelar_solicitud()
        if estaba_en_cola:
            self._cola.Quitar(solicitud)
        return solicitud

    def deshacer_ultimo_cambio(self, codigo: str) -> Solicitud:
        solicitud = self._exigir_solicitud(codigo)
        estado_antes = solicitud.estado
        asignacion = self._asignaciones.get(codigo) if estado_antes == EstadoSolicitud.ASIGNADA else None
        solicitud.DeshacerEstado()
        if estado_antes == EstadoSolicitud.ASIGNADA:
            if asignacion is not None:
                self._matriz.quitar_asignacion(*asignacion)
                del self._asignaciones[codigo]
            if solicitud.estado == EstadoSolicitud.EN_ESPERA:
                self._cola.EncolarAlFrente(solicitud)
        elif estado_antes == EstadoSolicitud.EN_ESPERA:
            self._cola.Quitar(solicitud)
        return solicitud

    def listar_cola_urgente(self) -> List[Solicitud]:
        return self._cola.ObtenerSolicitudesUrgentes()

    def listar_cola_normal(self) -> List[Solicitud]:
        return self._cola.ObtenerSolicitudesNormales()

    def matriz_carga(self) -> Tuple[List[str], List[str], List[List[int]]]:
        return self._matriz.obtener_matriz_completa()

    def resumen_carga(self) -> Dict:
        return self._matriz.resumen_carga()

    def pico_de_carga(self) -> Dict:
        return self._matriz.obtener_pico_de_carga()

    def estadisticas_calificaciones(self) -> Dict:
        return {
            "arreglo": self._estadisticas.ObtenerArreglo(),
            "conteo": self._estadisticas.ObtenerResumenConteo(),
            "promedio": self._estadisticas.ObtenerPromedio(),
        }

    @staticmethod
    def _resultado_orden(algoritmo: str, criterio: str, descendente: bool, datos: List[Any]) -> Dict:
        return {
            "algoritmo": algoritmo,
            "criterio": criterio,
            "orden": "descendente" if descendente else "ascendente",
            "descripcion": AlgoritmosOrdenamiento.describir_ordenamiento(algoritmo, criterio, descendente),
            "datos": datos,
        }

    def ordenar_solicitudes_por_costo(self, descendente: bool = True) -> Dict:
        AlgoritmosOrdenamiento.exigir_datos_suficientes(self._solicitudes, 2, "solicitudes")
        datos = AlgoritmosOrdenamiento.bubble_sort(self._solicitudes, key=lambda s: s.total, descendente=descendente)
        return self._resultado_orden(AlgoritmosOrdenamiento.BUBBLE_SORT, "Costo total", descendente, datos)

    def ordenar_tecnicos_por_servicios(self, descendente: bool = True) -> Dict:
        AlgoritmosOrdenamiento.exigir_datos_suficientes(self._tecnicos, 2, "técnicos")
        datos = AlgoritmosOrdenamiento.selection_sort(self._tecnicos, key=lambda t: t.serviciosFinalizados, descendente=descendente)
        return self._resultado_orden(AlgoritmosOrdenamiento.SELECTION_SORT, "Servicios finalizados", descendente, datos)

    def ordenar_repuestos_por_existencia(self, descendente: bool = False) -> Dict:
        AlgoritmosOrdenamiento.exigir_datos_suficientes(self._repuestos, 2, "repuestos")
        datos = AlgoritmosOrdenamiento.shell_sort(self._repuestos, key=lambda r: r.existencia, descendente=descendente)
        return self._resultado_orden(AlgoritmosOrdenamiento.SHELL_SORT, "Existencia disponible", descendente, datos)

    def ordenar_solicitudes_por_fecha(self, descendente: bool = False) -> Dict:
        AlgoritmosOrdenamiento.exigir_datos_suficientes(self._solicitudes, 2, "solicitudes")
        datos = AlgoritmosOrdenamiento.quick_sort(self._solicitudes, key=lambda s: s.fechaHoraRecepcion, descendente=descendente)
        return self._resultado_orden(AlgoritmosOrdenamiento.QUICK_SORT, "Fecha de recepción", descendente, datos)


    def buscar_clientes_por_nombre(self, texto: str) -> List[Cliente]:
        texto = self._limpiar(texto, "El texto de búsqueda")
        if not texto:
            raise ValueError("Escriba el texto a buscar.")
        return AlgoritmosBusqueda.busqueda_secuencial(
            self._clientes, texto, key=lambda c: c.nombreCompleto, busqueda_parcial=True
        )

    def buscar_solicitudes_por_estado(self, estado: EstadoSolicitud) -> List[Solicitud]:
        if not isinstance(estado, EstadoSolicitud):
            raise ValueError("Seleccione un estado válido.")
        return AlgoritmosBusqueda.busqueda_secuencial(
            self._solicitudes, estado.value, key=lambda s: s.estado.value, busqueda_parcial=False
        )

    def buscar_equipos_por_marca(self, texto: str) -> List[Equipo]:
        texto = self._limpiar(texto, "La marca")
        if not texto:
            raise ValueError("Escriba la marca a buscar.")
        return AlgoritmosBusqueda.busqueda_secuencial(
            self._equipos, texto, key=lambda e: e.marca, busqueda_parcial=True
        )

    def buscar_solicitud_binaria(self, codigo: str, ordenar_antes: bool = True) -> Optional[Solicitud]:
        codigo = self._limpiar(codigo, "El código")
        if not codigo:
            raise ValueError("Escriba el código a buscar.")
        if not self._solicitudes:
            raise ValueError("No hay solicitudes registradas.")
        clave = lambda s: s.codigoSolicitud.lower()
        if ordenar_antes:
            datos = AlgoritmosOrdenamiento.shell_sort(self._solicitudes, key=clave)
        else:
            datos = list(self._solicitudes)
        return AlgoritmosBusqueda.busqueda_binaria(datos, codigo.lower(), key=clave)
