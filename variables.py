variables = {"int" :1, # integer
             "float": 1.8, # float
             "string": "string", # string
             "bool": True, # boolean
             "list": [1, 2, 3], # list
             "dict": {'key': 'value'}, # dictionary
             "tuple": (1, 2, 3), # tuple
             "set": {1, 2, 3}, # set
             "none": None} # NoneType

for var_type, var_value in variables.items():
    print(f"Type: {type(var_value)}, Value: {var_value}")

print(f"Variables Keys : {variables.keys()} || Variables Values : {variables.values()}")

list = [1, 2, 3, 4, 5]
print(f"List before modification: {list[3:5]}")
list[3:5] = [8, 9]
print(f"List after modification: {list[3:5]}")

list.append(6)
print(f"List after appending 6: {list}")