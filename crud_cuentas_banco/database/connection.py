import pymysql
import configparser

class Database:
    """Clase para gestionar la conexión a la base de datos con PyMySQL y un archivo de configuración."""

    def __init__(self):
        self.connection = None
        self.config = {}
        self.load_config()

    def load_config(self):
        """Lee los datos de conexión del archivo config.ini."""
        config_parser = configparser.ConfigParser()
        try:
            config_parser.read('config/config.ini')
            self.config = {
                'user': config_parser.get('mysql_config', 'user'),
                'password': config_parser.get('mysql_config', 'password'),
                'host': config_parser.get('mysql_config', 'host'),
                'database': config_parser.get('mysql_config', 'db'),
                'port': config_parser.getint('mysql_config', 'port')
            }
        except (configparser.Error, FileNotFoundError) as e:
            print(f"Error al leer el archivo de configuración: {e}")
            self.config = None

    def connect(self):
        """Establece la conexión con la base de datos."""
        if not self.config:
            print("No se pudo cargar la configuración de la base de datos.")
            return

        try:
            self.connection = pymysql.connect(**self.config)
            print("Conexión a la base de datos exitosa.")
        except pymysql.MySQLError as err:
            print(f"Error de conexión: {err}")
            self.connection = None

    def disconnect(self):
        """Cierra la conexión con la base de datos."""
        if self.connection and self.connection.open:
            self.connection.close()
            print("Conexión a la base de datos cerrada.")
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL con seguridad."""
        if not self.connection or not self.connection.open:
            print("No hay conexión a la base de datos.")
            return None
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except pymysql.MySQLError as err:
            self.connection.rollback()
            print(f"Error al ejecutar la consulta: {err}")
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """Ejecuta una consulta y devuelve todos los resultados."""
        if not self.connection or not self.connection.open:
            print("No hay conexión a la base de datos.")
            return []

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Error al obtener los datos: {err}")
            return []
        finally:
            cursor.close()
