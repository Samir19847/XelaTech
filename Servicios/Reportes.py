from typing import Dict, List, Optional, Tuple
from Entidades.Enum import EstadoSolicitud, TipoEquipo
from Entidades.Solicitudes import Solicitud

FORMATO_FECHA = "%Y-%m-%d %H:%M"

def _q(valor: float) -> str:
    return f"Q{valor:,.2f}"

class Reportes:
    TITULOS = {
        1: "Solicitudes en espera separadas por prioridad",
        2: "Solicitudes activas, finalizadas y canceladas",
        3: "Técnicos disponibles y técnicos con carga completa",
        4: "Técnico con más servicios finalizados",
        5: "Equipos atendidos por tipo",
        6: "Solicitudes ordenadas por costo total",
        7: "Solicitudes ordenadas por fecha de recepción",
        8: "Repuestos ordenados por existencia",
        9: "Repuestos con existencia mínima o agotados",
        10: "Ingresos totales por servicios finalizados",
        11: "Resultados de las búsquedas",
        12: "Matriz semanal de carga de trabajo",
    }
    ESTADOS_ATENDIDOS = (EstadoSolicitud.ASIGNADA, EstadoSolicitud.EN_DIAGNOSTICO, EstadoSolicitud.EN_REPARACION,
                         EstadoSolicitud.LISTA_PARA_ENTREGAR, EstadoSolicitud.ENTREGADA)

    def __init__(self, gestor):
        self._g = gestor

    def catalogo(self) -> List[Tuple[int, str]]:
        """(número, título) de los reportes que no necesitan parámetros (todos menos el 11)."""
        return [(n, t) for n, t in self.TITULOS.items() if n != 11]

    def ejecutar(self, numero: int) -> Dict:
        metodos = {1: self.solicitudes_en_espera_por_prioridad, 2: self.solicitudes_por_situacion,
                   3: self.tecnicos_disponibles_y_con_carga_completa, 4: self.tecnico_con_mas_servicios,
                   5: self.equipos_atendidos_por_tipo, 6: self.solicitudes_por_costo_total,
                   7: self.solicitudes_por_fecha, 8: self.repuestos_por_existencia,
                   9: self.repuestos_en_minimo_o_agotados, 10: self.ingresos_por_servicios_finalizados,
                   12: self.matriz_carga_semanal}
        if numero not in metodos:
            raise ValueError("Número de reporte no válido (el 11 se ejecuta con sus parámetros).")
        return metodos[numero]()

    def _reporte(self, numero: int, encabezados: List[str], filas: List[List], notas: List[str]) -> Dict:
        return {"numero": numero, "titulo": self.TITULOS[numero],
                "encabezados": encabezados, "filas": filas, "notas": notas}

    @staticmethod
    def _equipo_texto(solicitud: Solicitud) -> str:
        e = solicitud.equipo
        return f"{e.marca} {e.modelo} ({e.tipoEquipo.value})"

    def solicitudes_en_espera_por_prioridad(self) -> Dict:
        urgentes = self._g.listar_cola_urgente()
        normales = self._g.listar_cola_normal()
        filas = []
        for prioridad, grupo in (("Urgente", urgentes), ("Normal", normales)):
            for s in grupo:
                filas.append([prioridad, s.codigoSolicitud, s.cliente.nombreCompleto, self._equipo_texto(s),
                              s.fechaHoraRecepcion.strftime(FORMATO_FECHA)])
        notas = [f"Urgentes en espera: {len(urgentes)}", f"Normales en espera: {len(normales)}",
                 "Orden de atención: primero las urgentes, luego las normales, por orden de llegada."]
        return self._reporte(1, ["Prioridad", "Código", "Cliente", "Equipo", "Recepción"], filas, notas)

    def solicitudes_por_situacion(self) -> Dict:
        solicitudes = self._g.listar_solicitudes()
        grupos = {"Activa": [], "Finalizada": [], "Cancelada": []}
        for s in solicitudes:
            if s.estado == EstadoSolicitud.ENTREGADA:
                grupos["Finalizada"].append(s)
            elif s.estado == EstadoSolicitud.CANCELADA:
                grupos["Cancelada"].append(s)
            else:
                grupos["Activa"].append(s)
        filas = []
        for situacion in ("Activa", "Finalizada", "Cancelada"):
            for s in grupos[situacion]:
                filas.append([situacion, s.codigoSolicitud, s.cliente.nombreCompleto, s.estado.value, _q(s.total)])
        notas = [f"Activas: {len(grupos['Activa'])} | Finalizadas (entregadas): {len(grupos['Finalizada'])} | "
                 f"Canceladas: {len(grupos['Cancelada'])} | Total: {len(solicitudes)}"]
        return self._reporte(2, ["Situación", "Código", "Cliente", "Estado", "Total"], filas, notas)

    def tecnicos_disponibles_y_con_carga_completa(self) -> Dict:
        filas = []
        disponibles = completos = 0
        for t in self._g.listar_tecnicos():
            if t.cargaCompleta:
                situacion = "Carga completa"
                completos += 1
            elif t.disponible:
                situacion = "Disponible"
                disponibles += 1
            else:
                situacion = "No disponible"
            filas.append([t.código, t.nombreCompleto, t.especialidad, t.trabajosActivos, situacion])
        notas = [f"Disponibles: {disponibles} | Con carga completa: {completos} | "
                 f"Límite de trabajos activos por técnico: 3"]
        return self._reporte(3, ["Código", "Técnico", "Especialidad", "Trabajos activos", "Situación"], filas, notas)

    def tecnico_con_mas_servicios(self) -> Dict:
        resultado = self._g.ordenar_tecnicos_por_servicios(descendente=True)
        tecnicos = resultado["datos"]
        filas = []
        for posicion, t in enumerate(tecnicos, start=1):
            filas.append([posicion, t.código, t.nombreCompleto, t.especialidad, t.serviciosFinalizados,
                          f"{t.calificacionPromedio:.2f}"])
        mayor = tecnicos[0].serviciosFinalizados
        notas = [resultado["descripcion"]]
        if mayor == 0:
            notas.append("Todavía no hay servicios finalizados.")
        else:
            lideres = [t.nombreCompleto for t in tecnicos if t.serviciosFinalizados == mayor]
            notas.append(f"Técnico con más servicios finalizados ({mayor}): {', '.join(lideres)}")
        return self._reporte(4, ["Puesto", "Código", "Técnico", "Especialidad", "Servicios finalizados",
                                 "Calificación promedio"], filas, notas)

    def equipos_atendidos_por_tipo(self) -> Dict:
        tipos = list(TipoEquipo)
        conteo = [0] * len(tipos)
        vistos = []
        for s in self._g.listar_solicitudes():
            ya_contado = False
            for equipo in vistos:
                if equipo is s.equipo:
                    ya_contado = True
            if s.estado in self.ESTADOS_ATENDIDOS and not ya_contado:
                vistos.append(s.equipo)
                conteo[tipos.index(s.equipo.tipoEquipo)] += 1
        filas = [[tipos[i].value, conteo[i]] for i in range(len(tipos))]
        total = 0
        for c in conteo:
            total += c
        notas = [f"Total de equipos atendidos: {total}",
                 "Atendido = su solicitud ya fue asignada a un técnico (de 'Asignada' en adelante, sin contar canceladas)."]
        return self._reporte(5, ["Tipo de equipo", "Equipos atendidos"], filas, notas)

    def solicitudes_por_costo_total(self, descendente: bool = True) -> Dict:
        resultado = self._g.ordenar_solicitudes_por_costo(descendente)
        filas = []
        for s in resultado["datos"]:
            filas.append([s.codigoSolicitud, s.cliente.nombreCompleto, s.estado.value,
                          _q(s.equipo.calcular_costo_revision()), _q(s.costoManoObra), _q(s.costoRepuestos), _q(s.total)])
        return self._reporte(6, ["Código", "Cliente", "Estado", "Revisión", "Mano de obra", "Repuestos", "Total"],
                             filas, [resultado["descripcion"]])

    def solicitudes_por_fecha(self, descendente: bool = False) -> Dict:
        resultado = self._g.ordenar_solicitudes_por_fecha(descendente)
        filas = []
        for s in resultado["datos"]:
            filas.append([s.fechaHoraRecepcion.strftime(FORMATO_FECHA), s.codigoSolicitud,
                          s.cliente.nombreCompleto, s.prioridad.value, s.estado.value])
        return self._reporte(7, ["Recepción", "Código", "Cliente", "Prioridad", "Estado"], filas,
                             [resultado["descripcion"]])

    def repuestos_por_existencia(self, descendente: bool = False) -> Dict:
        resultado = self._g.ordenar_repuestos_por_existencia(descendente)
        filas = []
        for r in resultado["datos"]:
            filas.append([r.codigo, r.nombre, r.categoria.value, r.existencia, r.existenciaMinima,
                          "AGOTADO" if r.existencia == 0 else ("Mínimo o menos" if r.bajoMinimo else "Normal")])
        return self._reporte(8, ["Código", "Repuesto", "Categoría", "Existencia", "Mínima", "Estado"], filas,
                             [resultado["descripcion"]])

    def repuestos_en_minimo_o_agotados(self) -> Dict:
        filas = []
        agotados = 0
        for r in self._g.listar_repuestos():
            if r.bajoMinimo:
                if r.existencia == 0:
                    agotados += 1
                filas.append([r.codigo, r.nombre, r.existencia, r.existenciaMinima,
                              "AGOTADO" if r.existencia == 0 else "En el mínimo o por debajo"])
        notas = [f"Repuestos en mínimo o agotados: {len(filas)} (agotados: {agotados})"]
        return self._reporte(9, ["Código", "Repuesto", "Existencia", "Mínima", "Situación"], filas, notas)

    def ingresos_por_servicios_finalizados(self) -> Dict:
        filas = []
        total = 0.0
        for s in self._g.listar_solicitudes():
            if s.estado == EstadoSolicitud.ENTREGADA:
                filas.append([s.codigoSolicitud, s.cliente.nombreCompleto, _q(s.equipo.calcular_costo_revision()),
                              _q(s.costoManoObra), _q(s.costoRepuestos), _q(s.total)])
                total += s.total
        notas = [f"Servicios finalizados (entregados): {len(filas)}", f"Ingresos totales: {_q(total)}"]
        return self._reporte(10, ["Código", "Cliente", "Revisión", "Mano de obra", "Repuestos", "Total"], filas, notas)

    def busquedas(self, nombre_cliente: Optional[str] = None, estado: Optional[EstadoSolicitud] = None,
                  marca: Optional[str] = None, codigo: Optional[str] = None) -> Dict:
        """Ejecuta las búsquedas para las que se dio un criterio y muestra todos los resultados."""
        filas = []
        if nombre_cliente:
            coincidencias = self._g.buscar_clientes_por_nombre(nombre_cliente)
            for c in coincidencias:
                filas.append(["Secuencial: cliente por nombre", nombre_cliente, f"{c.código} - {c.nombreCompleto}"])
            if not coincidencias:
                filas.append(["Secuencial: cliente por nombre", nombre_cliente, "(sin coincidencias)"])
        if estado is not None:
            coincidencias = self._g.buscar_solicitudes_por_estado(estado)
            for s in coincidencias:
                filas.append(["Secuencial: solicitud por estado", estado.value, f"{s.codigoSolicitud} - {s.cliente.nombreCompleto}"])
            if not coincidencias:
                filas.append(["Secuencial: solicitud por estado", estado.value, "(sin coincidencias)"])
        if marca:
            coincidencias = self._g.buscar_equipos_por_marca(marca)
            for e in coincidencias:
                filas.append(["Secuencial: equipo por marca", marca, f"{e.codigoInterno} - {e.marca} {e.modelo}"])
            if not coincidencias:
                filas.append(["Secuencial: equipo por marca", marca, "(sin coincidencias)"])
        if codigo:
            s = self._g.buscar_solicitud_binaria(codigo)
            filas.append(["Binaria: solicitud por código", codigo,
                          f"{s.codigoSolicitud} - {s.cliente.nombreCompleto} ({s.estado.value})" if s else "(no encontrada)"])
        if not filas:
            raise ValueError("Indique al menos un criterio de búsqueda.")
        return self._reporte(11, ["Búsqueda", "Criterio", "Resultado"], filas,
                             [f"Resultados encontrados: {len(filas)}"])

    def matriz_carga_semanal(self) -> Dict:
        nombres, dias, matriz = self._g.matriz_carga()
        filas = []
        for i in range(len(nombres)):
            total = 0
            for valor in matriz[i]:
                total += valor
            filas.append([nombres[i]] + list(matriz[i]) + [total])
        totales_dia = [0] * len(dias)
        for fila in matriz:
            for j in range(len(dias)):
                totales_dia[j] += fila[j]
        gran_total = 0
        for t in totales_dia:
            gran_total += t
        filas.append(["TOTAL POR DÍA"] + totales_dia + [gran_total])
        resumen = self._g.resumen_carga()
        pico = self._g.pico_de_carga()
        notas = [f"Técnico con más carga en la semana: {resumen['Técnico']} ({resumen['Total_técnico']} solicitudes)",
                 f"Día con más carga: {resumen['Día']} ({resumen['Total_día']} solicitudes)",
                 f"Mayor carga en una sola celda: {pico['Técnico']} el {pico['Día']} ({pico['Máx_carga']})"]
        return self._reporte(12, ["Técnico"] + dias + ["Total"], filas, notas)
