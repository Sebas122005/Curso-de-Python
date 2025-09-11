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
            
    def __str__(self):
        datos=self.consulta_clientes()
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
    
    def consulta_clientes(self):
        cur = self.conexion.cursor()
        cur.execute("SELECT * FROM clientes")
        datos = cur.fetchall()
        cur.close()    
        return datos

    def inserta_clientes(self,codigo, nombre, ape_paterno, ape_materno,credito):
        cur = self.conexion.cursor() #Conectate
        sql='''INSERT INTO clientes (codigo, nombre, ape_paterno, ape_materno,credito) 
        VALUES('{}', '{}', '{}', '{}','{}')'''.format(codigo, nombre, ape_paterno, ape_materno,credito)
        cur.execute(sql)
        n=cur.rowcount  #==1  Inserto el elemento
        self.conexion.commit()   #ejecuta el commit 
        cur.close()
        return n   
    
    def elimina_clientes(self,codigo): #cliente vamos a eliminar 1
        cur = self.conexion.cursor() #Conectamos
        sql='''DELETE FROM clientes WHERE codigo = {}'''.format(codigo)
        cur.execute(sql)
        n=cur.rowcount #N==1
        self.conexion.commit()  #ejecuta la consulta  
        cur.close()
        return n    
    
    def modifica_clientes(self,nombre, ape_paterno, ape_materno,credito,codigo): #5
        cur = self.conexion.cursor()
        sql='''UPDATE clientes SET nombre='{}', ape_paterno='{}', ape_materno='{}',
        credito='{}' WHERE codigo={}'''.format(nombre, ape_paterno, ape_materno,credito,codigo)
        cur.execute(sql)
        n=cur.rowcount
        self.conexion.commit()    
        cur.close()
        return n   