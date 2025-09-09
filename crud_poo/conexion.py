# Coonfigurar la conexion a la base de datos MYSQL
# Conexion a la base de datos y consultas

# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error
#Conexion con MYSQL

class DAO:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='admin',
                password='admin',
                db='crud_poo'
            )
        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
        print('Conectado')
    
    def listarClientes(self):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor() # cursor es una palabra reservada
                cursor.execute("SELECT * FROM clientes ORDER BY codigo ASC")
                resultados = cursor.fetchall() # fetchall trae todos los registros y lo guarda en un Array
                return resultados
            except Error as e:
                print(f'Error al listar los clientes: {e}')
        else:
            print('No hay conexion a la base de datos')


cone= DAO()

print(cone.listarClientes())

