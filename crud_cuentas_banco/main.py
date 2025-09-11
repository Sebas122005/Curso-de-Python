"""
Punto de entrada principal del sistema CRUD de cuentas bancarias.
Inicializa la aplicación y muestra la ventana principal.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import logging

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from database.connection import Database

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_bancario.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def verificar_conexion_bd():
    """
    Verifica la conexión a la base de datos.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        db = Database()
        db.connect()
        
        if db.connection and db.connection.open:
            # Probar la conexión con una consulta simple
            resultado = db.fetch_all("SELECT 1 as test")
            if resultado:
                logger.info("Conexión a la base de datos exitosa")
                db.disconnect()
                return True
            else:
                logger.error("Error al ejecutar consulta de prueba")
                db.disconnect()
                return False
        else:
            logger.error("No se pudo establecer conexión a la base de datos")
            return False
            
    except Exception as e:
        logger.error(f"Error al verificar conexión: {str(e)}")
        return False


def mostrar_error_conexion():
    """Muestra un mensaje de error de conexión."""
    mensaje = """
Error de Conexión a la Base de Datos

No se pudo conectar a la base de datos MySQL.

Por favor verifique:
1. Que MySQL esté ejecutándose
2. Que la base de datos 'banco_peru_db' exista
3. Que las credenciales en config/config.ini sean correctas
4. Que el usuario tenga permisos para acceder a la base de datos

Configuración actual:
- Host: localhost
- Puerto: 3306
- Base de datos: banco_peru_db
- Usuario: admin
    """
    
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    messagebox.showerror("Error de Conexión", mensaje)
    root.destroy()


def main():
    """Función principal de la aplicación."""
    try:
        logger.info("Iniciando Sistema CRUD de Cuentas Bancarias")
        
        # Verificar conexión a la base de datos
        if not verificar_conexion_bd():
            mostrar_error_conexion()
            return
        
        # Crear ventana principal
        root = tk.Tk()
        root.title("Sistema CRUD - Cuentas Bancarias")
        root.geometry("1000x700")
        
        # Configurar el ícono de la ventana (opcional)
        try:
            # root.iconbitmap('icono.ico')  # Descomentar si tienes un ícono
            pass
        except:
            pass
        
        # Crear y mostrar la ventana principal
        app = MainWindow(root)
        
        # Centrar la ventana
        root.update_idletasks()
        ancho = root.winfo_width()
        alto = root.winfo_height()
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()
        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2
        root.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        logger.info("Aplicación iniciada correctamente")
        
        # Iniciar el loop principal
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {str(e)}")
        messagebox.showerror("Error Crítico", f"Error crítico: {str(e)}")
    finally:
        logger.info("Aplicación finalizada")


if __name__ == "__main__":
    main()
