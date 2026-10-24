from Servicios.GestorXelaTech import GestorXelaTech

if __name__ == "__main__":
    gestor = GestorXelaTech()
    print("Gestor listo. Clientes registrados:", len(gestor.listar_clientes()))