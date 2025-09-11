"""
Controlador base para todos los controladores del sistema.
Proporciona funcionalidad común y manejo de errores.
"""

import logging
from typing import Dict, List, Tuple, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseController:
    """Clase base abstracta para todos los controladores del sistema."""
    
    def __init__(self, modelo):
        """
        Inicializa el controlador con un modelo específico.
        
        Args:
            modelo: Instancia del modelo correspondiente
        """
        self.modelo = modelo
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def crear(self, datos: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
        """
        Crea un nuevo registro.
        
        Args:
            datos: Diccionario con los datos del registro
            
        Returns:
            tuple: (exito, mensaje, id_nuevo)
        """
        try:
            self.logger.info(f"Intentando crear registro con datos: {datos}")
            return self.modelo.crear(datos)
        except Exception as e:
            self.logger.error(f"Error en controlador al crear: {str(e)}")
            return False, f"Error interno: {str(e)}", None
    
    def leer(self, id_registro: int) -> Tuple[bool, str, Optional[Dict]]:
        """
        Lee un registro por ID.
        
        Args:
            id_registro: ID del registro a leer
            
        Returns:
            tuple: (exito, mensaje, datos)
        """
        try:
            self.logger.info(f"Intentando leer registro con ID: {id_registro}")
            return self.modelo.leer(id_registro)
        except Exception as e:
            self.logger.error(f"Error en controlador al leer: {str(e)}")
            return False, f"Error interno: {str(e)}", None
    
    def actualizar(self, id_registro: int, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Actualiza un registro existente.
        
        Args:
            id_registro: ID del registro a actualizar
            datos: Diccionario con los nuevos datos
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            self.logger.info(f"Intentando actualizar registro {id_registro} con datos: {datos}")
            return self.modelo.actualizar(id_registro, datos)
        except Exception as e:
            self.logger.error(f"Error en controlador al actualizar: {str(e)}")
            return False, f"Error interno: {str(e)}"
    
    def eliminar(self, id_registro: int) -> Tuple[bool, str]:
        """
        Elimina un registro.
        
        Args:
            id_registro: ID del registro a eliminar
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            self.logger.info(f"Intentando eliminar registro con ID: {id_registro}")
            return self.modelo.eliminar(id_registro)
        except Exception as e:
            self.logger.error(f"Error en controlador al eliminar: {str(e)}")
            return False, f"Error interno: {str(e)}"
    
    def listar(self, filtros: Optional[Dict] = None, limite: Optional[int] = None, 
               offset: Optional[int] = None) -> Tuple[bool, str, List[Dict]]:
        """
        Lista registros con filtros opcionales.
        
        Args:
            filtros: Diccionario con filtros a aplicar
            limite: Número máximo de registros a retornar
            offset: Número de registros a omitir
            
        Returns:
            tuple: (exito, mensaje, lista_datos)
        """
        try:
            self.logger.info(f"Intentando listar registros con filtros: {filtros}")
            return self.modelo.listar(filtros, limite, offset)
        except Exception as e:
            self.logger.error(f"Error en controlador al listar: {str(e)}")
            return False, f"Error interno: {str(e)}", []
    
    def validar_datos_entrada(self, datos: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Valida los datos de entrada antes de procesarlos.
        Puede ser sobrescrito por controladores específicos.
        
        Args:
            datos: Diccionario con los datos a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not isinstance(datos, dict):
            return False, "Los datos deben ser un diccionario"
        
        if not datos:
            return False, "No se proporcionaron datos"
        
        return True, ""
    
    def formatear_respuesta(self, exito: bool, mensaje: str, datos: Any = None) -> Dict[str, Any]:
        """
        Formatea la respuesta del controlador.
        
        Args:
            exito: Indica si la operación fue exitosa
            mensaje: Mensaje descriptivo
            datos: Datos adicionales (opcional)
            
        Returns:
            dict: Respuesta formateada
        """
        respuesta = {
            'exito': exito,
            'mensaje': mensaje,
            'timestamp': self._obtener_timestamp()
        }
        
        if datos is not None:
            respuesta['datos'] = datos
        
        return respuesta
    
    def _obtener_timestamp(self) -> str:
        """Obtiene el timestamp actual formateado."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def manejar_error(self, error: Exception, operacion: str) -> Tuple[bool, str]:
        """
        Maneja errores de manera consistente.
        
        Args:
            error: Excepción capturada
            operacion: Nombre de la operación que falló
            
        Returns:
            tuple: (exito, mensaje)
        """
        self.logger.error(f"Error en {operacion}: {str(error)}")
        
        # Mensajes de error amigables según el tipo de error
        if "duplicate key" in str(error).lower():
            return False, "Ya existe un registro con esos datos"
        elif "foreign key" in str(error).lower():
            return False, "No se puede realizar la operación debido a restricciones de integridad"
        elif "not null" in str(error).lower():
            return False, "Faltan datos requeridos"
        else:
            return False, f"Error en {operacion}: {str(error)}"
    
    def verificar_existencia(self, id_registro: int) -> bool:
        """
        Verifica si un registro existe.
        
        Args:
            id_registro: ID del registro a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            exito, _, _ = self.leer(id_registro)
            return exito
        except:
            return False
    
    def obtener_conteo(self, filtros: Optional[Dict] = None) -> Tuple[bool, str, int]:
        """
        Obtiene el número total de registros que coinciden con los filtros.
        
        Args:
            filtros: Filtros a aplicar
            
        Returns:
            tuple: (exito, mensaje, conteo)
        """
        try:
            # Obtener todos los registros con los filtros
            exito, mensaje, datos = self.listar(filtros)
            if exito:
                return True, "Conteo obtenido exitosamente", len(datos)
            else:
                return False, mensaje, 0
        except Exception as e:
            self.logger.error(f"Error al obtener conteo: {str(e)}")
            return False, f"Error al obtener conteo: {str(e)}", 0
