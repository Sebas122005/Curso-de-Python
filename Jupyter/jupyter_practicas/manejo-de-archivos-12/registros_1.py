# Funciones y metodo para manejo de archivos secuenciales en disco
# El lenguaje Python provee las instrucciones para manejo de archivos en disco
# En la forma básica, la información que se puede almacenar en disco son cadenas de texto

# Apertura de un archivo
# f=open(n,t)

# t: tipo de operación a realizar con el archivo:
## Tipos de operación:
## 'w' crear el archivo y agregar datos. Si el archivo existe, lo borra y crea uno nuevo
## 'a' agregar datos al archivo. Si el archivo no existe lo crea y luego agrega
## 'r' lee datos del archivo
## 'r++' lee y escribe en el archivo

# Escritura de texto en el archivo
## f.write(s)
## s: es alguna variable que contiene la linea de texto
## Escribe en el archivo una línea de texto
## Fin de linea '\n'

# Lectura del contenido del archivo
## v=f.readline()
## En donde v es una variable que recibe la linea de texto
## Si no quedan lineas retorna una línea vacía
## Cierre de un archivo
## f.close()

# Al finalizar la operación con un archivo, debe cerrarse. En el ingreso de datos, esta 
# operación se necesita para completar el ingreso de los datos al archivo en el disco.
# Detectar la posición actual del dispositivo de lectura del archivo
# p=f.tell(123)

# p contendrá un entero con la posición actual. La posición inicial en el archivo es 0
# Ubicar el dispositivo de lectura del archivo en una posición especificada
# f.seek(p)
# d es el desplazamiento contado a partir del inicio que es la posición 0


import io #Modulo para manejo de archivos

archivo = open("registros.txt","w") #Abrir el archivo en modo escritura
texto='php\n'
archivo.write(texto) #Escribir en el archivo
texto='java\n'
archivo.write(texto) #Escribir en el archivo
texto='python\n'
archivo.write(texto) #Escribir en el archivo
archivo.close() #Cerrar el archivo

