# print("Funciones String")

def capitalizar(texto):
    """Convierte la primera letra en mayúscula."""
    return texto.capitalize()
# print(capitalizar("hola mundo"))

def casefold(texto):
    """Convierte todo el texto a minúsculas de manera más agresiva que lower()."""
    return texto.casefold()
#print(casefold("HOLA MUNDO"))

def center(texto, ancho, caracter=' '):
    """Centra el texto en un campo de ancho especificado, rellenando con el caracter dado."""
    return texto.center(ancho, caracter)
#print(center("Hola Mundo", 50, '*'))

def count(texto, subcadena, inicio=0, fin=None):
    """Cuenta las ocurrencias de una subcadena en el texto."""
    return texto.count(subcadena, inicio, fin if fin is not None else len(texto))
#print(count("Hola Mundo, Hola a todos", "Hola",0, 20))

def endwith(texto, sufijo, inicio=0, fin=None):
    """Verifica si el texto termina con la subcadena dada."""
    return texto.endswith(sufijo, inicio, fin if fin is not None else len(texto))
#print(endwith("Hola Mundo", "undo"))

def find(texto, subcadena, inicio=0, fin=None):
    """Busca la primera ocurrencia de una subcadena y devuelve su índice, o -1 si no se encuentra."""
    return texto.find(subcadena, inicio, fin if fin is not None else len(texto))    
#print(find("Hola Mundo", "undo"))

def formato(texto, *args, **kwargs):
    """Formatea el texto usando los argumentos posicionales y de palabra clave."""
    return texto.format(*args, **kwargs)
#print(formato("Hola {}, bienvenido a {}", "Juan", "Python"))

def alfanumerico(texto):
    """Verifica si el texto es alfanumérico."""
    return texto.isalnum()
#print(alfanumerico("HolaMundo123*^^¿?´´"))

def alfabetico(texto):
    """Verifica si el texto es alfabético."""
    return texto.isalpha()
#print(alfabetico("HolaMundo"))

def esminuscula(texto):
    """Verifica si todas las letras del texto están en minúsculas."""
    return texto.islower()
#print(esminuscula("hola mundo"))

def esmayuscula(texto):
    """Verifica si todas las letras del texto están en mayúsculas."""
    return texto.isupper()
#print(esmayuscula("HOLA MUNDO"))

def esnumero(texto):
    """Verifica si el texto es numérico."""
    return texto.isnumeric()
#print(esnumero("12345"))


def esespacio(texto):
    """Verifica si el texto contiene solo espacios en blanco."""
    return texto.isspace()
#print(esespacio("    "))

def unir(texto, iterable):
    """Une los elementos de un iterable en una cadena, separados por el texto dado."""
    return texto.join(iterable)

#print(unir(" ", ["Hola", "Mundo", "Python"]))

def convertir_minusculas(texto):
    """Convierte todas las letras del texto a minúsculas."""
    return texto.lower()
#print(convertir_minusculas("HOLA MUNDO PYTHON 3.11 *^^¿?´´ "))


def funciion_lstrip(texto, caracteres=None):
    """Elimina los caracteres especificados del inicio del texto."""
    return texto.lstrip(caracteres)
#print(funciion_lstrip("   Hola Mundo   "))

def maketrans(texto ,mapeo):
    """Crea una tabla de traducción para usar con translate()."""
    return texto.maketrans(mapeo)
#dato="Hola Sebas 12132323232"
#print(dato.translate(maketrans(dato,{"H": "h", "S": "s", "1": "hhh", "2": "", "3": ""})))

def paticionar(texto, separador=None, maxsplit=-1):
    """Divide el texto en una lista usando el separador dado."""
    return texto.partition(separador)
#print(paticionar("Hola Mundo, bienvenido a Python", "bienvenido"))

def reemplazar(texto, viejo, nuevo, maxreemplazos=-1):
    """Reemplaza las ocurrencias de una subcadena por otra."""
    return texto.replace(viejo, nuevo, maxreemplazos)   
#print(reemplazar("Hola Mundo, Hola a todos", "Hola", "Adiós", 1))

def separar(texto, separador=None, maxsplit=-1):
    """Divide el texto en una lista usando el separador dado."""
    return texto.split(separador,maxsplit)
#print(separar("Hola Mundo, bienvenido a Python", " ", 2))

def separar_lineas(texto, mantener_saltos=False):
    """Divide el texto en una lista de líneas."""
    return texto.splitlines(mantener_saltos)
#print(separar_lineas("Hola Mundo\nbienvenido a Python\n¿cómo estás?"))

def limpiar_espacios(texto, caracteres=None):
    """Elimina los caracteres especificados del inicio y final del texto."""
    return texto.strip(caracteres)
#print(limpiar_espacios("    .,@#$%&/()=?¿!¡*    Hola Mundo  .,@#$%&/()=?¿!¡*  ", " .,@#$%&/()=?¿!¡*"))

def invertir_caso(texto):
    """Invierte el caso de todas las letras en el texto.(De mayúsculas a minúsculas y viceversa)"""
    return texto.swapcase()
#print(invertir_caso("Hola Mundo, Bienvenido a Python 3.11"))

def titulo(texto):
    """Convierte la primera letra de cada palabra en mayúscula."""
    return texto.title()
#print(titulo("hola a todos este es un titulo"))

def convertir_mayusculas(texto):
    """Convierte todas las letras del texto a mayúsculas."""
    return texto.upper()
#print(convertir_mayusculas('Este texto se convertira en mayusculas'))

def comentarios_largos_multilinea():
    """
    Esta es una función de ejemplo que no hace nada.
    Se utiliza para demostrar cómo escribir comentarios largos
    o documentación en múltiples líneas.
    """
    pass

