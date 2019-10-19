import sys
import json
import pickle
from AFN import AFN
from state import State


#Funcion que retorna el id mas grande de todos los AFNS insertados
def setLastIdState(filePath):
    #Leer el archivo de AFNS
    fileRead = open(filePath, 'rb')
    AFNS = pickle.load(fileRead)
    fileRead.close()
    lastId = 0
    for Afn in AFNS:
        lastId += len(Afn.states)
    #Enviar Last Id a la clase estado
    if (lastId > 0):
        State.id_state = lastId
        

#Main que se conecta con los archivos de python por medio de nodejs
#Recibe argumentos por medio de la "consola"
if len(sys.argv) > 5:
    print(json.dumps({"message":"Error en numero de argumentos"}))
else:   #Numero de argumentos valido
    if(sys.argv[1] == "AFN"):
        #Leer el archivo de objetos serializados
        fileAFN = "/home/ricardo/ESCOM/5 Semestre/Compiladores/CompiladorGUI/GUI/Engine/AFNS.txt"
        #Enviar Ultimo Id a la Clase Estado
        setLastIdState(fileAFN)
        if (sys.argv[2] == "Inicializar"):  #Inicializa Arreglo de Automtas
            array = []
            fileObjWrite = open(fileAFN, 'wb')
            pickle.dump(array,fileObjWrite)
            fileObjWrite.close()
        #Opciones del Menu Principal
        elif(sys.argv[2] == "Basico"):
            if (len(sys.argv[3]) == 1):
                
                #Abrir Archivo de Automatas
                fileObjRead = open(fileAFN, 'rb')
                arrayAFN = pickle.load(fileObjRead) 
                #Crear Nuevo Automata
                basicAFN = AFN.createBasicAutomata(sys.argv[3])
                #Insertarlo en el arreglo y en escribir el archivo
                arrayAFN.append(basicAFN)
                fileObjWrite = open(fileAFN, 'wb')
                pickle.dump(arrayAFN, fileObjWrite)
                fileObjWrite.close()
                #Imprimir la respuesta
                print(json.dumps({"AFN":basicAFN.toJSON(), "Id": len(arrayAFN), "message": True}))
            else:
                print(json.dumps({"message":"Error en en automata basico"}))
        elif(sys.argv[2] == "Rango"):
            if (len(sys.argv[3]) == 3):
                #Abrir Archivo de Automatas
                fileObjRead = open(fileAFN, 'rb')
                arrayAFN = pickle.load(fileObjRead) 
                #Crear Nuevo Automata
                rangeAFN = AFN.createRangeAutomata(sys.argv[3][0],sys.argv[3][2])
                #Insertarlo en el arreglo y en escribir el archivo
                arrayAFN.append(rangeAFN)
                fileObjWrite = open(fileAFN, 'wb')
                pickle.dump(arrayAFN, fileObjWrite)
                fileObjWrite.close()
                #Imprimir la respuesta
                print(json.dumps({"AFN":rangeAFN.toJSON(), "Id":len(arrayAFN), "message": True}))
            else:
                print(json.dumps({"message":"Error en en automata rango"}))
        else:
            print(json.dumps({"message": "Error opcion AFN no valida"}));
