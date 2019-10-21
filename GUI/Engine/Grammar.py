import sys
from alphabet import Alphabet
from alphabet import Token
from regEx import RegularExp
from AFD import AFD
from analizadorLexico import LexAnalizer

#Clase Gramtica que construye una tabla LL a partir de un archivo dada una gramatica
class Grammar():

    def __init__(self, path):
        if isinstance(path, str):
            self.contAux = 1
            self.rules = []
            self.lastR = ""
            self.lastL = []
            #Abrir archivo de Gramatica
            self.file = open(path, "r")
            self.strGrammar = ""
            fileLines = self.file.readlines()
            for line in fileLines:
                for car in line:
                    if car != "\n":
                        self.strGrammar += car
            #Crear Analizador Lexico para Gramaticas
            regExp1 = "((A-Z)|(a-z))&((A-Z)|(a-z)|(0-9)|('))*"
            regExp2 = "(-)&(>)"
            regExp3 = "(;)"
            regExp4 = "( )+"
            regExp5 = "(\|)"
            regExpArray = [regExp1, regExp2, regExp3, regExp4, regExp5]
            tokenArray = [Token.grammar_SIMBOLO, Token.grammar_FLECHA, Token.grammar_PC, Token.grammar_SPACE, Token.grammar_OR]
            AFDMain = AFD.createSuperAFD(regExpArray, tokenArray)
            self.lexAn = LexAnalizer(AFDMain, self.strGrammar)

        else:
            sys.exit()
    #Metodo que devuelve el token dado por el analizador lexico
    def getToken(self):
        if (self.lexAn.apCarActual < len(self.strGrammar)-1):
            token = self.lexAn.yylex()  #Devuelve el token y lexema
            if token[0] == -1:
                print("Error en la gramatica.")
                sys.exit()
            #Token valido
            elif token[0] == Token.grammar_SPACE:
                return self.getToken()
            else:
                self.lastLexema = token[1]
                return token[0]
        else:
            return -1
    #Metodo que envia o recibe el estado del analizador lexico
    def status(self, status=None):
        return self.lexAn.statusLex(status);
    
    #Empieza el Descenso recursivo para la creacion de gramaticas
    def G(self):
        if self.ListaReglas():
            #Insertar La ultima Regla
            if len(self.lastR) > 0:
                self.rules.append([self.lastL, self.lastR])
            return True
        else:
            return False
    
    def ListaReglas(self):
        token = -1
        if self.Regla():
            token = self.getToken()
            if token == Token.grammar_PC:
                if self.ListaReglasP():
                    return True
        else:
            return False
    
    def ListaReglasP(self):
        token = -1
        status = self.status()
        if self.Regla():
            token = self.getToken()
            if token == Token.grammar_PC:
                # print("--Ultima regla", self.rules[len(self.rules)-1])
                if self.ListaReglasP():
                    return True
                return False
        self.status(status)
        return True 

    def Regla(self):
        token = -1
        if self.LadoIzquierdo():
            token = self.getToken()
            if token == Token.grammar_FLECHA:
                if self.LadosDerechos():
                    return True
        return False

    def LadoIzquierdo(self, s = None):
        token = -1
        token = self.getToken()
        if token == Token.grammar_SIMBOLO:
            strLex = self.lastLexema
            #Unir lado derecho y lado izquierdo
            if len(self.lastR) > 0:
                self.rules.append([self.lastL, self.lastR])
            self.lastL = strLex
            #Vaciar el arreglo auxuliar para lados izquierdos
            self.lastR = []     
            return True
        return False
    
    def LadosDerechos(self):    #(String s)
        #Nodo N
        if self.ListaSimbolos(): #(N)
            #ArrReglas[IndArrelgo].Simb = s;
            #ArrReglas[IndeArreglo].Ap=N
            #IndiceArrelgo ++
            if self.LadosDerechosP(): #(s)
                return True
        return False

    def LadosDerechosP(self):
        #Nodo N
        status = self.status()
        token = -1
        token = self.getToken()
        if token == Token.grammar_OR:
            if self.ListaSimbolos():
                arrayRuleAux1 =[]
                arrayRuleAux2 =[]
                ap = 0
                #Dividir el arreglo de lado derecho en dos partes con el "OR"
                for elem in self.lastR:
                    if ap < len(self.lastR) - self.contAux:
                        arrayRuleAux1.append(elem)
                    else:
                        arrayRuleAux2.append(elem)
                    ap += 1
                self.lastR = []
                #Insertar en la lista de Reglas
                if len(arrayRuleAux1)>0:
                    self.rules.append([self.lastL,arrayRuleAux1])
                self.rules.append([self.lastL,arrayRuleAux2])

                #Continuar con el desceno recursivo    
                if self.LadosDerechosP(): #(S)
                    return True
            return False
        self.status(status) #Hay "Epsilon"
        return True

    def ListaSimbolos(self):
        #Nodo N
        token = -1
        token = self.getToken()
        if token == Token.grammar_SIMBOLO:
            #Insertar Lexema en el arreglo de lados derechos
            arrayAux = self.lastR.copy()
            arrayAux.append(self.lastLexema)
            
            self.contAux = 1
            self.lastR = arrayAux.copy()
            #N = New Nodo(Lexico.getLexema)
            if self.ListaSimbolosP():   #N2
                #N.ApSig = N2
                return True
        return False

    def ListaSimbolosP(self):
        status = self.status()
        token = -1
        token = self.getToken()
        if token == Token.grammar_SIMBOLO:
            #Insertar Lexema en el arreglo de lados derechos
            arrayAux = self.lastR.copy()
            arrayAux.append(self.lastLexema)

            self.lastR = arrayAux.copy()
            self.contAux += 1
            #N = New Nodo(Lexico.getLexema())
            if self.ListaSimbolosP():   #N2
                #N.ApSig = N2
                return True
            return False
        self.status(status)
        return True

    def simbolos_NoTerminales(self):
        terminales = []
        for rule in self.rules:
            terminales.append(rule[0])
        return set(terminales)

    def simbolosTerminales(self):
        no_terminales = []
        for regla in self.rules:
            for simbolo in regla[1]:
                if simbolo not in self.simbolos_NoTerminales():
                    no_terminales.append(simbolo)
        return set(no_terminales)
    
    def first(self, regla, regla_anterior=[]):        
        c_first = []
        terminales = self.simbolosTerminales()
        #print("En first: "+regla[0])
        if(regla[0]=="Epsilon"):    
            #c_first.append(regla[0])
            return regla[0]

        elif regla[0] in terminales:
            #c_first.append(regla[0])
            return regla[0]
        else:
        #Para el caso de que es un simbolo no terminal
            #contador = 0
            for rule in self.rules:
                if rule[0]==regla[0]:
                    
                    if self.is_nullable(regla[0]) == False:
                        first_auxiliar = self.first(rule[1],rule[1])
                        if isinstance(first_auxiliar, str):
                            c_first.append(first_auxiliar)
                        else:
                            c_first = c_first + first_auxiliar
                    elif self.is_nullable(regla[0]) and (regla[0] in self.simbolos_NoTerminales()):
                        #print(f"Regla 0 : {regla[0]}")
                        eliminar_epsilon = False 
                        first_auxiliar2 = self.first(rule[1])
                        c_first.append(first_auxiliar2)
                        contador = 0
                        if len(regla_anterior) > 1:
                            eliminar_epsilon = True
                            for simbolo in regla_anterior:
                                if self.is_nullable(simbolo):
                                    contador = contador+1
                                else:
                                    break
                            for i in range(contador+1):
                                #print(i)
                                indice = regla_anterior.index(regla[0])+i
                                first_auxiliar = self.first(regla_anterior[indice])
                                if isinstance(first_auxiliar, str):
                                    c_first.append(first_auxiliar)
                                else:
                                    c_first = c_first + first_auxiliar
                        # print(f"Afuera: {eliminar_epsilon}")
                        # print(f"Antes de eliminar: {c_first}")
                        # print(f"Despues de eliminar: {auxiliar2}")
                        if eliminar_epsilon is True:
                            auxiliar1 = set(c_first)
                            auxiliar1.discard('Epsilon')
                            auxiliar2 = list(auxiliar1)
                            #print(f"En cond {auxiliar2}")
                            c_first = auxiliar2  
            #Quitamos elementos repetidos
            auxiliar = []
            for simbolo in c_first:
                if simbolo not in auxiliar:
                    auxiliar.append(simbolo)
            return auxiliar

    #Esta función determina determina si una regla
    #contiene producciones con epsilon, es decir, que 
    #puede ser omitida
    def is_nullable(self, regla):
        nullable = False
        for rule in self.rules:
            if rule[0] == regla[0]:
                if 'Epsilon' in rule[1]:
                    nullable = True
        return nullable
    # def follow(self, s_noTerminal):
    #     c_follow = []
    #     if(s_noTerminal==self.rules[0][0]):
    #         c_follow.append("$")
    #         return c_follow
    #     for rule in self.rules:
    #         if s_noTerminal in rule[1]:
    #             if(rule[1].index(s_noTerminal)):
    #                 print("Si jala")
                


if __name__ == "__main__":
    path = "c:/Users/brian/Documents/CompiladorGUI/GUI/Engine/Gramatica.txt"
    g1 = Grammar(path)
    g1.G()
    # no_terminales = g1.simbolos_NoTerminales()
    # terminales = g1.simbolosTerminales()
    for rule in g1.rules:
        print(rule)
    #print(g1.rules[0][0])
    # print("---Simbolos terminales---")
    # for simbolo in terminales:
    #     print(simbolo)
    # print("---Simbolos no terminales---")
    # for simbolo in no_terminales:
    #     print(simbolo)
    # print(g1.rules[4])
    print("---First---")
    for simbolo in g1.rules:
        first = g1.first(simbolo, simbolo)
        print(f"First de {simbolo[0]}: {first}")
        #print(simbolo[0])