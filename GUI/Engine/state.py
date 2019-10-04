import sys
#Aquí definimos la clase estado, recibe si es
#estado de aceptación y se le asigna un id. El id
#cada que se crea un estado incrementa el id para  
#que no haya dos estados con un mismo id
class State():
    id_state = 0
    #constructor: recibe si es estado de aceptación
    #el valor por defecto es que no es estado de aceptación
    def __init__(self, value=False):
        self.accept = value
        self.id_state = State.id_state
        self.token = -1
        State.id_state = State.id_state+1
    #Sobrecargamos el método de imprimir para poder iprimir el ID del estado
    def __str__(self):
        return str(self.id_state)
    #Sobrecarga del operador "==" para comprar si dos estados son iguales
    def __eq__(self, other):
        return self.id_state == other.id_state
    #Sobrecarga del operador "<" para comparar dos estados
    def __lt__(self, other):
        return self.id_state < other.id_state
    #Retornar si es un estado de aceptacion
    def isAccept(self):
        return self.accept
    #El atributo de aceptacion pasa a ser Falso
    def deleteAccept(self):
        self.accept = False
    #Union de de este mismo estado, con u un conjunto de estados
    def unionSt(self,states2):  #states 2 debe ser un conjunto de estados
        if isinstance(states2, list):
            newStates = [self]
            for state in states2:
                newStates.append(state) #Agregar los nuevos estados
            #Quitar elementos repetidos del arreglo
            outArrayStates = []
            for i in newStates:
                if i not in outArrayStates:
                    outArrayStates.append(i)
            #Regresamos un cojunto de estados sin repetir
            return outArrayStates
        else:
            print("Error en los argumentos")
            sys.exit()

    #Metodo para organizar un conjunto de estados de acuerdo con su ID
    # empieza por el indice mas pequeño, y termina en el mas grande
    def sortStates(arr):
        if len(arr) >1: 
            mid = len(arr)//2 #Finding the mid of the array 
            L = arr[:mid] # Dividing the array elements  
            R = arr[mid:] # into 2 halves 
    
            State.sortStates(L) # Sorting the first half 
            State.sortStates(R) # Sorting the second half 
    
            i = j = k = 0

            # Copy data to temp arrays L[] and R[] 
            while i < len(L) and j < len(R): 
                if L[i] < R[j]: 
                    arr[k] = L[i] 
                    i+=1
                else: 
                    arr[k] = R[j] 
                    j+=1
                k+=1

            # Checking if any element was left 
            while i < len(L): 
                arr[k] = L[i] 
                i+=1
                k+=1

            while j < len(R): 
                arr[k] = R[j] 
                j+=1
                k+=1

    #Metodo para comparar si un arreglo de estados se encuentra
    # en un arreglo de arreglos de estados
    def arrayIsMatrix(arraySts, matrix):
        #Organizamos el arreglo
        State.sortStates(arraySts)
        cont = 0
        for arrayAux in matrix:
            #Organizamos el conjunto de estados de la matriz de estados
            if len(arraySts) == len(arrayAux):
                State.sortStates(arrayAux)
                
                j = 0
                cont = 0
                for state in arraySts:
                    if state == arrayAux[j]:
                        cont = cont + 1
                    j = j + 1

                if cont == len(arraySts):
                    return True
        
        return False

    #Metodo para imprimir un arreglo de estados
    def printArray(array):
        array.sort()
        print("[",end="")
        for elem in array:
            print(elem, end=", ")
        print("]")

#Ejemplo de como instanciar un estado
# edo2 = state(True)
# edo3 = state(False)

# print(edo1.accept)
# print(edo2.accept)
# print(edo3.accept)