import sys
import json
from AFN import AFN

#Main que se conecta con los archivos de python por medio de nodejs
#Recibe argumentos por medio de la "consola"

if len(sys.argv) > 5:
    print(json.dumps({"message":"Error en numero de argumentos"}))
else:   #Numero de argumentos valido
    if(sys.argv[1] == "AFN"):
        if(sys.argv[2] == "Basico"):
            if (len(sys.argv[3]) == 1):
                basicAFN = AFN.createBasicAutomata(sys.argv[3])
                print(json.dumps(basicAFN.toJSON()))
            else:
                print(json.dumps({"message":"Error en en automata basico"}))
        elif(sys.argv[2] == "Rango"):
            if (len(sys.argv[3]) == 3):
                rangeAFN = AFN.createRangeAutomata(sys.argv[3][0],sys.argv[3][2])
                print(json.dumps(rangeAFN.toJSON()))
            else:
                print(json.dumps({"message":"Error en en automata basico"}))
        else:
            print(json.dumps({"message": "Error opcion AFN no valida"}));
