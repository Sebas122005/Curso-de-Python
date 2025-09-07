import modulo_1 as m1
import math
from modulo_1 import raizCuadrada as raiz

def imprimir_pi():
    print("El valor de pi es:", m1.pi)


def calcular_area_circulo(radio):
    area = round(m1.areaCirculo(radio), 2)
    print(f"El área del círculo con radio {radio} es: {area}")
    return area

def calcular_area_triangulo(base, altura):
    area = round(m1.areaTriangulo(base, altura),2)
    print(f"El área del triángulo con base {base} y altura {altura} es: {area}")
    return area

def calcular_raiz_cuadrada(numero):
    resultado = round(raiz(numero), 2)
    print(f"La raíz cuadrada de {numero} es: {resultado}")
    return resultado

def calcular_potencia(base, exponente):
    resultado = round(m1.potencia(base, exponente), 2)
    print(f"{base} elevado a la {exponente} es: {resultado}")
    return resultado

def calcular_seno(grados):
    resultado = round(m1.seno(grados), 2)
    print(f"El seno de {grados} grados es: {resultado}")
    return resultado

def main():
    imprimir_pi()
    calcular_raiz_cuadrada(25)
    calcular_area_circulo(5)
    calcular_area_triangulo(4, 6)

if __name__ == "__main__":
    main()

def usos_math():
    print("Usos del módulo math:")
    print("Valor de e:", math.e)
    print("Valor de pi:", math.pi)
    print("Raíz cuadrada de 16:", math.sqrt(16))
    print("Logaritmo natural de e:", math.log(math.e))
    print("Seno de 90 grados (en radianes):", math.sin(math.radians(90)))
    print("Coseno de 0 grados (en radianes):", math.cos(math.radians(0)))
    print("Tangente de 45 grados (en radianes):", math.tan(math.radians(45)))