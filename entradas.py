# Tienda de Ropa
'''print("Tienda de Ropa")

list_ropa = {"pantalones": 40, "camisas": 30, "zapatos": 50, "vestidos": 60, "faldas": 35, "sombreros": 20, "chaquetas": 80, "abrigos": 100, "bufandas": 15,
             "guantes": 25, "calcetines": 10, "camisetas": 25, "sudaderas": 45, "trajes": 90, "corbatas": 30, "cinturones": 20, "gafas": 70, "relojes": 150, "joyas": 200}

key=False
print("Prendas disponibles:")
for ropa, precio in list_ropa.items():
    print(f"- {ropa.capitalize()}: ${precio}")
while not key:
    ropa = input("Ingrese la prenda que desea comprar (o 'salir' para terminar): ").lower()
    if ropa == 'salir':
        key = True
        print("Gracias por su visita. ¡Hasta luego!")
    elif ropa.lower() in list_ropa.keys():
        print(f"El precio de {ropa} es: ${list_ropa[ropa]}")
    else:
        print("Prenda no disponible. Por favor, elija otra prenda.")
'''
#Calculadora Simple
'''
pase = False
while not pase:
    print("Calculadora Simple")
    num1 = float(input("Ingrese el primer número: "))
    num2 = float(input("Ingrese el segundo número: "))
    operacion = input("Ingrese la operación (+, -, *, /, **, o 'salir' para terminar): ")
    if operacion.lower() == 'salir':
        pase = True
        print("Gracias por usar la calculadora. ¡Hasta luego!")
        continue
    if operacion == '+': # Suma
        resultado = num1 + num2
    elif operacion == '-': # Resta
        resultado = num1 - num2

    elif operacion == '*': # Multiplicación
        resultado = num1 * num2
    elif operacion == '**': # Potenciación
        resultado = num1 ** num2
    elif operacion == '/': # División
        if num2 != 0: 
            resultado = num1 / num2
        else:
            resultado = "Error: División por cero no permitida."
    else: # Operación no válida
        resultado = "Operación no válida."
    print(f"El resultado de {num1} {operacion} {num2} es: {resultado}")
'''
#Pagos a Trabajadores
print("Pagos a Trabajadores")
try:
    nombre = input("Ingrese su nombre: ")
    horas_trabajadas = float(input("Ingrese las horas trabajadas en la semana: "))
    tarifa_hora = float(input("Ingrese la tarifa por hora: "))
    salario_semanal = horas_trabajadas * tarifa_hora
    print(f"Saludos {nombre}, su salario semanal es: ${salario_semanal:.2f}")

except Exception as e:
    print("Error: Por favor, ingrese valores numéricos válidos para las horas trabajadas y la tarifa por hora.")
    print(f"Detalles del error: {e}")
    
