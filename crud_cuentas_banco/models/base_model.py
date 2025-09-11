"""
Modelo base para todas las entidades del sistema.
Proporciona funcionalidad CRUD básica y manejo de conexión a BD.
"""

from database.connection import Database
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseModel:
    """Clase base abstracta para todos los modelos del sistema."""
    
    def __init__(self):
        self.db = Database()
        self.db.connect()
        self.id = None
        self.fecha_creacion = None
        self.fecha_modificacion = None
    
    def __del__(self):
        """Cierra la conexión cuando se destruye el objeto."""
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()
    
    def validar_datos(self, datos):
        """
        Valida los datos antes de operaciones CRUD.
        Debe ser implementado por cada modelo específico.
        
        Args:
            datos (dict): Diccionario con los datos a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        raise NotImplementedError("Cada modelo debe implementar validar_datos")
    
    def crear(self, datos):
        """
        Crea un nuevo registro en la base de datos.
        
        Args:
            datos (dict): Diccionario con los datos del registro
            
        Returns:
            tuple: (exito, mensaje, id_nuevo)
        """
        try:
            # Validar datos
            es_valido, mensaje_error = self.validar_datos(datos)
            if not es_valido:
                return False, mensaje_error, None
            
            # Preparar datos para inserción
            datos_insert = self._preparar_datos_creacion(datos)
            
            # Ejecutar inserción
            query = self._generar_query_creacion()
            id_nuevo = self.db.execute_query(query, datos_insert)
            
            if id_nuevo:
                logger.info(f"Registro creado exitosamente con ID: {id_nuevo}")
                return True, "Registro creado exitosamente", id_nuevo
            else:
                return False, "Error al crear el registro", None
                
        except Exception as e:
            logger.error(f"Error al crear registro: {str(e)}")
            return False, f"Error al crear el registro: {str(e)}", None
    
    def leer(self, id_registro):
        """
        Lee un registro específico por ID.
        
        Args:
            id_registro (int): ID del registro a leer
            
        Returns:
            tuple: (exito, mensaje, datos)
        """
        try:
            query = self._generar_query_lectura()
            params = (id_registro,)
            resultado = self.db.fetch_all(query, params)
            
            if resultado:
                datos = self._formatear_datos_lectura(resultado[0])
                return True, "Registro encontrado", datos
            else:
                return False, "Registro no encontrado", None
                
        except Exception as e:
            logger.error(f"Error al leer registro: {str(e)}")
            return False, f"Error al leer el registro: {str(e)}", None
    
    def actualizar(self, id_registro, datos):
        """
        Actualiza un registro existente.
        
        Args:
            id_registro (int): ID del registro a actualizar
            datos (dict): Diccionario con los nuevos datos
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Validar datos
            es_valido, mensaje_error = self.validar_datos(datos)
            if not es_valido:
                return False, mensaje_error
            
            # Verificar que el registro existe
            existe, _, _ = self.leer(id_registro)
            if not existe:
                return False, "El registro no existe"
            
            # Preparar datos para actualización
            datos_update = self._preparar_datos_actualizacion(datos)
            datos_update['id'] = id_registro
            
            # Ejecutar actualización
            query = self._generar_query_actualizacion()
            filas_afectadas = self.db.execute_query(query, datos_update)
            
            if filas_afectadas:
                logger.info(f"Registro {id_registro} actualizado exitosamente")
                return True, "Registro actualizado exitosamente"
            else:
                return False, "No se pudo actualizar el registro"
                
        except Exception as e:
            logger.error(f"Error al actualizar registro: {str(e)}")
            return False, f"Error al actualizar el registro: {str(e)}"
    
    def eliminar(self, id_registro):
        """
        Elimina un registro de la base de datos.
        
        Args:
            id_registro (int): ID del registro a eliminar
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Verificar que el registro existe
            existe, _, _ = self.leer(id_registro)
            if not existe:
                return False, "El registro no existe"
            
            # Ejecutar eliminación
            query = self._generar_query_eliminacion()
            params = (id_registro,)
            filas_afectadas = self.db.execute_query(query, params)
            
            if filas_afectadas:
                logger.info(f"Registro {id_registro} eliminado exitosamente")
                return True, "Registro eliminado exitosamente"
            else:
                return False, "No se pudo eliminar el registro"
                
        except Exception as e:
            logger.error(f"Error al eliminar registro: {str(e)}")
            return False, f"Error al eliminar el registro: {str(e)}"
    
    def listar(self, filtros=None, limite=None, offset=None):
        """
        Lista todos los registros con filtros opcionales.
        
        Args:
            filtros (dict): Diccionario con filtros a aplicar
            limite (int): Número máximo de registros a retornar
            offset (int): Número de registros a omitir
            
        Returns:
            tuple: (exito, mensaje, lista_datos)
        """
        try:
            query, params = self._generar_query_listado(filtros, limite, offset)
            resultado = self.db.fetch_all(query, params)
            
            datos_formateados = [self._formatear_datos_lectura(fila) for fila in resultado]
            return True, "Lista obtenida exitosamente", datos_formateados
            
        except Exception as e:
            logger.error(f"Error al listar registros: {str(e)}")
            return False, f"Error al listar registros: {str(e)}", []
    
    # Métodos abstractos que deben ser implementados por cada modelo
    def _generar_query_creacion(self):
        """Genera la query SQL para crear un registro."""
        raise NotImplementedError("Cada modelo debe implementar _generar_query_creacion")
    
    def _generar_query_lectura(self):
        """Genera la query SQL para leer un registro."""
        raise NotImplementedError("Cada modelo debe implementar _generar_query_lectura")
    
    def _generar_query_actualizacion(self):
        """Genera la query SQL para actualizar un registro."""
        raise NotImplementedError("Cada modelo debe implementar _generar_query_actualizacion")
    
    def _generar_query_eliminacion(self):
        """Genera la query SQL para eliminar un registro."""
        raise NotImplementedError("Cada modelo debe implementar _generar_query_eliminacion")
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        """Genera la query SQL para listar registros."""
        raise NotImplementedError("Cada modelo debe implementar _generar_query_listado")
    
    def _preparar_datos_creacion(self, datos):
        """Prepara los datos para la operación de creación."""
        raise NotImplementedError("Cada modelo debe implementar _preparar_datos_creacion")
    
    def _preparar_datos_actualizacion(self, datos):
        """Prepara los datos para la operación de actualización."""
        raise NotImplementedError("Cada modelo debe implementar _preparar_datos_actualizacion")
    
    def _formatear_datos_lectura(self, fila):
        """Formatea los datos leídos de la base de datos."""
        raise NotImplementedError("Cada modelo debe implementar _formatear_datos_lectura")
