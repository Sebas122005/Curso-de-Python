print("Generador de Contraseñas")
import random
import string
longitud = int(input("Ingrese la longitud deseada para la contraseña (mínimo 6 caracteres): "))
if longitud < 6:
    print("La longitud mínima para una contraseña segura es de 6 caracteres.")
else:
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    print(f"Contraseña generada: {contraseña}")
