import random
import unicodedata
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from Entidades.Enum import TipoCliente, TipoEquipo, NivelPrioridad, CategoriaRepuesto, EstadoSolicitud


class GeneradorDatos:
    NOMBRES = ["Ana", "Luis", "María", "José", "Carla", "Pedro", "Sofía", "Diego", "Lucía", "Marco", "Elena", "Andrés"]
    APELLIDOS = ["Pérez", "García", "López", "Morales", "Ramírez", "Castillo", "Gómez", "Hernández", "Cifuentes", "Xicay"]
    ESTADOS_FISICOS = ["Bueno", "Rayones leves", "Golpe en la carcasa", "Desgaste normal", "Marcas de uso"]

    CATALOGO = {
        TipoEquipo.COMPUTADORA_PORTATIL: (
            [("HP", "Pavilion 15"), ("Dell", "Inspiron 14"), ("Lenovo", "IdeaPad 3"), ("Asus", "VivoBook 15")],
            "Cargador",
            ["No enciende", "Pantalla rota", "Batería no carga", "Muy lenta", "Se sobrecalienta"],
        ),
        TipoEquipo.COMPUTADORA_ESCRITORIO: (
            [("Dell", "OptiPlex 3080"), ("HP", "ProDesk 400"), ("Lenovo", "ThinkCentre M70")],
            "Cable de poder",
            ["No da video", "Reinicios constantes", "Disco lleno y lento", "Ruido fuerte en el ventilador"],
        ),
        TipoEquipo.IMPRESORA: (
            [("Epson", "L3150"), ("Canon", "G3110"), ("HP", "DeskJet 2775")],
            "Cable USB",
            ["No imprime", "Imprime con rayas", "Atasco de papel", "No reconoce la tinta"],
        ),
        TipoEquipo.CONSOLA: (
            [("Sony", "PlayStation 5"), ("Microsoft", "Xbox Series S"), ("Nintendo", "Switch")],
            "Control y cable HDMI",
            ["No enciende", "No da imagen", "El control no responde", "Se apaga sola"],
        ),
    }

    DIAGNOSTICOS = ["Componente dañado, requiere reemplazo", "Falla por suciedad y desgaste", "Problema de software",
                    "Conexión interna defectuosa", "Desgaste normal por uso"]

    REPUESTOS_BASE = [
        ("Memoria RAM 8GB", CategoriaRepuesto.MEMORIA_RAM, 250, 350,
         (TipoEquipo.COMPUTADORA_PORTATIL, TipoEquipo.COMPUTADORA_ESCRITORIO)),
        ("Disco SSD 480GB", CategoriaRepuesto.ALMACENAMIENTO, 300, 420,
         (TipoEquipo.COMPUTADORA_PORTATIL, TipoEquipo.COMPUTADORA_ESCRITORIO)),
        ("Pantalla 15.6 pulgadas", CategoriaRepuesto.PANTALLAS, 700, 950, (TipoEquipo.COMPUTADORA_PORTATIL,)),
        ("Fuente de poder 500W", CategoriaRepuesto.COMPONENTES_INTERNOS, 180, 260, (TipoEquipo.COMPUTADORA_ESCRITORIO,)),
        ("Botella de tinta", CategoriaRepuesto.PERIFERICOS, 40, 65, (TipoEquipo.IMPRESORA,)),
        ("Teclado USB", CategoriaRepuesto.PERIFERICOS, 60, 95,
         (TipoEquipo.COMPUTADORA_PORTATIL, TipoEquipo.COMPUTADORA_ESCRITORIO)),
        ("Cable HDMI", CategoriaRepuesto.ACCESORIOS_CONSOLAS, 25, 45, (TipoEquipo.CONSOLA,)),
        ("Control inalámbrico", CategoriaRepuesto.ACCESORIOS_CONSOLAS, 280, 380, (TipoEquipo.CONSOLA,)),
    ]

    ETAPAS_BASE = ["RECIBIDA", "EN_ESPERA", "ASIGNADA", "EN_DIAGNOSTICO",
                   "EN_REPARACION", "LISTA", "ENTREGADA", "CANCELADA"]
    ETAPAS_EXTRA = ["EN_ESPERA", "ASIGNADA", "EN_DIAGNOSTICO", "EN_REPARACION", "LISTA", "ENTREGADA", "ENTREGADA", "CANCELADA"]
    ETAPAS_CON_TECNICO = ("ASIGNADA", "EN_DIAGNOSTICO", "EN_REPARACION", "LISTA", "ENTREGADA")

    def __init__(self, gestor, semilla: Optional[int] = None):
        self._gestor = gestor
        self._azar = random.Random(semilla)
        self._contadores: Dict[str, int] = {}

    def _codigo(self, prefijo: str, existe) -> str:
        """Siguiente código libre del tipo PREFIJO-0001. Nunca repite uno existente."""
        n = self._contadores.get(prefijo, 0)
        while True:
            n += 1
            codigo = f"{prefijo}-{n:04d}"
            if not existe(codigo):
                self._contadores[prefijo] = n
                return codigo

    @staticmethod
    def _sin_tildes(texto: str) -> str:
        return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")

    def _crear_cliente(self):
        nombre = self._azar.choice(self.NOMBRES)
        apellido = self._azar.choice(self.APELLIDOS)
        telefono = f"{self._azar.choice([3, 4, 5])}{self._azar.randint(100, 999)}-{self._azar.randint(1000, 9999)}"
        correo = f"{self._sin_tildes(nombre).lower()}.{self._sin_tildes(apellido).lower()}{self._azar.randint(1, 99)}@correo.com"
        return self._gestor.registrar_cliente(
            self._codigo("CLI", self._gestor.obtener_cliente), f"{nombre} {apellido}", telefono, correo,
            self._azar.choice(list(TipoCliente)),
        )

    def _asegurar_base(self):
        while len(self._gestor.listar_clientes()) < 4:
            self._crear_cliente()
        for especialidad in self._gestor.especialidades_validas():
            existentes = 0
            for t in self._gestor.listar_tecnicos():
                if t.especialidad == especialidad:
                    existentes += 1
            for _ in range(2 - existentes):
                nombre = f"{self._azar.choice(self.NOMBRES)} {self._azar.choice(self.APELLIDOS)}"
                self._gestor.registrar_tecnico(self._codigo("TEC", self._gestor.obtener_tecnico), nombre, especialidad)
        nombres_existentes = [r.nombre for r in self._gestor.listar_repuestos()]
        for nombre, categoria, costo, precio, _tipos in self.REPUESTOS_BASE:
            if nombre in nombres_existentes:
                continue
            existencia = self._azar.randint(6, 15)
            minima = self._azar.randint(2, 3)
            if nombre == "Cable HDMI":
                existencia, minima = 0, 2
            elif nombre == "Control inalámbrico":
                existencia, minima = 2, 3
            self._gestor.registrar_repuesto(
                self._codigo("REP", self._gestor.obtener_repuesto), nombre, categoria,
                existencia, costo, precio, minima,
            )

    def _crear_equipo(self, tipo: TipoEquipo, cliente):
        modelos, accesorios, _problemas = self.CATALOGO[tipo]
        marca, modelo = self._azar.choice(modelos)
        extras = {}
        if tipo == TipoEquipo.COMPUTADORA_PORTATIL:
            extras = {"incluyeCargador": self._azar.random() < 0.8}
        elif tipo == TipoEquipo.COMPUTADORA_ESCRITORIO:
            extras = {"tipoGabinete": self._azar.choice(["Mid Tower", "Mini Tower", "Full Tower"])}
        elif tipo == TipoEquipo.IMPRESORA:
            extras = {"tipoInyeccion": self._azar.choice(["Tinta continua", "Cartucho", "Láser"])}
        elif tipo == TipoEquipo.CONSOLA:
            extras = {"cantidadMandos": self._azar.randint(1, 2)}
        codigo = self._codigo("EQ", self._gestor.obtener_equipo)
        serie = f"{self._sin_tildes(marca)[:3].upper()}-{self._azar.randint(100000, 999999)}-{codigo[-4:]}"
        return self._gestor.registrar_equipo(
            tipo, codigo, serie, marca, modelo, cliente.código,
            self._azar.choice(self.ESTADOS_FISICOS), accesorios, **extras
        )

    def _usar_repuestos(self, solicitud):
        """Entre 0 y 2 repuestos compatibles con el equipo. Si no alcanza el stock, se omite."""
        tipo = solicitud.equipo.tipoEquipo
        candidatos = []
        for nombre, _cat, _costo, _precio, tipos in self.REPUESTOS_BASE:
            if tipo in tipos:
                for r in self._gestor.listar_repuestos():
                    if r.nombre == nombre:
                        candidatos.append(r)
        for _ in range(self._azar.randint(0, 2)):
            if not candidatos:
                return
            repuesto = self._azar.choice(candidatos)
            try:
                self._gestor.usar_repuesto(solicitud.codigoSolicitud, repuesto.codigo, self._azar.randint(1, 2))
            except ValueError:
                pass

    def _avanzar(self, solicitud, etapa: str):
        codigo = solicitud.codigoSolicitud
        g = self._gestor
        if etapa == "ASIGNADA":
            return
        g.cambiar_estado(codigo, EstadoSolicitud.EN_DIAGNOSTICO)
        if etapa == "EN_DIAGNOSTICO":
            return
        g.registrar_diagnostico(codigo, self._azar.choice(self.DIAGNOSTICOS), self._azar.randrange(50, 301, 25))
        self._usar_repuestos(solicitud)
        if etapa == "EN_REPARACION" or (etapa in ("LISTA", "ENTREGADA") and self._azar.random() < 0.5):
            g.cambiar_estado(codigo, EstadoSolicitud.EN_REPARACION)
        if etapa == "EN_REPARACION":
            return
        g.cambiar_estado(codigo, EstadoSolicitud.LISTA_PARA_ENTREGAR)
        if etapa == "ENTREGADA":
            g.entregar_solicitud(codigo, self._azar.choice([2, 3, 4, 4, 5, 5]))

    def _plan_de_etapas(self, cantidad: int) -> List[str]:
        if cantidad <= len(self.ETAPAS_BASE):
            plan = list(self.ETAPAS_BASE)
            self._azar.shuffle(plan)
            return plan[:cantidad]
        plan = list(self.ETAPAS_BASE)
        for _ in range(cantidad - len(plan)):
            plan.append(self._azar.choice(self.ETAPAS_EXTRA))
        self._azar.shuffle(plan)
        return plan

    def generar(self, cantidad_solicitudes: int = 10) -> Dict:
        if isinstance(cantidad_solicitudes, bool) or not isinstance(cantidad_solicitudes, int) \
                or not (1 <= cantidad_solicitudes <= 100):
            raise ValueError("La cantidad de solicitudes debe ser un número entero entre 1 y 100.")
        g = self._gestor
        self._asegurar_base()
        plan = self._plan_de_etapas(cantidad_solicitudes)
        tipos = list(self.CATALOGO.keys())
        desplazamiento = self._azar.randrange(len(tipos))
        omitidas: List[str] = []
        creadas = []
        for i, etapa in enumerate(plan):
            cliente = self._azar.choice(g.listar_clientes())
            tipo = tipos[(i + desplazamiento) % len(tipos)]
            equipo = self._crear_equipo(tipo, cliente)
            prioridad = NivelPrioridad.URGENTE if self._azar.random() < 0.35 else NivelPrioridad.NORMAL
            solicitud = g.crear_solicitud(
                self._codigo("SOL", g.obtener_solicitud), cliente.código, equipo.codigoInterno,
                self._azar.choice(self.CATALOGO[tipo][2]), prioridad,
            )
            solicitud.fechaHoraRecepcion = datetime.now() - timedelta(
                days=self._azar.randint(0, 6), hours=self._azar.randint(0, 23), minutes=self._azar.randint(0, 59))
            creadas.append((solicitud, etapa))
        for solicitud, etapa in creadas:
            if etapa == "CANCELADA":
                if self._azar.random() < 0.5:
                    g.encolar_solicitud(solicitud.codigoSolicitud)
                g.cancelar_solicitud(solicitud.codigoSolicitud)
        por_asignar = {}
        for solicitud, etapa in creadas:
            if etapa in self.ETAPAS_CON_TECNICO:
                g.encolar_solicitud(solicitud.codigoSolicitud)
                por_asignar[solicitud.codigoSolicitud] = (solicitud, etapa)
        asignadas = []
        intentos = 0
        while por_asignar and intentos < 2 * (len(por_asignar) + 50):
            intentos += 1
            try:
                atendida, _tecnico = g.atender_siguiente(dia=self._azar.randrange(5))
            except ValueError as ex:
                cabeza = (g.listar_cola_urgente() + g.listar_cola_normal())
                if not cabeza:
                    break
                bloqueada = (g.listar_cola_urgente() or g.listar_cola_normal())[0]
                g.cancelar_solicitud(bloqueada.codigoSolicitud)
                omitidas.append(f"{bloqueada.codigoSolicitud}: cancelada por falta de técnico ({ex})")
                por_asignar.pop(bloqueada.codigoSolicitud, None)
                continue
            if atendida.codigoSolicitud in por_asignar:
                asignadas.append(por_asignar.pop(atendida.codigoSolicitud))
        for solicitud, etapa in asignadas:
            self._avanzar(solicitud, etapa)
        for solicitud, etapa in creadas:
            if etapa == "EN_ESPERA":
                g.encolar_solicitud(solicitud.codigoSolicitud)

        por_estado: Dict[str, int] = {}
        for solicitud, _etapa in creadas:
            nombre = solicitud.estado.value
            por_estado[nombre] = por_estado.get(nombre, 0) + 1
        return {"solicitudes_creadas": len(creadas), "por_estado": por_estado, "omitidas": omitidas}
