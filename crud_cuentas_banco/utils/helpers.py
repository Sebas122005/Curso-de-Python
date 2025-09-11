"""
Funciones auxiliares y helpers para el sistema bancario.
Contiene utilidades generales y constantes.
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional
import re


# Constantes del sistema
class Constantes:
    """Constantes utilizadas en todo el sistema."""
    
    # Estados de cuenta
    ESTADOS_CUENTA = ['Activa', 'Inactiva', 'Suspendida', 'Cerrada']
    
    # Estados de tarjeta
    ESTADOS_TARJETA = ['Activa', 'Inactiva', 'Bloqueada', 'Vencida']
    
    # Tipos de movimiento
    TIPOS_MOVIMIENTO = ['Cargo', 'Abono', 'Transferencia', 'Compra', 'Retiro', 'Depósito']
    
    # Códigos de banco por defecto
    CODIGO_BANCO_DEFAULT = "003"
    
    # Límites del sistema
    SALDO_MAXIMO = 999999999999.99
    SALDO_MINIMO = 0.0
    
    # Longitudes máximas
    LONGITUD_MAXIMA_NOMBRE = 100
    LONGITUD_MAXIMA_EMAIL = 255
    LONGITUD_MAXIMA_TELEFONO = 20
    LONGITUD_MAXIMA_DOCUMENTO = 20
    LONGITUD_MAXIMA_USERNAME = 50
    LONGITUD_MAXIMA_PASSWORD = 100


def obtener_timestamp_actual() -> str:
    """
    Obtiene el timestamp actual formateado.
    
    Returns:
        str: Timestamp en formato YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def obtener_fecha_actual() -> str:
    """
    Obtiene la fecha actual en formato YYYY-MM-DD.
    
    Returns:
        str: Fecha actual
    """
    return date.today().strftime('%Y-%m-%d')


def formatear_nombre_completo(nombre: str, apellido_paterno: str, apellido_materno: str) -> str:
    """
    Formatea un nombre completo.
    
    Args:
        nombre: Nombre
        apellido_paterno: Apellido paterno
        apellido_materno: Apellido materno
        
    Returns:
        str: Nombre completo formateado
    """
    if not all([nombre, apellido_paterno, apellido_materno]):
        return "Nombre incompleto"
    
    return f"{apellido_paterno} {apellido_materno}, {nombre}"


def generar_numero_aleatorio(longitud: int = 6) -> str:
    """
    Genera un número aleatorio de la longitud especificada.
    
    Args:
        longitud: Longitud del número a generar
        
    Returns:
        str: Número aleatorio
    """
    import random
    return str(random.randint(10**(longitud-1), 10**longitud - 1))


def generar_codigo_verificacion() -> str:
    """
    Genera un código de verificación de 6 dígitos.
    
    Returns:
        str: Código de verificación
    """
    return generar_numero_aleatorio(6)


def formatear_numero_cuenta(codigo_banco: str = "003", codigo_agencia: str = "100") -> str:
    """
    Genera un número de cuenta formateado.
    
    Args:
        codigo_banco: Código del banco
        codigo_agencia: Código de la agencia
        
    Returns:
        str: Número de cuenta formateado
    """
    numero_secuencial = generar_numero_aleatorio(6)
    codigo_verificacion = generar_codigo_verificacion()[:2]
    
    return f"{codigo_banco}-{codigo_agencia}-{numero_secuencial}-{codigo_verificacion}"


def validar_formato_fecha(fecha_str: str, formato: str = '%Y-%m-%d') -> bool:
    """
    Valida si una fecha tiene el formato correcto.
    
    Args:
        fecha_str: Fecha como string
        formato: Formato esperado
        
    Returns:
        bool: True si el formato es correcto
    """
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False


def convertir_fecha_string(fecha_str: str, formato_origen: str = '%Y-%m-%d', 
                          formato_destino: str = '%d/%m/%Y') -> str:
    """
    Convierte una fecha de un formato a otro.
    
    Args:
        fecha_str: Fecha como string
        formato_origen: Formato original
        formato_destino: Formato destino
        
    Returns:
        str: Fecha convertida
    """
    try:
        fecha = datetime.strptime(fecha_str, formato_origen)
        return fecha.strftime(formato_destino)
    except ValueError:
        return fecha_str


def calcular_edad(fecha_nacimiento: str) -> int:
    """
    Calcula la edad basada en la fecha de nacimiento.
    
    Args:
        fecha_nacimiento: Fecha de nacimiento en formato YYYY-MM-DD
        
    Returns:
        int: Edad en años
    """
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        hoy = date.today()
        edad = hoy.year - fecha_nac.year
        
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
            edad -= 1
        
        return edad
    except ValueError:
        return 0


def es_mayor_de_edad(fecha_nacimiento: str, edad_minima: int = 18) -> bool:
    """
    Verifica si una persona es mayor de edad.
    
    Args:
        fecha_nacimiento: Fecha de nacimiento en formato YYYY-MM-DD
        edad_minima: Edad mínima requerida
        
    Returns:
        bool: True si es mayor de edad
    """
    edad = calcular_edad(fecha_nacimiento)
    return edad >= edad_minima


def formatear_monto_para_bd(monto: str) -> float:
    """
    Convierte un monto de string a float para la base de datos.
    
    Args:
        monto: Monto como string
        
    Returns:
        float: Monto como float
    """
    try:
        # Remover caracteres no numéricos excepto punto y coma
        monto_limpio = re.sub(r'[^\d.,]', '', str(monto))
        
        # Reemplazar coma por punto si es necesario
        if ',' in monto_limpio and '.' not in monto_limpio:
            monto_limpio = monto_limpio.replace(',', '.')
        
        return float(monto_limpio)
    except (ValueError, TypeError):
        return 0.0


def formatear_monto_para_mostrar(monto: float, moneda: str = "S/") -> str:
    """
    Formatea un monto para mostrar al usuario.
    
    Args:
        monto: Monto como float
        moneda: Símbolo de moneda
        
    Returns:
        str: Monto formateado
    """
    try:
        return f"{moneda} {monto:,.2f}"
    except (ValueError, TypeError):
        return f"{moneda} 0.00"


def crear_diccionario_respuesta(exito: bool, mensaje: str, datos: Any = None) -> Dict[str, Any]:
    """
    Crea un diccionario de respuesta estándar.
    
    Args:
        exito: Indica si la operación fue exitosa
        mensaje: Mensaje descriptivo
        datos: Datos adicionales (opcional)
        
    Returns:
        dict: Diccionario de respuesta
    """
    respuesta = {
        'exito': exito,
        'mensaje': mensaje,
        'timestamp': obtener_timestamp_actual()
    }
    
    if datos is not None:
        respuesta['datos'] = datos
    
    return respuesta


def extraer_iniciales(nombre: str, apellido_paterno: str, apellido_materno: str) -> str:
    """
    Extrae las iniciales de un nombre completo.
    
    Args:
        nombre: Nombre
        apellido_paterno: Apellido paterno
        apellido_materno: Apellido materno
        
    Returns:
        str: Iniciales
    """
    iniciales = ""
    
    if apellido_paterno:
        iniciales += apellido_paterno[0].upper()
    if apellido_materno:
        iniciales += apellido_materno[0].upper()
    if nombre:
        iniciales += nombre[0].upper()
    
    return iniciales


def truncar_texto(texto: str, longitud_maxima: int = 50) -> str:
    """
    Trunca un texto a la longitud máxima especificada.
    
    Args:
        texto: Texto a truncar
        longitud_maxima: Longitud máxima permitida
        
    Returns:
        str: Texto truncado
    """
    if not texto:
        return ""
    
    if len(texto) <= longitud_maxima:
        return texto
    
    return texto[:longitud_maxima-3] + "..."


def es_email_valido(email: str) -> bool:
    """
    Verifica si un email tiene formato válido.
    
    Args:
        email: Email a verificar
        
    Returns:
        bool: True si es válido
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def limpiar_telefono(telefono: str) -> str:
    """
    Limpia un número de teléfono removiendo caracteres no numéricos.
    
    Args:
        telefono: Teléfono a limpiar
        
    Returns:
        str: Teléfono limpio
    """
    if not telefono:
        return ""
    
    # Remover todo excepto números, + y espacios
    return re.sub(r'[^\d\s\+]', '', telefono).strip()


def obtener_mes_actual() -> str:
    """
    Obtiene el mes actual en formato YYYY-MM.
    
    Returns:
        str: Mes actual
    """
    return datetime.now().strftime('%Y-%m')


def obtener_año_actual() -> int:
    """
    Obtiene el año actual.
    
    Returns:
        int: Año actual
    """
    return datetime.now().year
