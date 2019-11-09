from Grammar import Grammar
from alphabet import Alphabet

class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
    
    #Metodo cerradura, dado una regla con "punto" (indice)
    #regresara una lista con las reglas y sus "pintos"
    # Regresa lista de tuplas
    def closure(self, rule, index):
        # print(rule[1][index])
        # print(self.grammar.termSymbs)
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
    def moveTo(self, state, symbol):
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
        order = self.grammar.nonTermSymbs
        order.extend(self.grammar.termSymbs)
        order = ["E", "T", "F", "(", "num", "+", "*", ")"]
        return sorted(list(set(outItmes)), key=order.index)

    # def printState(self, state):
    #     for tup in state:
    #         print(tup[0][0],"->",tup[0][1], tup[1])

    #Funcion que crea los desplazamientos LR0
    def createTableMoves(self):
        states = list()
        transtions = list()
        #Crear el primer "estado"
        states.append(self.closure(self.grammar.rules[0], 0))
        apunt = 0
        while apunt < len(states):
            #Traer Itmes del estado
            items = self.getItemsMove(states[apunt])
            #Verificar transciones (IrA)
            for item in items:
                newState = self.moveTo(states[apunt], item)
                #Verificar au no existe ese estado
                if newState not in states:  #Aun no existe
                    states.append(newState)
                #Crear trasicion
                indexStateTo = states.index(newState)
                transtions.append((apunt, item, indexStateTo))
            apunt += 1
        #Una vez creada todas las transiciones "llenamos la tabla"
        headTb = self.grammar.termSymbs
        headTb.append(Ala)

        self.printArray(states)
        print(len(states))
        



def main():
    pathGR = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/gramLR0.txt"
    gr = Grammar(pathGR)
    LRTest = LR0(gr)
    LRTest.createTableMoves()
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
    # state1 = LRTest.moveTo(state0, "(")
    # for pair in state1:
    #     print(pair)
if __name__ == "__main__":
    main()