import sys

from state import State
from alphabet import Alphabet


# Definimos el simbolo estático epsilon
class Epsilon:
    symbol = "Epsilon"
# En la clase transición tendremos que definir el estado 
# hacia donde se va, el estadoinicial, un simbolo minimo 
# y un máximo (si es que es un rango).
# Por default, el simbolo máximo será epsilon, si se desea 
# un rango, se especificará el simbolo máximo cuando 
# se construya la transición
class Transition():
    #Constructor: Recibe Estado ir, estado viene, y los simbolos de la transicion
    
    def __init__(self, state_from, state_to, min_Symbol, max_Symbol = Epsilon.symbol ):
        self.state_from = state_from
        self.state_to = state_to
        #Rangos conocidos
        # if min_Symbol == 'a' and max_Symbol == 'z':
        #     self.min_Symbol = Alphabet.range_min
        #     self.max_Symbol = Alphabet.range_min
        # elif min_Symbol == 'A' and max_Symbol == 'Z':
        #     self.min_Symbol = Alphabet.range_may
        #     self.max_Symbol = Alphabet.range_may
        # elif min_Symbol == '0' and max_Symbol == '9':
        #     self.min_Symbol = Alphabet.range_num
        #     self.max_Symbol = Alphabet.range_num
        # elif max_Symbol == Epsilon.symbol:
        #     self.min_Symbol = min_Symbol
        #     self.max_Symbol = min_Symbol
        # elif min_Symbol != max_Symbol:
        if max_Symbol != Epsilon.symbol:
            if ord(min_Symbol) > ord(max_Symbol):
                print ("El simbolo final debe ser menor al simbolo inicio")
                sys.exit()
        if max_Symbol == Epsilon.symbol:
            self.min_Symbol = min_Symbol
            self.max_Symbol = min_Symbol
        else:
            self.min_Symbol = min_Symbol
            self.max_Symbol = max_Symbol
        
    #Sobrecarga para "convertir a String"
    def __str__(self):
        Out = ""
        Out += str(self.state_from)+" to "+str(self.state_to)+" with "
        if self.min_Symbol != self.max_Symbol:
            Out += "["+self.min_Symbol+" - "+self.max_Symbol+"]"
        elif self.min_Symbol == Alphabet.range_num:
            Out += "[0-9]"
        elif self.min_Symbol == Alphabet.range_min:
            Out += "[a-z]"
        elif self.min_Symbol == Alphabet.range_may:
            Out += "[A-Z]"
        else:
            Out += self.min_Symbol
        return Out

    #Enviar estado Inicial
    def set_state_to(self, state):
        self.state_to = state
    #Enviar estado Final
    def set_state_from(self, state):
        self.state_from = state
    #La transicion cuenta con el simbolo epsilon
    def hasEpsilon(self):
        return self.min_Symbol == Epsilon.symbol
    # La función rango retorna un arreglo con todos
    # los simbolos que pertenecen a la transición
    def range(self):
        if self.max_Symbol == Epsilon.symbol:
            return [self.min_Symbol]
        else: 
            i = ord(self.min_Symbol)
            j = ord(self.max_Symbol)
            if i < j:
                arreglo = []
                for k in range(i,j+1):
                    # print("I:",i)
                    arreglo.append(chr(k))
                return arreglo      
            elif i == j:
                return self.min_Symbol
            else:
                print("Rango de Transcion incorrecto: "+self.min_Symbol+"-"+self.max_Symbol)
                sys.exit() 
    

    # Ejemplo de como instanciar una transición
# edoIni = state()
# edoFin = state(True)
# trans = transition(edoIni,edoFin,'s')
# print(trans.state_to)