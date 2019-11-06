import sys
import pickle

from alphabet import Alphabet
from alphabet import Token
from regEx import RegularExp
from AFD import AFD
from analizadorLexico import LexAnalizer

#Clase Gramtica que construye una tabla LL a partir de un archivo dada una gramatica
class Grammar():

    def __init__(self, path):
        if isinstance(path, str):
            #Analizar Cadena

            #Descenso Recursivo
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
            #Modificar de acuerdo a la ruta especifica
            pathLexAn = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/files/analizadorLexicoGramatica.txt"
            #pathLexAn = "c:/Users/brian/Documents/CompiladorGUI/GUI/Engine/analizadorLexicoGramatica.txt"
            #Crear Analizador Lexico para Gramaticas
            # regExp1 = "(-)|(\&)|(\()|(\))|(\?)|(\*)|(\+)|(((A-Z)|(a-z))&((A-Z)|(a-z)|(0-9)|('))*)"
            # regExp2 = "(-)&(>)"
            # regExp3 = "(;)"
            # regExp4 = "( )+"
            # regExp5 = "(\|)"
            # regExpArray = [regExp1, regExp2, regExp3, regExp4, regExp5]
            # tokenArray = [Token.grammar_SIMBOLO, Token.grammar_FLECHA, Token.grammar_PC, Token.grammar_SPACE, Token.grammar_OR]
            # AFDMain = AFD.createSuperAFD(regExpArray, tokenArray)
            # #Serializacion de Objeto AFDN MAIN
            # fileObjWrite = open(pathLexAn, 'wb')
            # pickle.dump(AFDMain, fileObjWrite)
            # fileObjWrite.close()
            # Deserializacion del Objeto
            fileObjRead = open(pathLexAn, 'rb')
            objectSerialAFD = pickle.load(fileObjRead) 
            fileObjRead.close()
            #Asignacion
            lexAnal = LexAnalizer(objectSerialAFD, self.strGrammar)
            self.lexAn = lexAnal

        else:
            sys.exit()

    def error(self, message=""):
        print("Error en {message}")
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

    # --- TERMINA DESCENO RECURSIVO ----
    def simbolos_NoTerminales(self):
        terminales = list()
        for rule in self.rules:
            terminales.append(rule[0])
        return sorted(set(terminales))

    def simbolosTerminales(self):
        no_terminales = list()
        for regla in self.rules:
            for simbolo in regla[1]:
                if simbolo not in self.simbolos_NoTerminales():
                    no_terminales.append(simbolo)
        return sorted(set(no_terminales))
    
    def first(self, regla, regla_anterior=[]):        
        c_first = []
        terminales = self.simbolosTerminales()
        #print("En first: "+regla[0])
        if(regla[0]==Alphabet.symbol_EPSILON):    
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
                        if eliminar_epsilon is True:
                            auxiliar1 = set(c_first)
                            auxiliar1.discard(Alphabet.symbol_EPSILON)
                            auxiliar2 = list(auxiliar1)
                            #print(f"En cond {auxiliar2}")
                            c_first = auxiliar2  
            #Quitamos elementos repetidos
            auxiliar = []
            for simbolo in c_first:
                if simbolo not in auxiliar:
                    auxiliar.append(simbolo)
            return auxiliar

    #Esta función determina si una regla
    #contiene producciones con epsilon, es decir, que 
    #puede ser omitida
    def is_nullable(self, regla):
        nullable = False
        for rule in self.rules:
            if rule[0] == regla[0]:
                if Alphabet.symbol_EPSILON in rule[1]:
                    nullable = True
        return nullable
    def follow(self, s_noTerminal):
        eliminar_epsilon = False
        c_follow = []
        ocurrencias = 0
        reglas_auxiliar = []
        for rule in self.rules:
            if s_noTerminal in rule[1]:
                ocurrencias = ocurrencias+1
                reglas_auxiliar.append(rule)
        if(s_noTerminal==self.rules[0][0] and ocurrencias == 0):
            return ['$']
        if(s_noTerminal==self.rules[0][0]):
            c_follow.append("$")
        for rule in reglas_auxiliar:
            if s_noTerminal in rule[1] and rule[1].index(s_noTerminal) < len(rule[1])-1:
                indice = rule[1].index(s_noTerminal)+1
                first_auxiliar = self.first([rule[1][indice]])
                if self.is_nullable([rule[1][indice]]):
                    follow_auxiliar = self.follow(rule[1][indice])
                    if isinstance(first_auxiliar,str):
                        c_follow.append(first_auxiliar)
                    else:
                        c_follow = c_follow + first_auxiliar
                    if isinstance(follow_auxiliar,str):
                        c_follow.append(follow_auxiliar)
                    else:
                        c_follow = c_follow + follow_auxiliar
                    eliminar_epsilon = True
                else:
                    if isinstance(first_auxiliar,str):
                        c_follow.append(first_auxiliar)
                    else:
                        c_follow = c_follow + first_auxiliar
                if eliminar_epsilon:
                    c_follow.remove(Alphabet.symbol_EPSILON)
                return c_follow
            elif s_noTerminal in rule[1] and rule[1].index(s_noTerminal) == len(rule[1])-1:
                auxiliar = self.follow(rule[0])
                if isinstance(auxiliar,str):
                    c_follow.append(auxiliar)
                else:
                    c_follow = c_follow + auxiliar
                return c_follow
    
    def creatTableLL1(self): 
        self.G()
        terminales = list(self.simbolosTerminales())
        terminales.append('$')
        if Alphabet.symbol_EPSILON in terminales:
            terminales.remove(Alphabet.symbol_EPSILON)
        no_terminales = list(self.simbolos_NoTerminales())
        no_terminales.append('$')
        #Llenamos la tabla con los no terminales en la cabecera y los terminales en el principio
        tabla_ll1 = [[no_terminales[j-1] if i==0 and j>0 else ' ' for i in range(len(terminales)+1)] for j in range(len(no_terminales)+1)]
        tabla_ll1[0] = list(set(tabla_ll1[0]))+terminales
        #Obtenemos el contenido de la tabla
        n_regla = 1
        for rule in self.rules:
            first_aux1 = self.first(rule[1])
            first_aux = []
            if isinstance(first_aux1,str):
                first_aux.append(first_aux1)
            else:
                first_aux = first_aux + first_aux1
            if Alphabet.symbol_EPSILON in first_aux:
                follow_aux = self.follow(rule[0])
                insertar(tabla_ll1,rule[0], follow_aux,n_regla,rule[1])
            else:
               insertar(tabla_ll1,rule[0],first_aux,n_regla,rule[1])
            n_regla = n_regla+1
        
        body =[]
        for cont in range (1,len(tabla_ll1)):
            body.append(tabla_ll1[cont])
        return tabla_ll1[0], body
    
    #Metodo que devuelve la "accion" dado el simbolo NO terminal, y otro simbolo
    def findAction(self, notTermSym, thermSym, table):    
        for row in table[1]:
            #Analizar "cuerpo de la tabla"
            if row[0] == notTermSym:
                #Encontrar simbolo
                foundedSym = False
                cont = 0
                for cont in range (0, len(table[0])):
                    if table[0][cont] == thermSym:
                        foundedSym = True
                        break
                # Regresar simbolo
                if(foundedSym):
                    return row[cont]
                else:
                    return False
        #No se encontro el simbolo no terminal
        return False
    
    #Funcion que analiza una cadena de la gramatica, 
    # devolvera 3 arreglos de "historial" (Pila, cadena, accion)
    def analizeStr(self, stringAn, lexAnString, dicSymbTerm):
        arraySymTerminal = dicSymbTerm.keys()
        #Pedir Tabla de acciones
        headTb, bodyTb = self.creatTableLL1()
        tableAction = [headTb, bodyTb]
        #Registros
        regStack = list()         #Columna de "registro"
        regString = list()         #Columna de la cadena
        regAction = list()         #Columna de Accion
        #Insertar Datos Iniciales
        stringAn += Alphabet.symbol_STRINGEND
        regString.append(stringAn)
        regStack.append([Alphabet.symbol_STRINGEND,self.rules[0][0]])
        statusLexStr = lexAnString.statusLex()
        auxLexem = lexAnString.yylex()
        invertDict = dict(map(reversed, dicSymbTerm.items()))
        regAction.append(self.findAction(self.rules[0][0], invertDict[auxLexem[0]], tableAction))
        lexAnString.statusLex(statusLexStr)
        #Variable que almacena el ultimo lexema con token encontrado
        lastLexemFound = list()
        complete = False
        while not complete:
            #Solicitar ulitmos elementos en los registros
            auxStack = regStack[len(regStack)-1].copy()

            auxAction = regAction[len(regAction)-1]
            if isinstance(auxAction[0], list):
                auxAction = regAction[len(regAction)-1][0].copy()

            auxString = regString[len(regString)-1]
            #Ultimo item encontrado
            auxStack.pop()
            if auxAction[0] == "pop":
                #Accion POP
                stringOut = ""
                stringPop = list(auxString)
                #Funcion pop
                for i in range(0, len(lastLexemFound[1])):
                    stringPop.pop(0)
                for car in stringPop:
                    stringOut += car
                #Insertar en los registros
                regStack.append(auxStack)
                regString.append(stringOut)

            elif auxAction[0] == Alphabet.symbol_EPSILON:
                regStack.append(auxStack)
                auxString = regString[len(regString)-1]
                regString.append(auxString)
            
            else:
                #Accion encotrada
                auxAction.reverse()
                for elem in auxAction:
                    auxStack.append(elem)
                regStack.append(auxStack)
                regString.append(auxString)
                
            #Ultimo simbolo
            lastItemStack = auxStack[len(auxStack)-1]
            #Encontrar si el ulitmo simbolo de la pila es o no simbolo terminal
            if lastItemStack in arraySymTerminal:
                auxLexem = lexAnString.yylex()
                lastLexemFound = auxLexem.copy()
                tokenDict = dicSymbTerm[lastItemStack]
                if tokenDict == auxLexem[0]:
                    regAction.append(["pop"])
                else:
                    return False, False, False
            elif regString[len(regString)-1][0] == Alphabet.symbol_STRINGEND:
                if (lastItemStack == Alphabet.symbol_STRINGEND):
                    regAction.append("Aceptar")
                    complete = True
                else:
                    regAction.append(self.findAction(lastItemStack, Alphabet.symbol_STRINGEND, tableAction))
            else:
                #Buscar siguiente accion
                statusLexStr = lexAnString.statusLex()
                auxLexem = lexAnString.yylex()
                regAction.append(self.findAction(lastItemStack, invertDict[auxLexem[0]], tableAction))
                lexAnString.statusLex(statusLexStr)

        return regStack, regString, regAction 

def insertar(tabla,no_terminal, simbolos, num_regla,regla):
    for tupla in tabla:
        if no_terminal == tupla[0]:
            indice1 = tabla.index(tupla)
    indice2 = []
    for terminal in tabla[0]:
        for simbolo in simbolos:
            if terminal == simbolo:
                indice2.append(tabla[0].index(terminal))
    # print(f"Indice de {no_terminal}: {indice1}")
    # print(f"Indices de {simbolos}: {indice2}")
    # cad = "{0},{1}".format(regla,num_regla)
    cad = (regla,num_regla)
    for indice in indice2:
        tabla[indice1][indice] = (cad)


if __name__ == "__main__":
    path = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/GramaticaEj.txt" #Belmont
    pathDict = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/dictFile.txt" #Belmont
    #path = "c:/Users/brian/Documents/CompiladorGUI/GUI/Engine/gram.txt"
    g1 = Grammar(path)
    print("-------ll1--------")
    # termSym.remove(Alphabet().symbol_EPSILON)
    # arrayRegExStr = ["(\()", "(\))", "(\*)", "(\+)", "(a)"]
    anString = "(025*110)"
    lexAnString = LexAnalizer.createLexFile("/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/Examples/lex.txt", anString)
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
    #Analizar Cadena
    reg1, reg2, reg3 = g1.analizeStr(anString, lexAnString, dictTerm)
    print(reg1)
    print()
    print(reg2)
    print()
    print(reg3)
    