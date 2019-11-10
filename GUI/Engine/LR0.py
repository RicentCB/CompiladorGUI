from Grammar import Grammar
from alphabet import Alphabet

class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
    
    #Metodo cerradura, dado una regla con "punto" (indice)
    #regresara una lista con las reglas y sus "pintos"
    # Regresa lista de tuplas
    def closure(self, rule, index):
        if (index == len(rule[1])) or (rule[1][index] in self.grammar.termSymbs):
            return [(rule, index)]
        else:   #Simbolo es NO terminal
                #Calculara la misma Cerradura
            auxRules = list()
            auxRules.append((rule, index))
            nonTerm = rule[1][index]
            for ruleAux in self.grammar.rules:
                if nonTerm == ruleAux[0]:
                    if (ruleAux == rule and index != 0) or (ruleAux != rule):
                        arAux = self.closure(ruleAux, 0)
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
    
    def printArray(self,array):
        for elem in array:
            print(elem)

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
        order = ["E", "T", "F", "(", "num", "+", "*", ")"]
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
        print("\t",self.grammar.rules[0])
        for item in state:
            if item [1] == len(item[0][1]):
                #Regla "Aceptar"
                if (item[0] == self.grammar.rules[0]):
                        return Alphabet.symbol_ACCEPT
                #Calcular reducciones
                else:
                    return self.grammar.follow(item[0][0])
    
    def createTableLR1(self):
        #Creamos los conjuntos de "reglas"
        states, transitions = self.createSets()
        #Crear cabecera con simboloes terminales y no-terminales
        headTb = list()
        headTb.append("")
        headTb .extend(self.grammar.termSymbs.copy())
        headTb.append(Alphabet.symbol_STRINGEND)
        headTb.extend(self.grammar.nonTermSymbs.copy())
        bodyTb = list()
        for state in states:
            rowAux = list()
            idState = states.index(state)
            rowAux.append(idState)
            red = self.getReduction(state)
            for elem in headTb:
                getElemTo =self.findTransition(transitions, idState, elem) 
                if getElemTo == -1:
                    rowAux.append("")
                else:
                    rowAux.append(getElemTo)
            #Insertar la Fila
            bodyTb.append(rowAux)

        # print(headTb)
        # for row in bodyTb:
        #     print(row)
        # print()
        print("T", self.grammar.follow("T"))

        



def main():
    pathGR = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/gramLR0.txt"
    gr = Grammar(pathGR)
    LRTest = LR0(gr)
    LRTest.createTableLR1()
    # for rule in LRTest.grammar.rules:
    #     print(rule)
    # print()
    # rule = LRTest.grammar.rules[0]
    # print(rule)
    # print()
    # state0 = LRTest.C(rule, 0)
    # for tupla in state0:
    #     print(tupla)
    # print()
    # state1 = LRTest.goTo(state0, "(")
    # for pair in state1:
    #     print(pair)
if __name__ == "__main__":
    main()