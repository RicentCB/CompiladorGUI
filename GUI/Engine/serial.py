import pickle

# data = []

file_name = "/home/ricardo/ESCOM/5Semestre/Compiladores/CompiladorGUI/GUI/Engine/AFNS.txt"
# fileObject = open(file_name, 'wb')

#Escribir el objeto
# pickle.dump(data,fileObject)
# fileObject.close()

#Leer El mensaje
fileObjectRead = open(file_name, 'rb')
read = pickle.load(fileObjectRead) 
if len(read) > 0:
    for elem in read:
        print(elem)

