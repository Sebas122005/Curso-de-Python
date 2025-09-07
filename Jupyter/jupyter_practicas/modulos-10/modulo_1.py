# Modulos: Archivo que contiene metodos, variables, y sirve a otros Archivos
import math
pi = 3.1416

#Area de un circulo\n",
def areaCirculo(radio):
    return pi * (radio**2)

#Area de un Triangulo\n",
def areaTriangulo(base,altura):
    return (base*altura)/2

def raizCuadrada(numero):
    return math.sqrt(numero)

def potencia(base, exponente):
    return math.pow(base, exponente)

def coseno(grados):
    radianes = math.radians(grados)
    return math.cos(radianes)

def seno(grados):
    radianes = math.radians(grados)
    return math.sin(radianes)

def tangente(grados):
    radianes = math.radians(grados)
    return math.tan(radianes)

def pintar_area(area):
    print(f'El area es: {area}')
       