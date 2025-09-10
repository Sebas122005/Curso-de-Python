# Archivo: master.py
# Contiene el menú principal y la lógica de control.

import os
from conexion import DAO
import funciones as fn

def menu_principal():
    os.system('cls' if os.name == 'nt' else 'clear') # Limpiar consola
    print("----- Menú Principal -----")
    print("1. Listar Clientes")
    print("2. Registrar Cliente")
    print("3. Actualizar Cliente")
    print("4. Eliminar Cliente")
    print("5. Buscar Cliente por Código") # <-- Nueva opción
    print("6. Salir")
    opcion = input("Selecciona una opción: ")
    return opcion

def main():
    dao = DAO()
    if dao.conexion is not None:
        while True:
            opcion = menu_principal()
            
            if opcion == '1':
                fn.listarClientes(dao)
            elif opcion == '2':
                fn.registrarCliente(dao)
            elif opcion == '3':
                fn.actualizarCliente(dao)
            elif opcion == '4':
                fn.eliminarCliente(dao)
            elif opcion == '5': #
                fn.buscarClientePorCodigo(dao)
            elif opcion == '6':
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")
    else:
        print("Saliendo del programa debido a un error de conexión con la base de datos.")

if __name__ == '__main__':
    main()
