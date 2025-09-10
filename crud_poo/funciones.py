# Archivo: funciones.py
# Contiene funciones para interactuar con el DAO y el modelo Cliente.

from Cliente import Cliente

def listarClientes(dao_conexion):
    """
    Obtiene la lista de clientes de la base de datos y la muestra.
    """
    print('\nListado de Clientes:')
    
    # El método listarClientes del DAO devuelve una lista de tuplas o None
    clientes_raw = dao_conexion.listarClientes() 
    
    if clientes_raw: 
        for cliente_data in clientes_raw:
            try:
                # Crea un objeto Cliente con los datos de la tupla
                cliente_obj = Cliente(
                    cliente_data[0], # codigo
                    cliente_data[1], # nombre
                    cliente_data[2], # ape_paterno
                    cliente_data[3], # ape_materno
                    cliente_data[4]  # credito
                )
                print(cliente_obj) # Usa el método __str__ del objeto
            except Exception as e:
                print(f"Error al crear objeto Cliente: {e}")
        
        print('Fin del listado de clientes.')
        print('-------------------------')
    else:
        print('No hay clientes registrados o hubo un error en la consulta.')

def registrarCliente(dao_conexion):
    print("\n----- Registrar Nuevo Cliente -----")
    try:
        codigo = int(input("Ingresa el código del cliente: "))
        nombre = input("Ingresa el nombre: ")
        ape_paterno = input("Ingresa el apellido paterno: ")
        ape_materno = input("Ingresa el apellido materno: ")
        credito = int(input("Ingresa el crédito del cliente: "))
        
        # Crea una instancia del modelo Cliente
        cliente_nuevo = Cliente(codigo, nombre, ape_paterno, ape_materno, credito)
        
        # Llama al método del DAO para insertar el cliente en la base de datos
        dao_conexion.insertarCliente(cliente_nuevo)
        
    except ValueError:
        print("Entrada inválida. Asegúrate de ingresar números para el código y el crédito.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def actualizarCliente(dao_conexion):
    print("\n----- Actualizar Cliente Existente -----")
    try:
        codigo = int(input("Ingresa el CÓDIGO del cliente a actualizar: "))
        
        cliente_existente = dao_conexion.buscarClientePorCodigo(codigo)

        if cliente_existente:
            print(f"Cliente encontrado: {cliente_existente[1]}")
            
            nombre = input("Ingresa el nuevo nombre: ")
            ape_paterno = input("Ingresa el nuevo apellido paterno: ")
            ape_materno = input("Ingresa el nuevo apellido materno: ")
            credito = float(input("Ingresa el nuevo crédito: "))
            
            cliente_actualizado = Cliente(codigo, nombre, ape_paterno, ape_materno, credito)
            
            dao_conexion.actualizarCliente(cliente_actualizado)
        else:
            # 6. Si el cliente no existe, informa al usuario
            print(f"No se encontró un cliente con el código {codigo}.")
            
    except ValueError:
        print("Entrada inválida. El código y el crédito deben ser números.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def eliminarCliente(dao_conexion):
    print("\n----- Actualizar Cliente Existente -----")
    try:
        codigo = int(input("Ingresa el CÓDIGO del cliente a eliminar: "))
        
        cliente_existente = dao_conexion.buscarClientePorCodigo(codigo)

        if cliente_existente:
            print(f"Cliente eliminado: {cliente_existente[1]}")
            dao_conexion.eliminarCliente(codigo)
        else:
            print(f"No se encontró un cliente con el código {codigo}.")
        
    except ValueError:
        print("Entrada inválida. El código debe ser un número.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def buscarClientePorCodigo(dao_conexion):
    print("\n----- Buscar Cliente por Código -----")
    try:
        codigo = int(input("Ingresa el CÓDIGO del cliente a buscar: "))
        
        # Llama al método del DAO para buscar el cliente en la base de datos.
        cliente_data = dao_conexion.buscarClientePorCodigo(codigo)
        
        if cliente_data:
            # Crea un objeto Cliente con los datos encontrados.
            cliente_obj = Cliente(cliente_data[0], cliente_data[1], cliente_data[2], cliente_data[3], cliente_data[4])
            print("\nCliente encontrado:")
            print(cliente_obj) # Usa el método __str__ para mostrar los datos.
        else:
            print(f"No se encontró un cliente con el código {codigo}.")
            
    except ValueError:
        print("Entrada inválida. El código debe ser un número.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")