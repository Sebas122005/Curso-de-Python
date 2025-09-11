# Archivo: conexion.py
# Contiene la clase DAO para la gestión de la base de datos.

import pymysql
from pymysql.err import Error
import configparser

class DAO:
    def __init__(self):
        # 1. Leer el archivo de configuración
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
            db_config = config['database']
        except KeyError:
            print("Error: La sección 'database' no se encontró en 'config.ini'.")
            self.conexion = None
            return

        # 2. Usar los valores del archivo para la conexión
        try:
            self.conexion = pymysql.connect(
                host=db_config['host'],
                port=int(db_config['port']),
                user=db_config['user'],
                password=db_config['password'],
                db=db_config['db'],
            )
            print("Conexión establecida con éxito.")
        except Error as ex:
            print(f'Error al conectar: {ex}')
            self.conexion = None # Aseguramos que la conexión sea None si falla
    
    def listarClientes(self):
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute("SELECT * FROM clientes ORDER BY codigo ASC")
                resultados = cursor.fetchall()
                return resultados
            except Error as ex:
                print(f'Error al listar los clientes: {ex}')
                return None
        else:
            print('No hay conexión a la base de datos.')
            return None
    def insertarCliente(self, cliente):
        # Esta es la consulta parametrizada. Usamos %s como marcador de posición.
        sql = "INSERT INTO clientes (codigo, nombre, ape_paterno, ape_materno, credito) VALUES (%s, %s, %s, %s, %s)"
        
        # Los datos se pasan como una tupla, en el mismo orden que los marcadores de posición.
        # Aquí usamos los atributos del objeto Cliente.
        valores = (cliente.codigo, cliente.nombre, cliente.ape_paterno, cliente.ape_materno, cliente.credito)
        
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql, valores)
                self.conexion.commit() # Confirma la transacción para guardar los cambios en la BD.
                print("Cliente registrado con éxito.")
                return True
            except Error as ex:
                print(f"Error al registrar cliente: {ex}")
                self.conexion.rollback() # Revierte la transacción en caso de error.
                return False
        else:
            print("No hay conexión a la base de datos.")
            return False
        
    def actualizarCliente(self, cliente):
        # La consulta parametrizada con marcadores de posición (%s)
        sql = "UPDATE clientes SET nombre = %s, ape_paterno = %s, ape_materno = %s, credito = %s WHERE codigo = %s"
        
        # Los valores se pasan como una tupla en el orden correcto
        valores = (cliente.nombre, cliente.ape_paterno, cliente.ape_materno, cliente.credito, cliente.codigo)
        
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql, valores)
                self.conexion.commit() # Confirma la transacción
                print("Cliente actualizado con éxito.")
                return True
            except Error as ex:
                print(f"Error al actualizar cliente: {ex}")
                self.conexion.rollback() # Revierte la transacción en caso de error
                return False
        else:
            print("No hay conexión a la base de datos.")
            return False
    
    def eliminarCliente(self, codigo):
        # La consulta parametrizada con el marcador de posición para el código
        sql = "DELETE FROM clientes WHERE codigo = %s"
        
        # El valor se pasa como una tupla, incluso si es un solo valor.
        valores = (codigo,)
        
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql, valores)
                self.conexion.commit() # Confirma la transacción
                # Verificamos si se eliminó alguna fila
                if cursor.rowcount > 0:
                    print(f"Cliente con código {codigo} eliminado con éxito.")
                    return True
                else:
                    print(f"No se encontró un cliente con el código {codigo}.")
                    return False
            except Error as ex:
                print(f"Error al eliminar cliente: {ex}")
                self.conexion.rollback() # Revierte la transacción en caso de error
                return False
        else:
            print("No hay conexión a la base de datos.")
            return False
    
    def buscarClientePorCodigo(self, codigo):
        # Consulta parametrizada para buscar un cliente por su código.
        sql = "SELECT * FROM clientes WHERE codigo = %s"
        valores = (codigo,)
        
        if self.conexion:
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql, valores)
                # fetchone() devuelve una sola fila o None si no encuentra nada.
                resultado = cursor.fetchone() 
                return resultado
            except Error as ex:
                print(f"Error al buscar cliente: {ex}")
                return None
        else:
            print("No hay conexión a la base de datos.")
            return None