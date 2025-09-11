"""
Modelo para la entidad Cliente del sistema bancario.
Maneja la información personal y de contacto de los clientes.
"""

from models.base_model import BaseModel
import re
from datetime import datetime


class Cliente(BaseModel):
    """Modelo para clientes del banco"""
    
    def __init__(self):
        super().__init__()
        self.nombre = None
        self.apellido_paterno = None
        self.apellido_materno = None
        self.id_tipo_documento = None
        self.numero_documento = None
        self.email = None
        self.telefono = None
        self.fecha_nacimiento = None
        self.id_categoria = None
        self.id_agencia_apertura = None
    
    def validar_datos(self, datos):
        """Valida los datos del cliente."""
        errores = []
        
        # Validar campos requeridos
        if not datos.get('nombre'):
            errores.append("El nombre es requerido")
        elif len(datos['nombre']) > 100:
            errores.append("El nombre no puede exceder 100 caracteres")
        
        if not datos.get('apellido_paterno'):
            errores.append("El apellido paterno es requerido")
        elif len(datos['apellido_paterno']) > 100:
            errores.append("El apellido paterno no puede exceder 100 caracteres")
        
        if not datos.get('apellido_materno'):
            errores.append("El apellido materno es requerido")
        elif len(datos['apellido_materno']) > 100:
            errores.append("El apellido materno no puede exceder 100 caracteres")
        
        if not datos.get('id_tipo_documento'):
            errores.append("El tipo de documento es requerido")
        
        if not datos.get('numero_documento'):
            errores.append("El número de documento es requerido")
        elif len(datos['numero_documento']) > 20:
            errores.append("El número de documento no puede exceder 20 caracteres")
        
        if not datos.get('email'):
            errores.append("El email es requerido")
        elif not self._validar_email(datos['email']):
            errores.append("El formato del email no es válido")
        elif len(datos['email']) > 255:
            errores.append("El email no puede exceder 255 caracteres")
        
        if not datos.get('id_categoria'):
            errores.append("La categoría de cliente es requerida")
        
        if not datos.get('id_agencia_apertura'):
            errores.append("La agencia de apertura es requerida")
        
        # Validar teléfono si se proporciona
        if datos.get('telefono') and len(datos['telefono']) > 20:
            errores.append("El teléfono no puede exceder 20 caracteres")
        
        # Validar fecha de nacimiento si se proporciona
        if datos.get('fecha_nacimiento'):
            if not self._validar_fecha_nacimiento(datos['fecha_nacimiento']):
                errores.append("La fecha de nacimiento no es válida")
        
        if errores:
            return False, "; ".join(errores)
        
        return True, ""
    
    def _validar_email(self, email):
        """Valida el formato del email."""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def _validar_fecha_nacimiento(self, fecha_str):
        """Valida la fecha de nacimiento."""
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hoy = datetime.now().date()
            if fecha >= hoy:
                return False
            # Verificar que no sea muy antigua (más de 120 años)
            if fecha.year < (hoy.year - 120):
                return False
            return True
        except ValueError:
            return False
    
    def _generar_query_creacion(self):
        return """INSERT INTO clientes 
                  (nombre, apellido_paterno, apellido_materno, id_tipo_documento, 
                   numero_documento, email, telefono, fecha_nacimiento, 
                   id_categoria, id_agencia_apertura) 
                  VALUES (%(nombre)s, %(apellido_paterno)s, %(apellido_materno)s, 
                          %(id_tipo_documento)s, %(numero_documento)s, %(email)s, 
                          %(telefono)s, %(fecha_nacimiento)s, %(id_categoria)s, 
                          %(id_agencia_apertura)s)"""
    
    def _generar_query_lectura(self):
        return """SELECT c.*, td.nombre_tipo, cat.nombre_categoria, a.nombre_agencia
                  FROM clientes c
                  LEFT JOIN tipo_documento_legal td ON c.id_tipo_documento = td.id_tipo_documento
                  LEFT JOIN categoria_cliente cat ON c.id_categoria = cat.id_categoria
                  LEFT JOIN agencias a ON c.id_agencia_apertura = a.id_agencia
                  WHERE c.id_cliente = %s"""
    
    def _generar_query_actualizacion(self):
        return """UPDATE clientes SET 
                  nombre = %(nombre)s, apellido_paterno = %(apellido_paterno)s, 
                  apellido_materno = %(apellido_materno)s, id_tipo_documento = %(id_tipo_documento)s,
                  numero_documento = %(numero_documento)s, email = %(email)s, 
                  telefono = %(telefono)s, fecha_nacimiento = %(fecha_nacimiento)s,
                  id_categoria = %(id_categoria)s, id_agencia_apertura = %(id_agencia_apertura)s
                  WHERE id_cliente = %(id)s"""
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM clientes WHERE id_cliente = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = """SELECT c.*, td.nombre_tipo, cat.nombre_categoria, a.nombre_agencia
                   FROM clientes c
                   LEFT JOIN tipo_documento_legal td ON c.id_tipo_documento = td.id_tipo_documento
                   LEFT JOIN categoria_cliente cat ON c.id_categoria = cat.id_categoria
                   LEFT JOIN agencias a ON c.id_agencia_apertura = a.id_agencia"""
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('nombre'):
                condiciones.append("(c.nombre LIKE %s OR c.apellido_paterno LIKE %s OR c.apellido_materno LIKE %s)")
                params.extend([f"%{filtros['nombre']}%", f"%{filtros['nombre']}%", f"%{filtros['nombre']}%"])
            if filtros.get('numero_documento'):
                condiciones.append("c.numero_documento LIKE %s")
                params.append(f"%{filtros['numero_documento']}%")
            if filtros.get('email'):
                condiciones.append("c.email LIKE %s")
                params.append(f"%{filtros['email']}%")
            if filtros.get('id_categoria'):
                condiciones.append("c.id_categoria = %s")
                params.append(filtros['id_categoria'])
            if filtros.get('id_agencia_apertura'):
                condiciones.append("c.id_agencia_apertura = %s")
                params.append(filtros['id_agencia_apertura'])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY c.apellido_paterno, c.apellido_materno, c.nombre"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'nombre': datos['nombre'].strip(),
            'apellido_paterno': datos['apellido_paterno'].strip(),
            'apellido_materno': datos['apellido_materno'].strip(),
            'id_tipo_documento': datos['id_tipo_documento'],
            'numero_documento': datos['numero_documento'].strip(),
            'email': datos['email'].strip().lower(),
            'telefono': datos.get('telefono', '').strip() or None,
            'fecha_nacimiento': datos.get('fecha_nacimiento') or None,
            'id_categoria': datos['id_categoria'],
            'id_agencia_apertura': datos['id_agencia_apertura']
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre': datos['nombre'].strip(),
            'apellido_paterno': datos['apellido_paterno'].strip(),
            'apellido_materno': datos['apellido_materno'].strip(),
            'id_tipo_documento': datos['id_tipo_documento'],
            'numero_documento': datos['numero_documento'].strip(),
            'email': datos['email'].strip().lower(),
            'telefono': datos.get('telefono', '').strip() or None,
            'fecha_nacimiento': datos.get('fecha_nacimiento') or None,
            'id_categoria': datos['id_categoria'],
            'id_agencia_apertura': datos['id_agencia_apertura']
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_cliente': fila[0],
            'nombre': fila[1],
            'apellido_paterno': fila[2],
            'apellido_materno': fila[3],
            'id_tipo_documento': fila[4],
            'numero_documento': fila[5],
            'email': fila[6],
            'telefono': fila[7],
            'fecha_nacimiento': fila[8],
            'id_categoria': fila[9],
            'id_agencia_apertura': fila[10],
            'tipo_documento': fila[11] if len(fila) > 11 else None,
            'categoria': fila[12] if len(fila) > 12 else None,
            'agencia': fila[13] if len(fila) > 13 else None
        }
    
    def buscar_por_documento(self, numero_documento):
        """
        Busca un cliente por número de documento.
        
        Args:
            numero_documento (str): Número de documento a buscar
            
        Returns:
            tuple: (exito, mensaje, datos)
        """
        try:
            query = """SELECT c.*, td.nombre_tipo, cat.nombre_categoria, a.nombre_agencia
                       FROM clientes c
                       LEFT JOIN tipo_documento_legal td ON c.id_tipo_documento = td.id_tipo_documento
                       LEFT JOIN categoria_cliente cat ON c.id_categoria = cat.id_categoria
                       LEFT JOIN agencias a ON c.id_agencia_apertura = a.id_agencia
                       WHERE c.numero_documento = %s"""
            
            resultado = self.db.fetch_all(query, (numero_documento,))
            
            if resultado:
                datos = self._formatear_datos_lectura(resultado[0])
                return True, "Cliente encontrado", datos
            else:
                return False, "Cliente no encontrado", None
                
        except Exception as e:
            return False, f"Error al buscar cliente: {str(e)}", None
    
    def obtener_nombre_completo(self, datos_cliente):
        """Obtiene el nombre completo del cliente."""
        return f"{datos_cliente['apellido_paterno']} {datos_cliente['apellido_materno']}, {datos_cliente['nombre']}"
