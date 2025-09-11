"""
Modelo para la entidad Cuenta del sistema bancario.
Maneja las cuentas bancarias de los clientes.
"""

from models.base_model import BaseModel
import re
from datetime import datetime


class Cuenta(BaseModel):
    """Modelo para cuentas bancarias"""
    
    def __init__(self):
        super().__init__()
        self.numero_cuenta = None
        self.cci = None
        self.id_cliente = None
        self.id_producto = None
        self.saldo = None
        self.fecha_apertura = None
        self.estado = None
    
    def validar_datos(self, datos):
        """Valida los datos de la cuenta."""
        errores = []
        
        # Validar campos requeridos
        if not datos.get('numero_cuenta'):
            errores.append("El número de cuenta es requerido")
        elif not self._validar_numero_cuenta(datos['numero_cuenta']):
            errores.append("El formato del número de cuenta no es válido")
        elif len(datos['numero_cuenta']) > 50:
            errores.append("El número de cuenta no puede exceder 50 caracteres")
        
        if not datos.get('cci'):
            errores.append("El CCI es requerido")
        elif not self._validar_cci(datos['cci']):
            errores.append("El formato del CCI no es válido")
        elif len(datos['cci']) > 25:
            errores.append("El CCI no puede exceder 25 caracteres")
        
        if not datos.get('id_cliente'):
            errores.append("El cliente es requerido")
        
        if not datos.get('id_producto'):
            errores.append("El producto de cuenta es requerido")
        
        if not datos.get('saldo'):
            errores.append("El saldo inicial es requerido")
        elif not self._validar_saldo(datos['saldo']):
            errores.append("El saldo debe ser un número positivo")
        
        if not datos.get('fecha_apertura'):
            errores.append("La fecha de apertura es requerida")
        elif not self._validar_fecha_apertura(datos['fecha_apertura']):
            errores.append("La fecha de apertura no es válida")
        
        if not datos.get('estado'):
            errores.append("El estado es requerido")
        elif datos['estado'] not in ['Activa', 'Inactiva', 'Suspendida', 'Cerrada']:
            errores.append("El estado debe ser: Activa, Inactiva, Suspendida o Cerrada")
        
        if errores:
            return False, "; ".join(errores)
        
        return True, ""
    
    def _validar_numero_cuenta(self, numero):
        """Valida el formato del número de cuenta."""
        # Formato: XXX-XXX-XXXXXX-XX (ej: 003-100-001001-44)
        patron = r'^\d{3}-\d{3}-\d{6}-\d{2}$'
        return re.match(patron, numero) is not None
    
    def _validar_cci(self, cci):
        """Valida el formato del CCI."""
        # Formato: XXX-XXX-XXXXXX-XX (ej: 003-100-001001-44)
        patron = r'^\d{3}-\d{3}-\d{6}-\d{2}$'
        return re.match(patron, cci) is not None
    
    def _validar_saldo(self, saldo):
        """Valida que el saldo sea un número positivo."""
        try:
            saldo_float = float(saldo)
            return saldo_float >= 0
        except (ValueError, TypeError):
            return False
    
    def _validar_fecha_apertura(self, fecha_str):
        """Valida la fecha de apertura."""
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hoy = datetime.now().date()
            # La fecha no puede ser futura
            if fecha > hoy:
                return False
            return True
        except ValueError:
            return False
    
    def _generar_query_creacion(self):
        return """INSERT INTO cuentas 
                  (numero_cuenta, cci, id_cliente, id_producto, saldo, fecha_apertura, estado) 
                  VALUES (%(numero_cuenta)s, %(cci)s, %(id_cliente)s, %(id_producto)s, 
                          %(saldo)s, %(fecha_apertura)s, %(estado)s)"""
    
    def _generar_query_lectura(self):
        return """SELECT c.*, cl.nombre, cl.apellido_paterno, cl.apellido_materno, 
                         p.nombre_producto, p.tipo_producto
                  FROM cuentas c
                  LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                  LEFT JOIN productos_cuenta p ON c.id_producto = p.id_producto
                  WHERE c.id_cuenta = %s"""
    
    def _generar_query_actualizacion(self):
        return """UPDATE cuentas SET 
                  numero_cuenta = %(numero_cuenta)s, cci = %(cci)s, 
                  id_cliente = %(id_cliente)s, id_producto = %(id_producto)s,
                  saldo = %(saldo)s, fecha_apertura = %(fecha_apertura)s, 
                  estado = %(estado)s
                  WHERE id_cuenta = %(id)s"""
    
    def _generar_query_eliminacion(self):
        return "DELETE FROM cuentas WHERE id_cuenta = %s"
    
    def _generar_query_listado(self, filtros=None, limite=None, offset=None):
        query = """SELECT c.*, cl.nombre, cl.apellido_paterno, cl.apellido_materno, 
                          p.nombre_producto, p.tipo_producto
                   FROM cuentas c
                   LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                   LEFT JOIN productos_cuenta p ON c.id_producto = p.id_producto"""
        params = []
        
        condiciones = []
        if filtros:
            if filtros.get('numero_cuenta'):
                condiciones.append("c.numero_cuenta LIKE %s")
                params.append(f"%{filtros['numero_cuenta']}%")
            if filtros.get('id_cliente'):
                condiciones.append("c.id_cliente = %s")
                params.append(filtros['id_cliente'])
            if filtros.get('estado'):
                condiciones.append("c.estado = %s")
                params.append(filtros['estado'])
            if filtros.get('id_producto'):
                condiciones.append("c.id_producto = %s")
                params.append(filtros['id_producto'])
            if filtros.get('saldo_minimo'):
                condiciones.append("c.saldo >= %s")
                params.append(filtros['saldo_minimo'])
            if filtros.get('saldo_maximo'):
                condiciones.append("c.saldo <= %s")
                params.append(filtros['saldo_maximo'])
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY c.fecha_apertura DESC"
        
        if limite:
            query += " LIMIT %s"
            params.append(limite)
        
        if offset:
            query += " OFFSET %s"
            params.append(offset)
        
        return query, params
    
    def _preparar_datos_creacion(self, datos):
        return {
            'numero_cuenta': datos['numero_cuenta'].strip(),
            'cci': datos['cci'].strip(),
            'id_cliente': datos['id_cliente'],
            'id_producto': datos['id_producto'],
            'saldo': float(datos['saldo']),
            'fecha_apertura': datos['fecha_apertura'],
            'estado': datos['estado']
        }
    
    def _preparar_datos_actualizacion(self, datos):
        return {
            'numero_cuenta': datos['numero_cuenta'].strip(),
            'cci': datos['cci'].strip(),
            'id_cliente': datos['id_cliente'],
            'id_producto': datos['id_producto'],
            'saldo': float(datos['saldo']),
            'fecha_apertura': datos['fecha_apertura'],
            'estado': datos['estado']
        }
    
    def _formatear_datos_lectura(self, fila):
        return {
            'id_cuenta': fila[0],
            'numero_cuenta': fila[1],
            'cci': fila[2],
            'id_cliente': fila[3],
            'id_producto': fila[4],
            'saldo': float(fila[5]) if fila[5] else 0.0,
            'fecha_apertura': fila[6],
            'estado': fila[7],
            'nombre_cliente': fila[8] if len(fila) > 8 else None,
            'apellido_paterno': fila[9] if len(fila) > 9 else None,
            'apellido_materno': fila[10] if len(fila) > 10 else None,
            'producto': fila[11] if len(fila) > 11 else None,
            'tipo_producto': fila[12] if len(fila) > 12 else None
        }
    
    def buscar_por_numero(self, numero_cuenta):
        """
        Busca una cuenta por número de cuenta.
        
        Args:
            numero_cuenta (str): Número de cuenta a buscar
            
        Returns:
            tuple: (exito, mensaje, datos)
        """
        try:
            query = """SELECT c.*, cl.nombre, cl.apellido_paterno, cl.apellido_materno, 
                              p.nombre_producto, p.tipo_producto
                       FROM cuentas c
                       LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                       LEFT JOIN productos_cuenta p ON c.id_producto = p.id_producto
                       WHERE c.numero_cuenta = %s"""
            
            resultado = self.db.fetch_all(query, (numero_cuenta,))
            
            if resultado:
                datos = self._formatear_datos_lectura(resultado[0])
                return True, "Cuenta encontrada", datos
            else:
                return False, "Cuenta no encontrada", None
                
        except Exception as e:
            return False, f"Error al buscar cuenta: {str(e)}", None
    
    def buscar_por_cliente(self, id_cliente):
        """
        Busca todas las cuentas de un cliente.
        
        Args:
            id_cliente (int): ID del cliente
            
        Returns:
            tuple: (exito, mensaje, lista_cuentas)
        """
        try:
            filtros = {'id_cliente': id_cliente}
            return self.listar(filtros)
        except Exception as e:
            return False, f"Error al buscar cuentas del cliente: {str(e)}", []
    
    def actualizar_saldo(self, id_cuenta, nuevo_saldo):
        """
        Actualiza el saldo de una cuenta.
        
        Args:
            id_cuenta (int): ID de la cuenta
            nuevo_saldo (float): Nuevo saldo
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            if nuevo_saldo < 0:
                return False, "El saldo no puede ser negativo"
            
            query = "UPDATE cuentas SET saldo = %s WHERE id_cuenta = %s"
            filas_afectadas = self.db.execute_query(query, (nuevo_saldo, id_cuenta))
            
            if filas_afectadas:
                # Registrar en historial de saldos
                self._registrar_cambio_saldo(id_cuenta, nuevo_saldo)
                return True, "Saldo actualizado exitosamente"
            else:
                return False, "No se pudo actualizar el saldo"
                
        except Exception as e:
            return False, f"Error al actualizar saldo: {str(e)}"
    
    def _registrar_cambio_saldo(self, id_cuenta, nuevo_saldo):
        """Registra el cambio de saldo en el historial."""
        try:
            # Obtener saldo anterior
            exito, _, datos = self.leer(id_cuenta)
            if exito:
                saldo_anterior = datos['saldo']
                
                # Insertar en historial
                query = """INSERT INTO historial_saldos 
                          (id_cuenta, saldo_anterior, saldo_nuevo) 
                          VALUES (%s, %s, %s)"""
                self.db.execute_query(query, (id_cuenta, saldo_anterior, nuevo_saldo))
        except Exception as e:
            # No fallar si no se puede registrar el historial
            pass
    
    def obtener_nombre_cliente_completo(self, datos_cuenta):
        """Obtiene el nombre completo del cliente de la cuenta."""
        if datos_cuenta.get('apellido_paterno') and datos_cuenta.get('apellido_materno') and datos_cuenta.get('nombre_cliente'):
            return f"{datos_cuenta['apellido_paterno']} {datos_cuenta['apellido_materno']}, {datos_cuenta['nombre_cliente']}"
        return "Cliente no disponible"
