import sys
import json
import pickle
from AFN import AFN
from state import State
from Grammar import Grammar
from analizadorLexico import LexAnalizer
from LR0 import LR0

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

#Funcion que abre un archivo serializado
#Retorna lo que hay en dicho archivo
def openFileSerial(pathFile):
    #Abrir Archivo de Automatas
    fileObjRead = open(pathFile, 'rb')
    objectSerial = pickle.load(fileObjRead) 
    fileObjRead.close()
    return objectSerial


#Funcion que inserta un AFN en un array y lo serializa
#Retorna la longitud del array
def pushArrayAFN(arrayAFN, objAFN, pathFile):
    #Insertarlo en el arreglo y en escribir el archivo
    arrayAFN.append(objAFN)
    fileObjWrite = open(pathFile, 'wb')
    pickle.dump(arrayAFN, fileObjWrite)
    fileObjWrite.close()
    return len(arrayAFN)

#Crea un diccionario dado un archivo 
def createDictFile(pathFile):
    symbArray = list()
    tokenArray = list()
    dictFile = open(pathFile, "r")
    fileLines = dictFile.readlines()
    for line in fileLines:
        auxArray = line.split()
        symbArray.append(auxArray[0])
        tokenArray.append(auxArray[1])
    dictOut = dict(zip(symbArray, tokenArray))
    return dictOut
        

#Main que se conecta con los archivos de python por medio de nodejs
#Recibe argumentos por medio de la "consola"
if len(sys.argv) > 7:
    print(json.dumps({"message":"Error en numero de argumentos"}))
else:   #Numero de argumentos valido
    if(sys.argv[1] == "AFN"):
        #Leer el archivo de objetos serializados
        fileAFN = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/files/AFNS.txt"
        #Enviar Ultimo Id a la Clase Estado
        setLastIdState(fileAFN)
        if (sys.argv[2] == "Inicializar"):  #Inicializa Arreglo de Automtas
            array = list()
            fileObjWrite = open(fileAFN, 'wb')
            pickle.dump(array,fileObjWrite)
            fileObjWrite.close()
        #----------- Opciones del Menu Principal -----------
        # ---- B A S I C O ----
        elif(sys.argv[2] == "Basico"):
            if (len(sys.argv[3]) == 1):
                #Crear Nuevo Automata
                basicAFN = AFN.createBasicAutomata(sys.argv[3])
                #Abrir Array AFN
                arrayAFN = openFileSerial(fileAFN)
                #Insertarlo y serializar
                idAfn = pushArrayAFN(arrayAFN, basicAFN, fileAFN)
                #Imprimir la respuesta
                print(json.dumps({"AFN":basicAFN.toJSON(), "Id":idAfn, "message": True}))
            else:
                print(json.dumps({"message":"Error en en automata basico"}))
        # ---- R A N G O ----
        elif(sys.argv[2] == "Rango"):
            if (len(sys.argv[3]) == 3):
                #Crear Nuevo Automata
                rangeAFN = AFN.createRangeAutomata(sys.argv[3][0],sys.argv[3][2])
                #Abrir Array AFN
                arrayAFN = openFileSerial(fileAFN)
                #Insertarlo y serializar
                idAfn = pushArrayAFN(arrayAFN, rangeAFN, fileAFN)
                #Imprimir la respuesta
                print(json.dumps({"AFN":rangeAFN.toJSON(), "Id":idAfn, "message": True}))
            else:
                print(json.dumps({"message":"Error en en automata rango"}))
        # ---- C O N C A T E N A R ----       
        elif(sys.argv[2] == "Concatenar"):
            #Abrir Array AFN
            arrayAFN = openFileSerial(fileAFN)
            #Adquirir los dos AFN de la lista
            AFN1 = arrayAFN[int(sys.argv[3])]
            AFN2 = arrayAFN[int(sys.argv[4])]
            #Crearmos el nuevo AFN
            AFNConc = AFN1.concatenate(AFN2)
            #Insertarlo y serializar
            idAfn = pushArrayAFN(arrayAFN, AFNConc, fileAFN)
            #Imprimir la respuesta
            print(json.dumps({"AFN":AFNConc.toJSON(), "Id":idAfn, "message": True}))        
        # ---- O P C I O N A L ----
        elif(sys.argv[2] == "Opcional"):
            #Deserializar el array AFN
            arrayAFN = openFileSerial(fileAFN)
            #Nuevo AFN
            AFNOp = arrayAFN[int(sys.argv[3])]  #Adquirir AFN de la lista
            AFNNew = AFNOp.optional()           #Crear nuevo AFN
            #Insertartlo en el array y escribir el archivo
            idAfn = pushArrayAFN(arrayAFN, AFNNew, fileAFN)
            #Imprimir la respuesta
            print(json.dumps({"AFN":AFNNew.toJSON(), "Id":idAfn, "message": True}))
        # ---- K L   P L U S ----
        elif(sys.argv[2] == "Plus"):
            #Deserializar el array AFN
            arrayAFN = openFileSerial(fileAFN)
            #Adquirir AFN de la lista
            AFNPlus = arrayAFN[int(sys.argv[3])]
            AFNNew = AFNPlus.kleene_plus()      #Crear nuevo AFN
            #Insertartlo en el array y escribir el archivo
            idAfn = pushArrayAFN(arrayAFN, AFNNew, fileAFN)
            #Imprimir la respuesta
            print(json.dumps({"AFN":AFNNew.toJSON(), "Id":idAfn, "message": True}))
        # ---- K L   S T A R ----
        elif(sys.argv[2] == "Star"):
            #Deserializar el array AFN
            arrayAFN = openFileSerial(fileAFN)
            #Adquirir AFN de la lista
            AFNStar = arrayAFN[int(sys.argv[3])]
            AFNNew = AFNStar.kleene_star()          #Crear nuevo AFN
            #Insertartlo en el array y escribir el archivo
            idAfn = pushArrayAFN(arrayAFN, AFNNew, fileAFN)
            #Imprimir la respuesta
            print(json.dumps({"AFN":AFNNew.toJSON(), "Id":idAfn, "message": True}))
        
        else:
            print(json.dumps({"message": "Error opcion AFN no valida"}));
    #Opciones de Gramatica
    elif(sys.argv[1] == "Grammar"):
        fileGrammar = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/files/grammar.txt"
        if(sys.argv[2] == "PathLL1"):
            #Creamos un objeto gramatica y guardamos 
            fileObjectGrammar = open(fileGrammar, 'wb')
            gramObject = Grammar(sys.argv[3])
            pickle.dump(sys.argv[3], fileObjectGrammar)
            fileObjectGrammar.close()
            #Crear tabla ll1 y mostrarla
            head, body = gramObject.creatTableLL1()
            print(json.dumps({"Head":head, "Body":body, "message": True}))
        #Analizar una cadena con LL1
        elif(sys.argv[2] == "StringLL1"):
            fileObjRead = open(fileGrammar, 'rb')
            pathStringGrammar = pickle.load(fileObjRead) 
            fileObjRead.close()
            #Creamos la gramatica
            gramObj = Grammar(pathStringGrammar)
            #Crear analizador Lexico
            pathLex = sys.argv[4]
            lexAn = LexAnalizer.createLexFile(pathLex, sys.argv[3])
            #Crear diccinario
            dictStr = createDictFile(sys.argv[5])
            #Analizar la cadena
            stack, string, action = gramObj.analizeStr(sys.argv[3], lexAn, dictStr)
            print(json.dumps({"Stack":stack, "String":string, "Action":action, "message":True}))
        #Crear Tabla LRO
        elif(sys.argv[2] == "PathLR0"):
            #Creamos un objeto gramatica y guardamos 
            fileObjectGrammar = open(fileGrammar, 'wb')
            gramObject = Grammar(sys.argv[3])
            pickle.dump(sys.argv[3], fileObjectGrammar)
            fileObjectGrammar.close()
            #Crear tabla ll1 y mostrarla
            LR0Obj = LR0(gramObject)
            head, body = LR0Obj.createTableLR1()
            print(json.dumps({"Head":head, "Body":body, "message": True}))
        #Analizar una cadena con LR0
        elif(sys.argv[2] == "StringLR0"):
            fileObjRead = open(fileGrammar, 'rb')
            pathStringGrammar = pickle.load(fileObjRead) 
            fileObjRead.close()
            #Creamos la gramatica
            gramObj = Grammar(pathStringGrammar)
            #Crear analizador Lexico
            pathLex = sys.argv[4]
            lexAn = LexAnalizer.createLexFile(pathLex, sys.argv[3])
            #Crear diccinario
            dictStr = createDictFile(sys.argv[5])
            #Crear LRO
            LR = LR0(gramObj)
            #Analizar la cadena
            stack, string, action = LR.analizeStr(sys.argv[3], lexAn, dictStr)
            print(json.dumps({"Stack":stack, "String":string, "Action":action, "message":True}))
        else:
            print(json.dumps({"message": "Error opcion Grammar no valida"}));
