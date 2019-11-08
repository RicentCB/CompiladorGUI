from Grammar import Grammar

class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
    
    #Metodo cerradura, dado una regla con "punto" (indice)
    #regresara una lista con las reglas y sus "pintos"
    # Regresa lista de tuplas
    def C(self, rule, index):
        # print(rule[1][index])
        # print(self.grammar.termSymbs)
        if (index == len(rule[1])) or (rule[1][index] in self.grammar.termSymbs):
            return [(rule, index)]
        else:   #Simbolo es NO terminal
                #Calculara la misma Cerradura
            auxRules = list()
            auxRules.append((rule, index))
            for ruleAux in self.grammar.rules:
                if (ruleAux[0] == rule[1][index]) and (ruleAux != rule):
                    arAux = self.C(ruleAux, 0)
                    auxRules.extend(arAux)
            #Eliminar reglas repetidas
            outRules = list()
            for ruleAux in auxRules:
                if ruleAux not in outRules:
                    outRules.append(ruleAux)
            return outRules
    
    #Funcion que devuelve el conjunto de items para aplicar la operacion "Ir"
    # Recibe un conjunto de reglas con punto (Estado)
    def getItemsMove(self, state):
        outItmes = list()
        for pair in state:
            #pair = ([NT,[r,e,g,l,a]], punto)
            if pair[1] < len(pair[0][1]):
                outItmes.append(pair[0][1][pair[1]])
        return sorted(list(set(outItmes)))
    
    #Funcion ir, recivbe un "estado" (lista de regla con punto) y un elemento,
    #devuleve otro "estado"
    def moveTo(self, state, symbol):
        auxPairs = list()
        for pair in state:
            #pair = ([NT,[r,e,g,l,a]], punto)
            if symbol == pair[0][1][pair[1]]:
                auxPairs.append((pair[0], pair[1]+1))
        #Calcular cerradura de cada nueva regla con punto
        newRules = list()
        for pair in auxPairs:
            newRules.extend(self.C(pair[0], pair[1]))
        #Eliminar elementos repetidos
        finalRules = list()
        for rule in newRules:
            if rule not in finalRules:
                finalRules.append(rule)
        return finalRules
    
    #Funcion que crea los desplazamientos LR0
    def createTableMoves(self):
        states = list()
        states.append(self.C(self.grammar.rules[0], 0))
        print(states)



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