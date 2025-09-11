"""
Controlador para la gestión de usuarios del sistema bancario.
Maneja la lógica de negocio relacionada con usuarios y autenticación.
"""

from controllers.base_controller import BaseController
from models.usuario import Usuario
from models.cliente import Cliente
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class UsuarioController(BaseController):
    """Controlador para la gestión de usuarios."""
    
    def __init__(self):
        super().__init__(Usuario())
        self.cliente_model = Cliente()
    
    def crear_usuario(self, datos: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Crea un nuevo usuario con validaciones específicas.
        
        Args:
            datos: Diccionario con los datos del usuario
            
        Returns:
            tuple: (exito, mensaje, id_usuario)
        """
        try:
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_usuario_especifico(datos)
            if not exito:
                return False, mensaje, None
            
            # Verificar que el username no exista
            if self._username_existe(datos['username']):
                return False, "Ya existe un usuario con ese nombre de usuario", None
            
            # Verificar que el cliente existe
            if not self._cliente_existe(datos['id_cliente']):
                return False, "El cliente seleccionado no existe", None
            
            # Verificar que el cliente no tenga ya un usuario
            if self._cliente_tiene_usuario(datos['id_cliente']):
                return False, "El cliente ya tiene un usuario asociado", None
            
            # Crear el usuario
            return self.crear(datos)
            
        except Exception as e:
            logger.error(f"Error al crear usuario: {str(e)}")
            return False, f"Error al crear usuario: {str(e)}", None
    
    def actualizar_usuario(self, id_usuario: int, datos: Dict) -> Tuple[bool, str]:
        """
        Actualiza un usuario existente con validaciones específicas.
        
        Args:
            id_usuario: ID del usuario a actualizar
            datos: Diccionario con los nuevos datos
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Verificar que el usuario existe
            if not self.verificar_existencia(id_usuario):
                return False, "El usuario no existe"
            
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_usuario_especifico(datos)
            if not exito:
                return False, mensaje
            
            # Verificar que el username no exista en otro usuario
            if self._username_existe_en_otro_usuario(datos['username'], id_usuario):
                return False, "Ya existe otro usuario con ese nombre de usuario"
            
            # Verificar que el cliente existe
            if not self._cliente_existe(datos['id_cliente']):
                return False, "El cliente seleccionado no existe"
            
            # Actualizar el usuario
            return self.actualizar(id_usuario, datos)
            
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {str(e)}")
            return False, f"Error al actualizar usuario: {str(e)}"
    
    def autenticar_usuario(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Autentica un usuario con username y password.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            tuple: (exito, mensaje, datos_usuario)
        """
        try:
            return self.modelo.autenticar(username, password)
        except Exception as e:
            logger.error(f"Error al autenticar usuario: {str(e)}")
            return False, f"Error en autenticación: {str(e)}", None
    
    def buscar_usuario_por_username(self, username: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Busca un usuario por nombre de usuario.
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            tuple: (exito, mensaje, datos_usuario)
        """
        try:
            return self.modelo.buscar_por_username(username)
        except Exception as e:
            logger.error(f"Error al buscar usuario por username: {str(e)}")
            return False, f"Error al buscar usuario: {str(e)}", None
    
    def buscar_usuarios_por_cliente(self, id_cliente: int) -> Tuple[bool, str, List[Dict]]:
        """
        Busca usuarios asociados a un cliente.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            tuple: (exito, mensaje, lista_usuarios)
        """
        try:
            filtros = {'id_cliente': id_cliente}
            return self.listar(filtros)
        except Exception as e:
            logger.error(f"Error al buscar usuarios del cliente: {str(e)}")
            return False, f"Error al buscar usuarios: {str(e)}", []
    
    def cambiar_password(self, id_usuario: int, password_actual: str, password_nuevo: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            id_usuario: ID del usuario
            password_actual: Contraseña actual
            password_nuevo: Nueva contraseña
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Obtener datos del usuario
            exito, mensaje, datos_usuario = self.leer(id_usuario)
            if not exito:
                return False, "Usuario no encontrado"
            
            # Verificar contraseña actual
            if not self.modelo._verificar_password(password_actual, datos_usuario['password_hash']):
                return False, "La contraseña actual es incorrecta"
            
            # Validar nueva contraseña
            if len(password_nuevo) < 6:
                return False, "La nueva contraseña debe tener al menos 6 caracteres"
            
            # Actualizar contraseña
            datos_actualizacion = {
                'username': datos_usuario['username'],
                'password': password_nuevo,
                'id_cliente': datos_usuario['id_cliente']
            }
            
            return self.actualizar(id_usuario, datos_actualizacion)
            
        except Exception as e:
            logger.error(f"Error al cambiar contraseña: {str(e)}")
            return False, f"Error al cambiar contraseña: {str(e)}"
    
    def obtener_usuarios_activos(self) -> Tuple[bool, str, List[Dict]]:
        """
        Obtiene todos los usuarios activos (con cliente asociado).
        
        Returns:
            tuple: (exito, mensaje, lista_usuarios)
        """
        try:
            # Obtener todos los usuarios que tienen cliente asociado
            exito, mensaje, usuarios = self.listar()
            if not exito:
                return False, mensaje, []
            
            # Filtrar solo los que tienen cliente
            usuarios_activos = [u for u in usuarios if u.get('id_cliente')]
            return True, "Usuarios activos obtenidos exitosamente", usuarios_activos
            
        except Exception as e:
            logger.error(f"Error al obtener usuarios activos: {str(e)}")
            return False, f"Error al obtener usuarios activos: {str(e)}", []
    
    def obtener_estadisticas_usuarios(self) -> Tuple[bool, str, Dict]:
        """
        Obtiene estadísticas de los usuarios.
        
        Returns:
            tuple: (exito, mensaje, estadisticas)
        """
        try:
            # Obtener total de usuarios
            exito, mensaje, total_usuarios = self.obtener_conteo()
            if not exito:
                return False, mensaje, {}
            
            # Obtener usuarios activos
            exito_activos, _, usuarios_activos = self.obtener_usuarios_activos()
            total_activos = len(usuarios_activos) if exito_activos else 0
            
            # Obtener usuarios sin cliente asociado
            usuarios_sin_cliente = total_usuarios - total_activos
            
            estadisticas = {
                'total_usuarios': total_usuarios,
                'usuarios_activos': total_activos,
                'usuarios_sin_cliente': usuarios_sin_cliente
            }
            
            return True, "Estadísticas obtenidas exitosamente", estadisticas
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            return False, f"Error al obtener estadísticas: {str(e)}", {}
    
    def _validar_usuario_especifico(self, datos: Dict) -> Tuple[bool, str]:
        """
        Validaciones específicas del controlador de usuario.
        
        Args:
            datos: Datos del usuario a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Verificar que el cliente existe
        if datos.get('id_cliente'):
            exito, _, cliente = self.cliente_model.leer(datos['id_cliente'])
            if not exito:
                return False, "El cliente seleccionado no existe"
        
        # Validar formato del username
        if datos.get('username'):
            username = datos['username'].strip()
            if len(username) < 3:
                return False, "El nombre de usuario debe tener al menos 3 caracteres"
            if not username.replace('_', '').isalnum():
                return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
        
        return True, ""
    
    def _username_existe(self, username: str) -> bool:
        """
        Verifica si ya existe un usuario con el username.
        
        Args:
            username: Username a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            exito, _, _ = self.buscar_usuario_por_username(username)
            return exito
        except:
            return False
    
    def _cliente_existe(self, id_cliente: int) -> bool:
        """
        Verifica si el cliente existe.
        
        Args:
            id_cliente: ID del cliente a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            exito, _, _ = self.cliente_model.leer(id_cliente)
            return exito
        except:
            return False
    
    def _cliente_tiene_usuario(self, id_cliente: int) -> bool:
        """
        Verifica si el cliente ya tiene un usuario asociado.
        
        Args:
            id_cliente: ID del cliente a verificar
            
        Returns:
            bool: True si tiene usuario, False en caso contrario
        """
        try:
            exito, _, usuarios = self.buscar_usuarios_por_cliente(id_cliente)
            return exito and len(usuarios) > 0
        except:
            return False
    
    def _username_existe_en_otro_usuario(self, username: str, id_usuario_actual: int) -> bool:
        """
        Verifica si el username existe en otro usuario (para actualizaciones).
        
        Args:
            username: Username a verificar
            id_usuario_actual: ID del usuario que se está actualizando
            
        Returns:
            bool: True si existe en otro usuario, False en caso contrario
        """
        try:
            exito, _, usuario = self.buscar_usuario_por_username(username)
            if exito and usuario['id_usuario'] != id_usuario_actual:
                return True
            return False
        except:
            return False
