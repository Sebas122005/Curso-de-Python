# Archivo: Cliente.py
# Contiene la definición de la clase Cliente.

class Cliente:
    def __init__(self, codigo, nombre, ape_paterno, ape_materno, credito):
        self.codigo = codigo
        self.nombre = nombre
        self.ape_paterno = ape_paterno
        self.ape_materno = ape_materno
        self.credito = credito
    
    def __str__(self):
        return f'Codigo: {self.codigo}, Nombre: {self.nombre}, Apellido Paterno: {self.ape_paterno}, Apellido Materno: {self.ape_materno}, Credito: {self.credito}'
    

    