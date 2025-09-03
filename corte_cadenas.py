
print("Ejemplo de corte de cadenas en Python")

entrada= input("Introducir una cadena:")
print("Cadena introducida:", entrada)
caracter_initial=int(input("Introducir la posicion inicial del corte:"))
caracter_final=int(input("Introducir la posicion del caracter final del corte:"))
cadena_corteda=entrada[caracter_initial:caracter_final]
print("Cadena cortada:", cadena_corteda)

acciones={'Mayusculas':cadena_corteda.upper(),
          'Minusculas':cadena_corteda.lower(),
          'Reemplazar espacios por guiones':cadena_corteda.replace(" ","-"),
          'Contar caracteres':len(cadena_corteda),
          'Salir':"Salir"
          }
print("Acciones disponibles:")
for accion in acciones:
    print(accion)
print("Seleccionar una accion:")
accion_seleccionada=input()
while accion_seleccionada not in acciones:
    print("Accion no valida, seleccionar una accion:")
    accion_seleccionada=input()
if accion_seleccionada!="Salir":
    print("Resultado de la accion",accion_seleccionada,":",acciones[accion_seleccionada])

escapadores={'Nueva linea':"\n",
            'Tabulador':"\t",
            'Comilla simple':"\'",
            'Comilla doble':'\"',
            'Barra invertida':"\\",
            'Regresar al inicio de la linea':"\r",
            'Salir':"Salir"
            }

print("Escapadores disponibles:")
for escapador in escapadores:
    print(escapador)
print("Seleccionar un escapador:")
escapador_seleccionado=input()
while escapador_seleccionado not in escapadores:
    print("Escapador no valido, seleccionar un escapador:")
    escapador_seleccionado=input()
if escapador_seleccionado!="Salir":
    print("Resultado del escapador",escapador_seleccionado,":",escapadores[escapador_seleccionado])
