"""
Modelos para las entidades de catálogo del sistema bancario.
Incluye tipos de documento, ubicaciones, categorías, etc.
"""

from models.base_model import BaseModel
import re


class TipoDocumento(BaseModel):
    """Modelo para tipos de documento legal (DNI, Pasaporte, etc.)"""
    
    def __init__(self):
        super().__init__()
        self.nombre_tipo = None
    
    def validar_datos(self, datos):
        """Valida los datos del tipo de documento."""
        if not datos.get('nombre_tipo'):
            return False, "El nombre del tipo de documento es requerido"
        
        if len(datos['nombre_tipo']) > 50:
            return False, "El nombre del tipo de documento no puede exceder 50 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO tipo_documento_legal (nombre_tipo) VALUES (%(nombre_tipo)s)"
    
    def _generar_query_lectura(self):
        return "SELECT * FROM tipo_documento_legal WHERE id_tipo_documento = %s"
    
    def _generar_query_actualizacion(self):
        return "UPDATE tipo_documento_legal SET nombre_tipo = %(nombre_tipo)s WHERE id_tipo_documento = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM tipo_documento_legal WHERE id_tipo_documento = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = "SELECT * FROM tipo_documento_legal"
        params = []
        
        if filtros and filtros.get('nombre_tipo'):
            query += " WHERE nombre_tipo LIKE %s"
            params.append(f"%{filtros['nombre_tipo']}%")
        
        query += " ORDER BY nombre_tipo"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'nombre_tipo': datos['nombre_tipo'].strip()
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre_tipo': datos['nombre_tipo'].strip()
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_tipo_documento': fila[0],
            'nombre_tipo': fila[1]
        }


class Departamento(BaseModel):
    """Modelo para departamentos del Perú"""
    
    def __init__(self):
        super().__init__()
        self.nombre = None
    
    def validar_datos(self, datos):
        """Valida los datos del departamento."""
        if not datos.get('nombre'):
            return False, "El nombre del departamento es requerido"
        
        if len(datos['nombre']) > 50:
            return False, "El nombre del departamento no puede exceder 50 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO departamentos (nombre) VALUES (%(nombre)s)"
    
    def _generar_query_lectura(self):
        return "SELECT * FROM departamentos WHERE id_departamento = %s"
    
    def _generar_query_actualizacion(self):
        return "UPDATE departamentos SET nombre = %(nombre)s WHERE id_departamento = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM departamentos WHERE id_departamento = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = "SELECT * FROM departamentos"
        params = []
        
        if filtros and filtros.get('nombre'):
            query += " WHERE nombre LIKE %s"
            params.append(f"%{filtros['nombre']}%")
        
        query += " ORDER BY nombre"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'nombre': datos['nombre'].strip()
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre': datos['nombre'].strip()
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_departamento': fila[0],
            'nombre': fila[1]
        }


class Provincia(BaseModel):
    """Modelo para provincias del Perú"""
    
    def __init__(self):
        super().__init__()
        self.nombre = None
        self.id_departamento = None
    
    def validar_datos(self, datos):
        """Valida los datos de la provincia."""
        if not datos.get('nombre'):
            return False, "El nombre de la provincia es requerido"
        
        if not datos.get('id_departamento'):
            return False, "El departamento es requerido"
        
        if len(datos['nombre']) > 50:
            return False, "El nombre de la provincia no puede exceder 50 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO provincias (nombre, id_departamento) VALUES (%(nombre)s, %(id_departamento)s)"
    
    def _generar_query_lectura(self):
        return "SELECT p.*, d.nombre as departamento FROM provincias p LEFT JOIN departamentos d ON p.id_departamento = d.id_departamento WHERE p.id_provincia = %s"
    
    def _generar_query_actualizacion(self):
        return "UPDATE provincias SET nombre = %(nombre)s, id_departamento = %(id_departamento)s WHERE id_provincia = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM provincias WHERE id_provincia = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = """SELECT p.*, d.nombre as departamento 
                   FROM provincias p 
                   LEFT JOIN departamentos d ON p.id_departamento = d.id_departamento"""
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('nombre'):
                condiciones.append("p.nombre LIKE %s")
                params.append(f"%{filtros['nombre']}%")
            if filtros.get('id_departamento'):
                condiciones.append("p.id_departamento = %s")
                params.append(filtros['id_departamento'])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY p.nombre"
        
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
            'id_departamento': datos['id_departamento']
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre': datos['nombre'].strip(),
            'id_departamento': datos['id_departamento']
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_provincia': fila[0],
            'nombre': fila[1],
            'id_departamento': fila[2],
            'departamento': fila[3] if len(fila) > 3 else None
        }


class Distrito(BaseModel):
    """Modelo para distritos del Perú"""
    
    def __init__(self):
        super().__init__()
        self.nombre = None
        self.id_provincia = None
    
    def validar_datos(self, datos):
        """Valida los datos del distrito."""
        if not datos.get('nombre'):
            return False, "El nombre del distrito es requerido"
        
        if not datos.get('id_provincia'):
            return False, "La provincia es requerida"
        
        if len(datos['nombre']) > 50:
            return False, "El nombre del distrito no puede exceder 50 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO distritos (nombre, id_provincia) VALUES (%(nombre)s, %(id_provincia)s)"
    
    def _generar_query_lectura(self):
        return """SELECT d.*, p.nombre as provincia, dep.nombre as departamento 
                  FROM distritos d 
                  LEFT JOIN provincias p ON d.id_provincia = p.id_provincia
                  LEFT JOIN departamentos dep ON p.id_departamento = dep.id_departamento
                  WHERE d.id_distrito = %s"""
    
    def _generar_query_actualizacion(self):
        return "UPDATE distritos SET nombre = %(nombre)s, id_provincia = %(id_provincia)s WHERE id_distrito = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM distritos WHERE id_distrito = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = """SELECT d.*, p.nombre as provincia, dep.nombre as departamento 
                   FROM distritos d 
                   LEFT JOIN provincias p ON d.id_provincia = p.id_provincia
                   LEFT JOIN departamentos dep ON p.id_departamento = dep.id_departamento"""
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('nombre'):
                condiciones.append("d.nombre LIKE %s")
                params.append(f"%{filtros['nombre']}%")
            if filtros.get('id_provincia'):
                condiciones.append("d.id_provincia = %s")
                params.append(filtros['id_provincia'])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY d.nombre"
        
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
            'id_provincia': datos['id_provincia']
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre': datos['nombre'].strip(),
            'id_provincia': datos['id_provincia']
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_distrito': fila[0],
            'nombre': fila[1],
            'id_provincia': fila[2],
            'provincia': fila[3] if len(fila) > 3 else None,
            'departamento': fila[4] if len(fila) > 4 else None
        }


class CategoriaCliente(BaseModel):
    """Modelo para categorías de cliente (Estándar, Premium, Empresarial)"""
    
    def __init__(self):
        super().__init__()
        self.nombre_categoria = None
    
    def validar_datos(self, datos):
        """Valida los datos de la categoría de cliente."""
        if not datos.get('nombre_categoria'):
            return False, "El nombre de la categoría es requerido"
        
        if len(datos['nombre_categoria']) > 50:
            return False, "El nombre de la categoría no puede exceder 50 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO categoria_cliente (nombre_categoria) VALUES (%(nombre_categoria)s)"
    
    def _generar_query_lectura(self):
        return "SELECT * FROM categoria_cliente WHERE id_categoria = %s"
    
    def _generar_query_actualizacion(self):
        return "UPDATE categoria_cliente SET nombre_categoria = %(nombre_categoria)s WHERE id_categoria = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM categoria_cliente WHERE id_categoria = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = "SELECT * FROM categoria_cliente"
        params = []
        
        if filtros and filtros.get('nombre_categoria'):
            query += " WHERE nombre_categoria LIKE %s"
            params.append(f"%{filtros['nombre_categoria']}%")
        
        query += " ORDER BY nombre_categoria"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'nombre_categoria': datos['nombre_categoria'].strip()
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre_categoria': datos['nombre_categoria'].strip()
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_categoria': fila[0],
            'nombre_categoria': fila[1]
        }


class Banco(BaseModel):
    """Modelo para bancos del sistema"""
    
    def __init__(self):
        super().__init__()
        self.nombre_banco = None
        self.codigo_banco = None
    
    def validar_datos(self, datos):
        """Valida los datos del banco."""
        if not datos.get('nombre_banco'):
            return False, "El nombre del banco es requerido"
        
        if not datos.get('codigo_banco'):
            return False, "El código del banco es requerido"
        
        if len(datos['nombre_banco']) > 100:
            return False, "El nombre del banco no puede exceder 100 caracteres"
        
        if len(datos['codigo_banco']) > 10:
            return False, "El código del banco no puede exceder 10 caracteres"
        
        return True, ""
    
    def _generar_query_creacion(self):
        return "INSERT INTO bancos (nombre_banco, codigo_banco) VALUES (%(nombre_banco)s, %(codigo_banco)s)"
    
    def _generar_query_lectura(self):
        return "SELECT * FROM bancos WHERE id_banco = %s"
    
    def _generar_query_actualizacion(self):
        return "UPDATE bancos SET nombre_banco = %(nombre_banco)s, codigo_banco = %(codigo_banco)s WHERE id_banco = %(id)s"
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM bancos WHERE id_banco = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = "SELECT * FROM bancos"
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('nombre_banco'):
                condiciones.append("nombre_banco LIKE %s")
                params.append(f"%{filtros['nombre_banco']}%")
            if filtros.get('codigo_banco'):
                condiciones.append("codigo_banco LIKE %s")
                params.append(f"%{filtros['codigo_banco']}%")
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY nombre_banco"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'nombre_banco': datos['nombre_banco'].strip(),
            'codigo_banco': datos['codigo_banco'].strip()
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'nombre_banco': datos['nombre_banco'].strip(),
            'codigo_banco': datos['codigo_banco'].strip()
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_banco': fila[0],
            'nombre_banco': fila[1],
            'codigo_banco': fila[2]
        }
