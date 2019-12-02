from Grammar import Grammar
from alphabet import Alphabet
from analizadorLexico import LexAnalizer
import sys

class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
    
    #Metodo cerradura, dado una regla con "punto" (indice)
    #regresara una lista con las reglas y sus "pintos"
    # Regresa lista de tuplas
    def closure(self, rule, index, reglasPasadas = list()):
        if (index == len(rule[1])) or (rule[1][index] in self.grammar.termSymbs):
            return [(rule, index)]
        else:   #Simbolo es NO terminal
                #Calculara la misma Cerradura
            auxRules = list()
            auxRules.append((rule, index))
            reglasPasadas.append((rule,index))
            nonTerm = rule[1][index]
            for ruleAux in self.grammar.rules:
                if nonTerm == ruleAux[0]:
                    tuplaAux = (ruleAux, 0)
                    if  tuplaAux not in reglasPasadas:
                        if (ruleAux == rule and index != 0) or (ruleAux != rule):
                            arAux = self.closure(ruleAux, 0, reglasPasadas)
                            auxRules.extend(arAux)
            #Eliminar reglas repetidas
            outRules = list()
            for ruleAux in auxRules:
                if ruleAux not in outRules:
                    outRules.append(ruleAux)
            return outRules
    
    
    
    #Funcion ir, recivbe un "estado" (lista de regla con punto) y un elemento,
    #devuleve otro "estado"
    def goTo(self, state, symbol):
        auxPairs = list()
        for pair in state:
            if len(pair[0][1]) > pair[1]:
                if symbol == pair[0][1][pair[1]]:
                    auxPairs.append((pair[0], pair[1]+1))
        #Calcular cerradura de cada nueva regla con punto
        newRules = list()
        for pair in auxPairs:
            newRules.extend(self.closure(pair[0], pair[1]))
        #Eliminar elementos repetidos
        finalRules = list()
        for rule in newRules:
            if rule not in finalRules:
                finalRules.append(rule)
        return finalRules

    #Funcion que devuelve el conjunto de items para aplicar la operacion "Ir"
    # Recibe un conjunto de reglas con punto (Estado)
    def getItemsMove(self, state):
        outItmes = list()
        for pair in state:
            #pair = ([NT,[r,e,g,l,a]], punto)
            if pair[1] < len(pair[0][1]):
                outItmes.append(pair[0][1][pair[1]])
        order = self.grammar.nonTermSymbs.copy()
        order.extend(self.grammar.termSymbs)
        order = ['^', 'SIN', 'num', '/', '-', '+', '*',')', '(', 'E', 'F', 'P','T']
        return sorted(list(set(outItmes)), key=order.index)


    def findTransition(self, arrayTrans, elemIni, objTrans):
        for trans in arrayTrans:
            if (elemIni == trans[0]) and (objTrans == trans[1]):
                return trans[2]
        return -1

    def createSets(self):
        states = list()
        transitions = list()
        #Crear el primer "estado"
        states.append(self.closure(self.grammar.rules[0], 0))
        apunt = 0
        while apunt < len(states):
            #Traer Itmes del estado
            items = self.getItemsMove(states[apunt])
            #Verificar transciones (IrA)
            for item in items:
                newState = self.goTo(states[apunt], item)
                #Verificar au no existe ese estado
                if newState not in states:  #Aun no existe
                    states.append(newState)
                #Crear trasicion
                indexStateTo = states.index(newState)
                transitions.append((apunt, item, indexStateTo))
            apunt += 1
        #Una vez creada todas las transiciones "llenamos la tabla"
        return states, transitions
    
    def getReduction(self, state):
        for item in state:
            #Econtrar elemento con . al final
            if item [1] == len(item[0][1]):
                #Regla "Aceptar"
                if (item[0] == self.grammar.rules[0]):
                        return ([Alphabet.symbol_STRINGEND], Alphabet.symbol_ACCEPT)
                #Calcular reducciones
                else:
                    return (self.grammar.follow(item[0][0]), "r{}".format(self.grammar.rules.index(item[0])))

    def popItemReduction(self, reduction, symbol):
        if isinstance(reduction, tuple):
            elements = reduction[0]
            strOut = reduction[1]
            for elem in elements:
                if elem == symbol:
                    reduction[0].pop(reduction[0].index(elem))
                    return strOut
            return ""
        else:
            return ""


    def createTableLR0(self):
        #Creamos los conjuntos de "reglas"
        states, transitions = self.createSets()
        #Crear cabecera con simboloes terminales y no-terminales
        headTb = list()
        headTb.append("")
        headTb .extend(sorted(self.grammar.termSymbs.copy()))
        headTb.append(Alphabet.symbol_STRINGEND)
        headTb.extend(self.grammar.nonTermSymbs.copy())
        bodyTb = list()
        for state in states:
            rowAux = list()
            idState = states.index(state)
            rowAux.append(idState)
            reduction = self.getReduction(state)
            for elem in headTb:
                if(elem != ""):
                    getElemTo =self.findTransition(transitions, idState, elem) 
                    if getElemTo == -1:
                        if reduction == None or len(reduction[0]) == 0:
                            rowAux.append("")
                        else:
                            rowAux.append(self.popItemReduction(reduction, elem))
                    else:
                        rowAux.append("d{}".format(getElemTo))
            #Insertar la Fila
            bodyTb.append(rowAux)
        return headTb, bodyTb
    
    def findAction(self, state, symbol, table):
        idSymbol = table[0].index(symbol)
        #Recorrer filas de la tabla
        action = table[1][int(state)][idSymbol]    #El primer indice es del estado 
        if action == '':
            return [-1]
        elif action[0] == "d":
            return [action]
        elif action[0] == "r": #Reduccion:
            numRule = action.replace('r', '')
            return [action, self.grammar.rules[int(numRule)]]
        elif action == Alphabet.symbol_ACCEPT:
            return [action]
        return [-1]

    def analizeStr(self, stringAn, lexAnString, dicSymbTerm):
        #Crear tabla de transcion
        headTb, bodyTb = self.createTableLR0()
        #Crear tabla de accion
        actionTable = (headTb, bodyTb)
        stringAn += Alphabet.symbol_STRINGEND
        invertDict = dict(map(reversed, dicSymbTerm.items()))
        #registros
        regString, regStack, regAction = list(), list(), list()
        #Inicializar los registros
        regStack.append([0])
        regString.append(stringAn)
        #Pedir Accion
        statusLexStr = lexAnString.statusLex()
        auxLexem = lexAnString.yylex()
        regAction.append(self.findAction(0, invertDict[auxLexem[0]], actionTable))
        lexAnString.statusLex(statusLexStr)
        #Variable para el ultimo lexema
        lastLexemFound = list()
        complete = False
        while not complete:
            #Socilicar ulmtima informacion en las pilas
            auxStack = regStack[-1].copy()
            auxAction = regAction[-1].copy()
            auxString = regString[-1]
            if auxAction[0] == -1:
                print("Error en la cadena analizada por LRO")
                sys.exit()
            #Accion Valida
            if auxAction[0][0] == "r":    #Reduccion
                #Sacar elementos de la pila
                for cont in range(2*len(auxAction[1][1])):  #Pop a la |Regla|   
                    auxStack.pop()
                lastState = auxStack[-1]
                auxStack.append(auxAction[1][0])
                getAction = self.findAction(lastState,auxAction[1][0], actionTable)
                auxState = getAction[0]
                auxStack.append(int(auxState[1::]))  #Insertar el "estado" 
                regString.append(auxString)
            elif auxAction[0][0] == "d":  #Desplazamiento
                auxLexem = lexAnString.yylex()
                lastLexemFound = auxLexem.copy()
                #Pop a la cadena
                stringOut = ""
                stringPop = list(auxString)
                #Funcion pop
                for i in range(0, len(lastLexemFound[1])):
                    stringPop.pop(0)
                for car in stringPop:   #Reconstruir la cadena
                    stringOut += car
                #Insertar en los registros
                auxStack.append(invertDict[lastLexemFound[0]])
                auxState = auxAction[0]
                auxStack.append(auxState[1::])    #Estado
                regString.append(stringOut)
            #Ultimo en la pila
            regStack.append(auxStack)   
            #Buscar Accion
            if regString[-1][0] == Alphabet.symbol_STRINGEND:
                regAction.append(self.findAction(auxStack[-1], Alphabet.symbol_STRINGEND, actionTable))            
                if regAction[-1][0] == Alphabet.symbol_ACCEPT:
                    complete = True
            else:
                statusLexStr = lexAnString.statusLex()
                auxLexem = lexAnString.yylex()
                regAction.append(self.findAction(auxStack[-1], invertDict[auxLexem[0]], actionTable))
                lexAnString.statusLex(statusLexStr)

        return regStack, regString, regAction

def main():
    pathGR = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/gram_LR1.txt"
    gr = Grammar(pathGR)
    LRTest = LR0(gr)
    anString = "2.97*6+5*(4-8)*SIN(16)"
    lexAnString = LexAnalizer.createLexFile("/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/lex_LR0.txt", anString)
    #Diccionario
    pathDict = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/dictFile_LR0.txt" #Belmont
    #Crear diccionario
    symbArray = list()
    tokenArray = list()
    dictFile = open(pathDict, "r")
    fileLines = dictFile.readlines()
    for line in fileLines:
        auxArray = line.split()
        symbArray.append(auxArray[0])
        tokenArray.append(auxArray[1])
    dictTerm = dict(zip(symbArray, tokenArray))

    reg1, reg2, reg3 = LRTest.analizeStr(anString, lexAnString, dictTerm)
if __name__ == "__main__":
    main()