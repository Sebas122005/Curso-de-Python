"""
Controlador para la gestión de cuentas bancarias.
Maneja la lógica de negocio relacionada con cuentas.
"""

from controllers.base_controller import BaseController
from models.cuenta import Cuenta
from models.cliente import Cliente
from models.catalogo import Banco
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class CuentaController(BaseController):
    """Controlador para la gestión de cuentas bancarias."""
    
    def __init__(self):
        super().__init__(Cuenta())
        self.cliente_model = Cliente()
        self.banco_model = Banco()
    
    def crear_cuenta(self, datos: Dict) -> Tuple[bool, str, Optional[int]]:
        """
        Crea una nueva cuenta con validaciones específicas.
        
        Args:
            datos: Diccionario con los datos de la cuenta
            
        Returns:
            tuple: (exito, mensaje, id_cuenta)
        """
        try:
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_cuenta_especifica(datos)
            if not exito:
                return False, mensaje, None
            
            # Verificar que el número de cuenta no exista
            if self._numero_cuenta_existe(datos['numero_cuenta']):
                return False, "Ya existe una cuenta con ese número", None
            
            # Verificar que el CCI no exista
            if self._cci_existe(datos['cci']):
                return False, "Ya existe una cuenta con ese CCI", None
            
            # Verificar que el cliente existe
            if not self._cliente_existe(datos['id_cliente']):
                return False, "El cliente seleccionado no existe", None
            
            # Crear la cuenta
            return self.crear(datos)
            
        except Exception as e:
            logger.error(f"Error al crear cuenta: {str(e)}")
            return False, f"Error al crear cuenta: {str(e)}", None
    
    def actualizar_cuenta(self, id_cuenta: int, datos: Dict) -> Tuple[bool, str]:
        """
        Actualiza una cuenta existente con validaciones específicas.
        
        Args:
            id_cuenta: ID de la cuenta a actualizar
            datos: Diccionario con los nuevos datos
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            # Verificar que la cuenta existe
            if not self.verificar_existencia(id_cuenta):
                return False, "La cuenta no existe"
            
            # Validaciones específicas del controlador
            exito, mensaje = self._validar_cuenta_especifica(datos)
            if not exito:
                return False, mensaje
            
            # Verificar que el número de cuenta no exista en otra cuenta
            if self._numero_cuenta_existe_en_otra_cuenta(datos['numero_cuenta'], id_cuenta):
                return False, "Ya existe otra cuenta con ese número"
            
            # Verificar que el CCI no exista en otra cuenta
            if self._cci_existe_en_otra_cuenta(datos['cci'], id_cuenta):
                return False, "Ya existe otra cuenta con ese CCI"
            
            # Verificar que el cliente existe
            if not self._cliente_existe(datos['id_cliente']):
                return False, "El cliente seleccionado no existe"
            
            # Actualizar la cuenta
            return self.actualizar(id_cuenta, datos)
            
        except Exception as e:
            logger.error(f"Error al actualizar cuenta: {str(e)}")
            return False, f"Error al actualizar cuenta: {str(e)}", None
    
    def buscar_cuenta_por_numero(self, numero_cuenta: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Busca una cuenta por número de cuenta.
        
        Args:
            numero_cuenta: Número de cuenta a buscar
            
        Returns:
            tuple: (exito, mensaje, datos_cuenta)
        """
        try:
            return self.modelo.buscar_por_numero(numero_cuenta)
        except Exception as e:
            logger.error(f"Error al buscar cuenta por número: {str(e)}")
            return False, f"Error al buscar cuenta: {str(e)}", None
    
    def buscar_cuentas_por_cliente(self, id_cliente: int) -> Tuple[bool, str, List[Dict]]:
        """
        Busca todas las cuentas de un cliente.
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            tuple: (exito, mensaje, lista_cuentas)
        """
        try:
            return self.modelo.buscar_por_cliente(id_cliente)
        except Exception as e:
            logger.error(f"Error al buscar cuentas del cliente: {str(e)}")
            return False, f"Error al buscar cuentas: {str(e)}", []
    
    def actualizar_saldo(self, id_cuenta: int, nuevo_saldo: float) -> Tuple[bool, str]:
        """
        Actualiza el saldo de una cuenta.
        
        Args:
            id_cuenta: ID de la cuenta
            nuevo_saldo: Nuevo saldo
            
        Returns:
            tuple: (exito, mensaje)
        """
        try:
            return self.modelo.actualizar_saldo(id_cuenta, nuevo_saldo)
        except Exception as e:
            logger.error(f"Error al actualizar saldo: {str(e)}")
            return False, f"Error al actualizar saldo: {str(e)}"
    
    def obtener_cuentas_activas(self) -> Tuple[bool, str, List[Dict]]:
        """
        Obtiene todas las cuentas activas.
        
        Returns:
            tuple: (exito, mensaje, lista_cuentas)
        """
        try:
            filtros = {'estado': 'Activa'}
            return self.listar(filtros)
        except Exception as e:
            logger.error(f"Error al obtener cuentas activas: {str(e)}")
            return False, f"Error al obtener cuentas activas: {str(e)}", []
    
    def obtener_cuentas_por_saldo(self, saldo_minimo: float = None, saldo_maximo: float = None) -> Tuple[bool, str, List[Dict]]:
        """
        Obtiene cuentas filtradas por rango de saldo.
        
        Args:
            saldo_minimo: Saldo mínimo (opcional)
            saldo_maximo: Saldo máximo (opcional)
            
        Returns:
            tuple: (exito, mensaje, lista_cuentas)
        """
        try:
            filtros = {}
            if saldo_minimo is not None:
                filtros['saldo_minimo'] = saldo_minimo
            if saldo_maximo is not None:
                filtros['saldo_maximo'] = saldo_maximo
            
            return self.listar(filtros)
        except Exception as e:
            logger.error(f"Error al obtener cuentas por saldo: {str(e)}")
            return False, f"Error al obtener cuentas: {str(e)}", []
    
    def obtener_estadisticas_cuentas(self) -> Tuple[bool, str, Dict]:
        """
        Obtiene estadísticas de las cuentas.
        
        Returns:
            tuple: (exito, mensaje, estadisticas)
        """
        try:
            # Obtener total de cuentas
            exito, mensaje, total_cuentas = self.obtener_conteo()
            if not exito:
                return False, mensaje, {}
            
            # Obtener cuentas activas
            exito_activas, _, cuentas_activas = self.obtener_cuentas_activas()
            total_activas = len(cuentas_activas) if exito_activas else 0
            
            # Calcular saldo total
            saldo_total = 0.0
            if exito_activas:
                for cuenta in cuentas_activas:
                    saldo_total += cuenta.get('saldo', 0.0)
            
            # Obtener cuentas por estado
            estados = {}
            for estado in ['Activa', 'Inactiva', 'Suspendida', 'Cerrada']:
                filtros = {'estado': estado}
                exito_filtro, _, conteo = self.obtener_conteo(filtros)
                if exito_filtro:
                    estados[estado] = conteo
            
            estadisticas = {
                'total_cuentas': total_cuentas,
                'cuentas_activas': total_activas,
                'saldo_total': round(saldo_total, 2),
                'cuentas_por_estado': estados
            }
            
            return True, "Estadísticas obtenidas exitosamente", estadisticas
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            return False, f"Error al obtener estadísticas: {str(e)}", {}
    
    def generar_numero_cuenta(self, codigo_banco: str = "003") -> str:
        """
        Genera un número de cuenta único.
        
        Args:
            codigo_banco: Código del banco (por defecto 003)
            
        Returns:
            str: Número de cuenta generado
        """
        try:
            import random
            import time
            
            # Obtener timestamp para unicidad
            timestamp = int(time.time())
            
            # Generar número aleatorio
            numero_aleatorio = random.randint(100000, 999999)
            
            # Formato: XXX-XXX-XXXXXX-XX
            numero_cuenta = f"{codigo_banco}-100-{numero_aleatorio:06d}-{timestamp % 100:02d}"
            
            # Verificar que no exista
            if not self._numero_cuenta_existe(numero_cuenta):
                return numero_cuenta
            else:
                # Si existe, generar otro
                return self.generar_numero_cuenta(codigo_banco)
                
        except Exception as e:
            logger.error(f"Error al generar número de cuenta: {str(e)}")
            return f"{codigo_banco}-100-000001-01"
    
    def _validar_cuenta_especifica(self, datos: Dict) -> Tuple[bool, str]:
        """
        Validaciones específicas del controlador de cuenta.
        
        Args:
            datos: Datos de la cuenta a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Verificar que el cliente existe
        if datos.get('id_cliente'):
            exito, _, cliente = self.cliente_model.leer(datos['id_cliente'])
            if not exito:
                return False, "El cliente seleccionado no existe"
        
        # Verificar saldo no negativo
        if datos.get('saldo') is not None:
            try:
                saldo = float(datos['saldo'])
                if saldo < 0:
                    return False, "El saldo no puede ser negativo"
            except (ValueError, TypeError):
                return False, "El saldo debe ser un número válido"
        
        return True, ""
    
    def _numero_cuenta_existe(self, numero_cuenta: str) -> bool:
        """
        Verifica si ya existe una cuenta con el número.
        
        Args:
            numero_cuenta: Número de cuenta a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            exito, _, _ = self.buscar_cuenta_por_numero(numero_cuenta)
            return exito
        except:
            return False
    
    def _cci_existe(self, cci: str) -> bool:
        """
        Verifica si ya existe una cuenta con el CCI.
        
        Args:
            cci: CCI a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        try:
            filtros = {'cci': cci}
            exito, _, cuentas = self.listar(filtros)
            return exito and len(cuentas) > 0
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
    
    def _numero_cuenta_existe_en_otra_cuenta(self, numero_cuenta: str, id_cuenta_actual: int) -> bool:
        """
        Verifica si el número existe en otra cuenta (para actualizaciones).
        
        Args:
            numero_cuenta: Número de cuenta a verificar
            id_cuenta_actual: ID de la cuenta que se está actualizando
            
        Returns:
            bool: True si existe en otra cuenta, False en caso contrario
        """
        try:
            exito, _, cuenta = self.buscar_cuenta_por_numero(numero_cuenta)
            if exito and cuenta['id_cuenta'] != id_cuenta_actual:
                return True
            return False
        except:
            return False
    
    def _cci_existe_en_otra_cuenta(self, cci: str, id_cuenta_actual: int) -> bool:
        """
        Verifica si el CCI existe en otra cuenta (para actualizaciones).
        
        Args:
            cci: CCI a verificar
            id_cuenta_actual: ID de la cuenta que se está actualizando
            
        Returns:
            bool: True si existe en otra cuenta, False en caso contrario
        """
        try:
            filtros = {'cci': cci}
            exito, _, cuentas = self.listar(filtros)
            if exito:
                for cuenta in cuentas:
                    if cuenta['id_cuenta'] != id_cuenta_actual:
                        return True
            return False
        except:
            return False
