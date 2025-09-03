Data = {"nombre": "Juan", "edad": 28,
        "ciudad": "Madrid", "ocupacion": "Ingeniero"}
#Con coma
print("Nombre:", Data["nombre"])
#Usando el símbolo +
print("Edad:"+str(Data["edad"]))
print("Ciudad:", Data.get("ciudad"))
#Usando f-string
print(f"Ocupación: {Data['ocupacion']}")
