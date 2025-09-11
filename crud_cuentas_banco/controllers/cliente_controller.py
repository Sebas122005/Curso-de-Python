"""
Controlador para la gestión de clientes del sistema bancario.
Maneja la lógica de negocio relacionada con clientes.
"""

from controllers.base_controller import BaseController
from models.cliente import Cliente
from models.catalogo import TipoDocumento, CategoriaCliente
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ClienteController(BaseController):
    """Controlador para la gestión de clientes."""
    
    def __init__(self):
        super().__init__(Cliente())
        self.tipo_documento_model = TipoDocumento()
        self.categoria_model = CategoriaCliente()
    
    def crear_cliente(self, datos: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Crea un nuevo cliente con validaciones específicas.
        
        Args:
            datos: Diccionario con los datos del cliente
            
        Returns:
            tuple: (exito, mensaje, id_cliente)
        """
        try:
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_cliente_especifico(datos)
            if not exito:
                return False, mensaje, None
            
            # Verificar que el documento no exista
            if self._documento_existe(datos['numero_documento']):
                return False, "Ya existe un cliente con ese número de documento", None
            
            # Verificar que el email no exista
            if self._email_existe(datos['email']):
                return False, "Ya existe un cliente con ese email", None
            
            # Crear el cliente
            return self.crear(datos)
            
        except Exception as e:
            logger.error(f"Error al crear cliente: {str(e)}")
            return False, f"Error al crear cliente: {str(e)}", None
    
    def actualizar_cliente(self, id_cliente: int, datos: Dict) -> Tuple[bool, str]:
        """
        Actualiza un cliente existente con validaciones específicas.
        
        Args:
            id_cliente: ID del cliente a actualizar
            datos: Diccionario con los nuevos datos
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Verificar que el cliente existe
            if not self.verificar_existencia(id_cliente):
                return False, "El cliente no existe"
            
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_cliente_especifico(datos)
            if not exito:
                return False, mensaje
            
            # Verificar que el documento no exista en otro cliente
            if self._documento_existe_en_otro_cliente(datos['numero_documento'], id_cliente):
                return False, "Ya existe otro cliente con ese número de documento"
            
            # Verificar que el email no exista en otro cliente
            if self._email_existe_en_otro_cliente(datos['email'], id_cliente):
                return False, "Ya existe otro cliente con ese email"
            
            # Actualizar el cliente
            return self.actualizar(id_cliente, datos)
            
        except Exception as e:
            logger.error(f"Error al actualizar cliente: {str(e)}")
            return False, f"Error al actualizar cliente: {str(e)}"
    
    def buscar_cliente_por_documento(self, numero_documento: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Busca un cliente por número de documento.
        
        Args:
            numero_documento: Número de documento a buscar
            
        Returns:
            tuple: (exito, mensaje, datos_cliente)
        """
        try:
            return self.modelo.buscar_por_documento(numero_documento)
        except Exception as e:
            logger.error(f"Error al buscar cliente por documento: {str(e)}")
            return False, f"Error al buscar cliente: {str(e)}", None
    
    def buscar_clientes_por_nombre(self, nombre: str) -> Tuple[bool, str, List[Dict]]:
        """
        Busca clientes por nombre (nombre, apellido paterno o materno).
        
        Args:
            nombre: Nombre a buscar
            
        Returns:
            tuple: (exito, mensaje, lista_clientes)
        """
        try:
            filtros = {'nombre': nombre}
            return self.listar(filtros)
        except Exception as e:
            logger.error(f"Error al buscar clientes por nombre: {str(e)}")
            return False, f"Error al buscar clientes: {str(e)}", []
    
    def obtener_tipos_documento(self) -> Tuple[bool, str, List[Dict]]:
        """
        Obtiene la lista de tipos de documento disponibles.
        
        Returns:
            tuple: (exito, mensaje, lista_tipos)
        """
        try:
            return self.tipo_documento_model.listar()
        except Exception as e:
            logger.error(f"Error al obtener tipos de documento: {str(e)}")
            return False, f"Error al obtener tipos de documento: {str(e)}", []
    
    def obtener_categorias_cliente(self) -> Tuple[bool, str, List[Dict]]:
        """
        Obtiene la lista de categorías de cliente disponibles.
        
        Returns:
            tuple: (exito, mensaje, lista_categorias)
        """
        try:
            return self.categoria_model.listar()
        except Exception as e:
            logger.error(f"Error al obtener categorías de cliente: {str(e)}")
            return False, f"Error al obtener categorías: {str(e)}", []
    
    def obtener_estadisticas_clientes(self) -> Tuple[bool, str, Dict]:
        """
        Obtiene estadísticas de los clientes.
        
        Returns:
            tuple: (exito, mensaje, estadisticas)
        """
        try:
            # Obtener total de clientes
            exito, mensaje, total_clientes = self.obtener_conteo()
            if not exito:
                return False, mensaje, {}
            
            # Obtener clientes por categoría
            categorias = {}
            exito_cat, _, lista_categorias = self.obtener_categorias_cliente()
            if exito_cat:
                for categoria in lista_categorias:
                    filtros = {'id_categoria': categoria['id_categoria']}
                    exito_filtro, _, conteo = self.obtener_conteo(filtros)
                    if exito_filtro:
                        categorias[categoria['nombre_categoria']] = conteo
            
            estadisticas = {
                'total_clientes': total_clientes,
                'clientes_por_categoria': categorias
            }
            
            return True, "Estadísticas obtenidas exitosamente", estadisticas
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            return False, f"Error al obtener estadísticas: {str(e)}", {}
    
    def _validar_cliente_especifico(self, datos: Dict) -> Tuple[bool, str]:
        """
        Validaciones específicas del controlador de cliente.
        
        Args:
            datos: Datos del cliente a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Verificar que el tipo de documento existe
        if datos.get('id_tipo_documento'):
            exito, _, tipo_doc = self.tipo_documento_model.leer(datos['id_tipo_documento'])
            if not exito:
                return False, "El tipo de documento seleccionado no existe"
        
        # Verificar que la categoría existe
        if datos.get('id_categoria'):
            exito, _, categoria = self.categoria_model.leer(datos['id_categoria'])
            if not exito:
                return False, "La categoría de cliente seleccionada no existe"
        
        return True, ""
    
    def _documento_existe(self, numero_documento: str) -> bool:
        """
        Verifica si ya existe un cliente con el número de documento.
        
        Args:
            numero_documento: Número de documento a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            exito, _, _ = self.buscar_cliente_por_documento(numero_documento)
            return exito
        except:
            return False
    
    def _email_existe(self, email: str) -> bool:
        """
        Verifica si ya existe un cliente con el email.
        
        Args:
            email: Email a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            filtros = {'email': email}
            exito, _, clientes = self.listar(filtros)
            return exito and len(clientes) > 0
        except:
            return False
    
    def _documento_existe_en_otro_cliente(self, numero_documento: str, id_cliente_actual: int) -> bool:
        """
        Verifica si el documento existe en otro cliente (para actualizaciones).
        
        Args:
            numero_documento: Número de documento a verificar
            id_cliente_actual: ID del cliente que se está actualizando
            
        Returns:
            bool: True si existe en otro cliente, False en caso contrario
        """
        try:
            exito, _, cliente = self.buscar_cliente_por_documento(numero_documento)
            if exito and cliente['id_cliente'] != id_cliente_actual:
                return True
            return False
        except:
            return False
    
    def _email_existe_en_otro_cliente(self, email: str, id_cliente_actual: int) -> bool:
        """
        Verifica si el email existe en otro cliente (para actualizaciones).
        
        Args:
            email: Email a verificar
            id_cliente_actual: ID del cliente que se está actualizando
            
        Returns:
            bool: True si existe en otro cliente, False en caso contrario
        """
        try:
            filtros = {'email': email}
            exito, _, clientes = self.listar(filtros)
            if exito:
                for cliente in clientes:
                    if cliente['id_cliente'] != id_cliente_actual:
                        return True
            return False
        except:
            return False
    
    def formatear_nombre_completo(self, datos_cliente: Dict) -> str:
        """
        Formatea el nombre completo del cliente.
        
        Args:
            datos_cliente: Datos del cliente
            
        Returns:
            str: Nombre completo formateado
        """
        return self.modelo.obtener_nombre_completo(datos_cliente)
