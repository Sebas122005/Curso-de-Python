"""
Modelo para la entidad Usuario del sistema bancario.
Maneja la autenticación y roles de los usuarios.
"""

from models.base_model import BaseModel
import hashlib
import secrets


class Usuario(BaseModel):
    """Modelo para usuarios del sistema"""
    
    def __init__(self):
        super().__init__()
        self.username = None
        self.password_hash = None
        self.id_cliente = None
    
    def validar_datos(self, datos):
        """Valida los datos del usuario."""
        errores = []
        
        # Validar campos requeridos
        if not datos.get('username'):
            errores.append("El nombre de usuario es requerido")
        elif len(datos['username']) > 50:
            errores.append("El nombre de usuario no puede exceder 50 caracteres")
        elif not self._validar_username(datos['username']):
            errores.append("El nombre de usuario solo puede contener letras, números y guiones bajos")
        
        if not datos.get('password'):
            errores.append("La contraseña es requerida")
        elif len(datos['password']) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres")
        
        if not datos.get('id_cliente'):
            errores.append("El cliente es requerido")
        
        if errores:
            return False, "; ".join(errores)
        
        return True, ""
    
    def _validar_username(self, username):
        """Valida el formato del nombre de usuario."""
        import re
        patron = r'^[a-zA-Z0-9_]+$'
        return re.match(patron, username) is not None
    
    def _hash_password(self, password):
        """Genera el hash de la contraseña."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def _generar_query_creacion(self):
        return "INSERT INTO usuarios (username, password_hash, id_cliente) VALUES (%(username)s, %(password_hash)s, %(id_cliente)s)"
    
    def _generar_query_lectura(self):
        return """SELECT u.*, c.nombre, c.apellido_paterno, c.apellido_materno, c.email
                  FROM usuarios u
                  LEFT JOIN clientes c ON u.id_cliente = c.id_cliente
                  WHERE u.id_usuario = %s"""
    
    def _generar_query_actualizacion(self):
        return "UPDATE usuarios SET username = %(username)s, password_hash = %(password_hash)s, id_cliente = %(id_cliente)s WHERE id_usuario = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM usuarios WHERE id_usuario = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = """SELECT u.*, c.nombre, c.apellido_paterno, c.apellido_materno, c.email
                   FROM usuarios u
                   LEFT JOIN clientes c ON u.id_cliente = c.id_cliente"""
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('username'):
                condiciones.append("u.username LIKE %s")
                params.append(f"%{filtros['username']}%")
            if filtros.get('id_cliente'):
                condiciones.append("u.id_cliente = %s")
                params.append(filtros['id_cliente'])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY u.username"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        password_hash = self._hash_password(datos['password'])
        return {
            'username': datos['username'].strip().lower(),
            'password_hash': password_hash,
            'id_cliente': datos['id_cliente']
        }
    
    def _preparar_datos_actualizacion(self, datos):
        result = {
            'username': datos['username'].strip().lower(),
            'id_cliente': datos['id_cliente']
        }
        
        # Solo actualizar contraseña si se proporciona una nueva
        if datos.get('password'):
            result['password_hash'] = self._hash_password(datos['password'])
        
        return result
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_usuario': fila[0],
            'username': fila[1],
            'password_hash': fila[2],
            'id_cliente': fila[3],
            'nombre_cliente': fila[4] if len(fila) > 4 else None,
            'apellido_paterno': fila[5] if len(fila) > 5 else None,
            'apellido_materno': fila[6] if len(fila) > 6 else None,
            'email_cliente': fila[7] if len(fila) > 7 else None
        }
    
    def autenticar(self, username, password):
        """
        Autentica un usuario con username y password.
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            tuple: (exito, mensaje, datos_usuario)
        """
        try:
            query = """SELECT u.*, c.nombre, c.apellido_paterno, c.apellido_materno, c.email
                       FROM usuarios u
                       LEFT JOIN clientes c ON u.id_cliente = c.id_cliente
                       WHERE u.username = %s"""
            
            resultado = self.db.fetch_all(query, (username.lower(),))
            
            if not resultado:
                return False, "Usuario no encontrado", None
            
            usuario_data = self._formatear_datos_lectura(resultado[0])
            
            # Verificar contraseña
            if self._verificar_password(password, usuario_data['password_hash']):
                return True, "Autenticación exitosa", usuario_data
            else:
                return False, "Contraseña incorrecta", None
                
        except Exception as e:
            return False, f"Error en autenticación: {str(e)}", None
    
    def _verificar_password(self, password, password_hash):
        """Verifica si la contraseña es correcta."""
        try:
            salt, hash_almacenado = password_hash.split(':')
            hash_calculado = hashlib.sha256((password + salt).encode()).hexdigest()
            return hash_calculado == hash_almacenado
        except:
            return False
    
    def buscar_por_username(self, username):
        """
        Busca un usuario por nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar
            
        Returns:
            tuple: (exito, mensaje, datos)
        """
        try:
            query = """SELECT u.*, c.nombre, c.apellido_paterno, c.apellido_materno, c.email
                       FROM usuarios u
                       LEFT JOIN clientes c ON u.id_cliente = c.id_cliente
                       WHERE u.username = %s"""
            
            resultado = self.db.fetch_all(query, (username.lower(),))
            
            if resultado:
                datos = self._formatear_datos_lectura(resultado[0])
                return True, "Usuario encontrado", datos
            else:
                return False, "Usuario no encontrado", None
                
        except Exception as e:
            return False, f"Error al buscar usuario: {str(e)}", None
    
    def obtener_nombre_cliente_completo(self, datos_usuario):
        """Obtiene el nombre completo del cliente del usuario."""
        if (datos_usuario.get('apellido_paterno') and 
            datos_usuario.get('apellido_materno') and 
            datos_usuario.get('nombre_cliente')):
            return f"{datos_usuario['apellido_paterno']} {datos_usuario['apellido_materno']}, {datos_usuario['nombre_cliente']}"
        return "Cliente no disponible"