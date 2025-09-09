

def metodo_for():
    value=[]
    for i in range(1,101):
        value.append(i)
    return value

def metodo_archivo():
    file = open('newfile.txt','w')
    file.write('Primera Linea '+str(metodo_for())+'\n')
    file.close()
    print('Primer Write terminado y cerrado')

    file= open('newfile.txt','a')
    file.write('Segunda Linea '+str(metodo_for())+'\n')


    print('Continua a Leer')
    file= open('newfile.txt','r')
    contenido= file.readline()
    file.close()
    print(contenido)

def metodo_error_escritura_en_archivo():
    bandera=True
    file=''
    while bandera==True:
        try:
            file=input('Ingrese el nombre del archivo: ')
            archivo=open(file+".txt",'a')
        except FileNotFoundError:
            print('El archivo no existe')
            crear = input('Desea crearlo? (s/n): ')
            if crear.lower()=='s':
                file= open(file+".txt",'w')
                print('Archivo creado')
                bandera=False
            else:
                print('Saliendo del programa')
                bandera=False
        else:
            contenido = input('Ingrese el contenido a escribir en el archivo: ')
            archivo.write(str(contenido+'\n'))
            print('Contenido escrito en el archivo')
        finally:
            print('Contenido en el archivo escrito:\n')
            archivo.close()
            archivo=open(file+".txt",'r')
            valores=archivo.readline(3)
            archivo.close()
            print(str(valores))
            bandera=False

metodo_error_escritura_en_archivo()