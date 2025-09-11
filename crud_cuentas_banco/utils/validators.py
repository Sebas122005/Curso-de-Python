"""
Utilidades de validación para el sistema bancario.
Contiene funciones de validación reutilizables.
"""

import re
from datetime import datetime, date
from typing import Tuple, Optional


def validar_email(email: str) -> Tuple[bool, str]:
    """
    Valida el formato de un email.
    
    Args:
        email: Email a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not email:
        return False, "El email es requerido"
    
    if len(email) > 255:
        return False, "El email no puede exceder 255 caracteres"
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        return False, "El formato del email no es válido"
    
    return True, ""


def validar_telefono(telefono: str) -> Tuple[bool, str]:
    """
    Valida el formato de un teléfono.
    
    Args:
        telefono: Teléfono a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not telefono:
        return True, ""  # Teléfono es opcional
    
    if len(telefono) > 20:
        return False, "El teléfono no puede exceder 20 caracteres"
    
    # Permitir números, espacios, guiones y paréntesis
    patron = r'^[\d\s\-\(\)\+]+$'
    if not re.match(patron, telefono):
        return False, "El teléfono solo puede contener números, espacios, guiones, paréntesis y el signo +"
    
    return True, ""


def validar_fecha(fecha_str: str, formato: str = '%Y-%m-%d') -> Tuple[bool, str]:
    """
    Valida el formato de una fecha.
    
    Args:
        fecha_str: Fecha como string
        formato: Formato esperado de la fecha
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not fecha_str:
        return True, ""  # Fecha es opcional en algunos casos
    
    try:
        fecha = datetime.strptime(fecha_str, formato).date()
        return True, ""
    except ValueError:
        return False, f"La fecha debe tener el formato {formato}"


def validar_fecha_nacimiento(fecha_str: str) -> Tuple[bool, str]:
    """
    Valida una fecha de nacimiento.
    
    Args:
        fecha_str: Fecha de nacimiento como string
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not fecha_str:
        return True, ""  # Fecha de nacimiento es opcional
    
    es_valido, mensaje = validar_fecha(fecha_str)
    if not es_valido:
        return False, mensaje
    
    try:
        fecha_nacimiento = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hoy = date.today()
        
        # Verificar que no sea futura
        if fecha_nacimiento > hoy:
            return False, "La fecha de nacimiento no puede ser futura"
        
        # Verificar que no sea muy antigua (más de 120 años)
        if fecha_nacimiento.year < (hoy.year - 120):
            return False, "La fecha de nacimiento no puede ser anterior a 120 años"
        
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido"


def validar_numero_cuenta(numero: str) -> Tuple[bool, str]:
    """
    Valida el formato de un número de cuenta bancaria.
    Formato esperado: XXX-XXX-XXXXXX-XX
    
    Args:
        numero: Número de cuenta a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not numero:
        return False, "El número de cuenta es requerido"
    
    if len(numero) > 50:
        return False, "El número de cuenta no puede exceder 50 caracteres"
    
    patron = r'^\d{3}-\d{3}-\d{6}-\d{2}$'
    if not re.match(patron, numero):
        return False, "El número de cuenta debe tener el formato XXX-XXX-XXXXXX-XX"
    
    return True, ""


def validar_cci(cci: str) -> Tuple[bool, str]:
    """
    Valida el formato de un CCI (Código de Cuenta Interbancario).
    Formato esperado: XXX-XXX-XXXXXX-XX
    
    Args:
        cci: CCI a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not cci:
        return False, "El CCI es requerido"
    
    if len(cci) > 25:
        return False, "El CCI no puede exceder 25 caracteres"
    
    patron = r'^\d{3}-\d{3}-\d{6}-\d{2}$'
    if not re.match(patron, cci):
        return False, "El CCI debe tener el formato XXX-XXX-XXXXXX-XX"
    
    return True, ""


def validar_saldo(saldo: str) -> Tuple[bool, str, Optional[float]]:
    """
    Valida un saldo monetario.
    
    Args:
        saldo: Saldo como string
        
    Returns:
        tuple: (es_valido, mensaje_error, saldo_float)
    """
    if not saldo:
        return False, "El saldo es requerido", None
    
    try:
        saldo_float = float(saldo)
        if saldo_float < 0:
            return False, "El saldo no puede ser negativo", None
        
        # Verificar que no sea demasiado grande
        if saldo_float > 999999999999.99:
            return False, "El saldo es demasiado grande", None
        
        return True, "", saldo_float
    except (ValueError, TypeError):
        return False, "El saldo debe ser un número válido", None


def validar_username(username: str) -> Tuple[bool, str]:
    """
    Valida el formato de un nombre de usuario.
    
    Args:
        username: Nombre de usuario a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not username:
        return False, "El nombre de usuario es requerido"
    
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if len(username) > 50:
        return False, "El nombre de usuario no puede exceder 50 caracteres"
    
    patron = r'^[a-zA-Z0-9_]+$'
    if not re.match(patron, username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, ""


def validar_password(password: str) -> Tuple[bool, str]:
    """
    Valida el formato de una contraseña.
    
    Args:
        password: Contraseña a validar
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    if len(password) > 100:
        return False, "La contraseña no puede exceder 100 caracteres"
    
    return True, ""


def validar_documento(numero_documento: str, tipo_documento: str = None) -> Tuple[bool, str]:
    """
    Valida el formato de un número de documento.
    
    Args:
        numero_documento: Número de documento a validar
        tipo_documento: Tipo de documento (opcional)
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if not numero_documento:
        return False, "El número de documento es requerido"
    
    if len(numero_documento) > 20:
        return False, "El número de documento no puede exceder 20 caracteres"
    
    # Validaciones específicas por tipo de documento
    if tipo_documento:
        if tipo_documento.lower() == 'dni':
            # DNI peruano: 8 dígitos
            if not re.match(r'^\d{8}$', numero_documento):
                return False, "El DNI debe tener exactamente 8 dígitos"
        elif 'extranjeria' in tipo_documento.lower():
            # Carné de extranjería: letra seguida de 8-9 dígitos
            if not re.match(r'^[A-Z]\d{8,9}$', numero_documento):
                return False, "El carné de extranjería debe tener una letra seguida de 8-9 dígitos"
        elif 'pasaporte' in tipo_documento.lower():
            # Pasaporte: alfanumérico
            if not re.match(r'^[A-Z0-9]{6,12}$', numero_documento):
                return False, "El pasaporte debe tener entre 6 y 12 caracteres alfanuméricos"
    
    return True, ""


def validar_campos_requeridos(datos: dict, campos_requeridos: list) -> Tuple[bool, str]:
    """
    Valida que todos los campos requeridos estén presentes.
    
    Args:
        datos: Diccionario con los datos
        campos_requeridos: Lista de campos requeridos
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    campos_faltantes = []
    
    for campo in campos_requeridos:
        if campo not in datos or not datos[campo]:
            campos_faltantes.append(campo)
    
    if campos_faltantes:
        return False, f"Los siguientes campos son requeridos: {', '.join(campos_faltantes)}"
    
    return True, ""


def validar_longitud_campo(valor: str, campo: str, longitud_maxima: int) -> Tuple[bool, str]:
    """
    Valida la longitud máxima de un campo.
    
    Args:
        valor: Valor a validar
        campo: Nombre del campo (para mensaje de error)
        longitud_maxima: Longitud máxima permitida
        
    Returns:
        tuple: (es_valido, mensaje_error)
    """
    if valor and len(valor) > longitud_maxima:
        return False, f"El campo {campo} no puede exceder {longitud_maxima} caracteres"
    
    return True, ""


def limpiar_string(valor: str) -> str:
    """
    Limpia un string eliminando espacios extra.
    
    Args:
        valor: String a limpiar
        
    Returns:
        str: String limpio
    """
    if not valor:
        return ""
    
    return valor.strip()


def formatear_monto(monto: float) -> str:
    """
    Formatea un monto monetario para mostrar.
    
    Args:
        monto: Monto a formatear
        
    Returns:
        str: Monto formateado
    """
    return f"S/ {monto:,.2f}"


def formatear_fecha(fecha: date, formato: str = '%d/%m/%Y') -> str:
    """
    Formatea una fecha para mostrar.
    
    Args:
        fecha: Fecha a formatear
        formato: Formato deseado
        
    Returns:
        str: Fecha formateada
    """
    if not fecha:
        return ""
    
    return fecha.strftime(formato)
