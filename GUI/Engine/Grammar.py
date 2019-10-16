import sys
from alphabet import Alphabet

#Clase Gramtica que construye una tabla LL a partir de un archivo dada una gramatica
class Grammar():

    def __init__(self, path):
        if isinstance(path, str):
            self.file = open(path, "r")
        else:
            sys.exit()
    
    def G(self):
        if self.ListaReglas != None:
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
        #edo = self.getEdo()
        if self.Regla():
            token = self.getToken()
            if token == Token.grammar_PC:
                if self.ListaReglasP():
                    return True
                return False
        #self.setEdo(edo)
        return True 

    def Regla(self):
        token = -1
        if self.LadoIzquierdo():
            token = self.getToken()
            if token == Token.grammar_FLECHA:
                if self.LadosDerechos()
                    return True
        return False

    def LadoIzquierdo(self, s = None):
        token = -1
        token = self.getToken()
        if token == Token.grammar_SIMBOLO:
            s = self.getLexema()    #Se modifica el string recibido como argumento
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
        token = -1
        token = self.getToken()
        if token == Alphabet.grammar_OR:
            if self.ListaSimbolos(): #(N)
                #ArrReglas[IndArrelgo].Simb = s;
                #ArrReglas[IndeArreglo+1].Ap=N
                if self.LadosDerechosP(): #(S)
                    return True
            return False
        self.backTrack()    #Es epsilon
        return True

    def ListaSimbolos(self):
        #Nodo N
        token = -1
        token = self.getToken()
        if token == Token.grammar_SIMBOLO:
            #N = New Nodo(Lexico.getLexema)
            if self.ListaSimbolosP():   #N2
                #N.ApSig = N2
                return True
        return False

    def ListaSimbolosP(self):
        return True
        #Codigo No dado, pero "sencillo", parecido a lista simbolos

    



if __name__ == "__main__":
    path = "/home/ricardo/ESCOM/5 Semestre/Compiladores/CompiladorGUI/GUI/Engine/Gramatica.txt";
    g1 = Grammar(path)
    print(g1.file.read())


            
