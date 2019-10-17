import sys

from AFD import AFD
from alphabet import Alphabet
from regEx import RegularExp

class LexAnalizer:
    def __init__(self, AFD, string):
        self.AFD = AFD
        self.string = string
        self.apCarActual = 0
    
    #Metodo que funciona como get y set para el apuntador del caracter actual
    def statusLex(self, apCar = None):
        if apCar == None:#Get Status
            return self.apCarActual
        else:   #Set Status
            if isinstance(apCar, int):
                self.apCarActual = apCar
            else:
                print("El argumento debe ser un entero")
                sys.exit()



    #Metodo que escannea la cadena dada como arugmento y 
    # devuelve el token dado por el estado 
    # y el lexema que corresponde a dicha clase lexica
    def yylex(self):    #Retorna el token y el lexema encontrado
        returnToken = []
        lastToken = -1
        #Buscamos los tokens de cada estado
        arrayStatesTokens = []
        for state in self.AFD.all_states:
            for trans in self.AFD.transitions:
                if state == trans[0]:
                    arrayStatesTokens.append([state, trans[len(trans)-1]])
                    break
        #Analizar la cadena dada como constructor del analizar
        actualState = self.AFD.ini_state    #Inciamos con el estado inicial del automata
        stringLex = ""
        foundedLexem = False
        while not foundedLexem:
            newState = self.AFD.transitionFuc(actualState, self.string[self.apCarActual])
            if  newState != -1: #La transicion sigue siendo valida
                #Buscamos el token que corresponde con ese estado
                for elem in arrayStatesTokens:
                    if newState == elem[0]:
                        lastToken = elem[1]
                        stringLex = stringLex +self.string[self.apCarActual]
                        break
                actualState = newState
                #LLegamos al final de la cadena
                if self.apCarActual == len(self.string)-1:
                    returnToken = [lastToken, stringLex]
                    foundedLexem = True
            else: #Hay transicion a un estado muerto
                if lastToken != -1:     #Ctrl -z
                    self.apCarActual = self.apCarActual - 1
                    returnToken = [lastToken, stringLex]  #Caputuramos el ultimo token valido encontrado y el lexema  
                    foundedLexem = True
                else:   #Ultimo token enocntrado no es valido
                    returnToken = [-1]
                    foundedLexem = True
            self.apCarActual = self.apCarActual + 1
        #Retorna el arreglo de token con su lexema
        return returnToken


    def analizeStr(self):
        self.apCarActual = 0
        arrayTokenLexema = []
        #Analizamos la cadena
        while self.apCarActual < len(self.string):
            token = self.yylex()
            if token[0] == -1:
                print("Hay un error en la cadena: '"+self.string+"' en la posicion [",self.apCarActual,"]")
                sys.exit()
            else:
                arrayTokenLexema.append(token)
        
        # return arrayTokenLexema
        print("\nCadena:", self.string,"\n")
        print(arrayTokenLexema)


def main():
    RegExp1 = "(\+|-)&(0-9)+"
    RegExp2 = "(\+|-)&(0-9)+&.&(0-9)+"
    RegExp3 = "L&(L|D)*"
    RegExp4 = "(S|T)+"
    RegExp5 = "(\+)&(\+)"
    RegExp6 = "(\+)"
    arrayTokens = [10,20,30,40,50,60]
    regExp = [RegExp1, RegExp2, RegExp3, RegExp4, RegExp5,RegExp6]
    AFDMain = AFD.createSuperAFD(regExp, [10,20, 30, 40, 50, 60])
    
    stringAn = "SSS+965+TTT+74.96STTSLDLDSSLDDDT+++179SSLDLLL"
    analizador = LexAnalizer(AFDMain, stringAn)
    print(analizador.AFD.printMinimizeTable(['+','-','0-9','.','L','D','T','S']))
    # print(analizador.AFD.printTransitionTable())
    print(analizador.yylex())
    print(analizador.yylex())
    print(analizador.yylex())
    print(analizador.yylex())
    print(analizador.yylex())
    print(analizador.yylex())

    # analizador.analizeStr()


if __name__ == '__main__':
    main()