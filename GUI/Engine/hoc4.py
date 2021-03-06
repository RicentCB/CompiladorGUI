from sly import Lexer
from sly import Parser
import math
import sys

# CALCULADORA CON VARIABLES
# Se integran las funciones:
#   sin, cos, atan, exp, log, log10, sqrt, int, abs
# Ademas de constantes:
#   PI, E, GAMMA, DEG. PHI

class Hoc4Lexer(Lexer):
    tokens = {NUMBER,NUMBER_F, NAME, 
        SM_EXP,
        SIN, COS, ATAN, EXP, LOG, LOG10, SQRT, ABS,
        IF, ELSE, WHILE, SWITCH, CASE, DEFAULT, ENDCASE,
        NE, EQ, GT, GE, LT, LE, OR, AND, NOT,
        PI, N_E, GAMMA, DEG, PHI,
        BRANCH, PRINTEX,
        STRING
        }

    ignore = '\t '
    SM_EXP = r'\^'

    literals = { '+', '-', '/', '*', '(', ')', '=', '{', '}', ':'}

    BRANCH = '\n'

    PRINTEX = r'PRINT'
    #Palabras Reservadas
    SIN = r'SIN'
    COS = r'COS'
    ATAN = r'ATAN'
    EXP = r'EXP'
    LOG10 = r'LOG10'
    LOG = r'LOG'
    SQRT = r'SQRT'
    ABS = r'ABS'
    #Codigo
    IF = r'IF'
    ELSE = r'ELSE'
    WHILE = r'WHILE'
    SWITCH = r'SWITCH'
    ENDCASE = r'break'
    CASE = r'CASE'
    DEFAULT = r'DEFAULT'

    EQ = r'==' 
    NE = r'!='
    GT = r'>' 
    GE = r'>=' 
    LT = r'<' 
    LE = r'<='
    OR = r'OR'
    AND = r'AND'
    NOT = r'NOT'

    STRING = r'\".*?\"'

    # CONSTANTES
    @_(r'PI')
    def PI(self, t):
        t.value = math.pi
        return t
    @_(r'E')
    def N_E(self, t):
        t.value = math.e
        return t
    @_(r'GAMMA')
    def GAMMA(self, t):
        t.value = 0.57721566490153286060
        return t
    @_(r'DEG')
    def DEG(self, t):
        t.value = 57.295777951308232048680
        return t
    @_(r'PHI')
    def PHI(self, t):
        t.value = 0.161803398874989484820
        return t

    # NUMEROS
    @_(r'\d*\.\d+')
    def NUMBER_F(self, t):
        t.value = float(t.value)
        return t
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    #Defincion de Variables
    NAME = r'[a-zA-Z_][a-zA-Z0-9]*'
    

class Hoc4Parser(Parser):
    debugfile = 'Hoc4.out'

    tokens = Hoc4Lexer().tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        ('right', SM_EXP),
        )

    def __init__(self):
        self.lines = list()
    #LIST
    @_('')
    def listStmt(self, p):
        pass

    @_('listStmt BRANCH')
    def listStmt(self, p):
        return p.listStmt
    
    @_('listStmt expr BRANCH')
    def listStmt(self, p):
        self.lines.append(p.expr)
        return p.listStmt
    @_('listStmt statment BRANCH')
    def listStmt(self, p):
        self.lines.append(p.statment)
        return p.listStmt    
    @_('listStmt assign BRANCH')
    def listStmt(self, p):
        self.lines.append(p.assign)
        return p.listStmt    

    # ASIGNACION
    # Funciones Artimeticas
    @_('NAME "=" expr')
    def assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    # STATMENTS
    @_('expr')
    def statment(self, p):
        return p.expr
    @_('assign')
    def statment(self, p):
        return p.assign
    @_('PRINTEX expr')
    def statment(self, p):
        return ('print', p.expr)
    @_('PRINTEX STRING')
    def statment(self, p):
        return ('print', p[1])
    @_('"{" statmentList "}"')
    def statment(self, p):
        return (p.statmentList)  
    #  C  O  D  I  G  O
    #While
    @_('whileCode superCondition statment end')
    def statment(self, p):
        return ('whileCode', p.superCondition, p.statment)
    #If
    @_('ifCode superCondition statment end')
    def statment(self, p):
        return ('ifCode', p.superCondition, p.statment)
    @_('ifCode superCondition statment ELSE statment end')
    def statment(self, p):
        return ('ifCodeElse', p.superCondition, p.statment0, p.statment1)
    #Switch - Case
    @_('switchCode "(" NAME ")" superSwitchList')
    def statment(self, p):
        return ('switchCode', p.NAME, (p.superSwitchList))
    @_('"{" BRANCH switchList "}"')
    def superSwitchList(self,p):
        return (p.switchList)
    @_('switchList caseSwitch')
    def switchList(self, p):
        if p.switchList == None:
            return p.caseSwitch
        else:
            return ('caseList', p.switchList, p.caseSwitch)
    @_('')
    def switchList(self, p):
        pass
    @_('CASE expr ":" BRANCH statmentList ENDCASE BRANCH')
    def caseSwitch(self, p):
        return ('caseSwitch', p.expr, p.statmentList)   
    @_('DEFAULT ":" BRANCH statmentList ENDCASE BRANCH')    
    def caseSwitch(self, p):
        return ('caseDefault', p.statmentList)   

    #REDUCCIONES PALABRAS CLAVE
    @_('WHILE')
    def whileCode(self, p):
        return ("WHILE")
    @_('IF')
    def ifCode(self, p):
        return ("IF")
    @_('SWITCH')
    def switchCode(self, p):
        return ('SWITCH')

    @_('')
    def end(self, p):
        pass
    @_('')
    def statmentList(self, p):
        pass

    @_('statmentList BRANCH')
    def statmentList(self, p):
        return p.statmentList
    @_('statmentList statment')
    def statmentList(self, p):
        if p.statmentList == None:
            return ('stmt', p.statment)
        else:
            return ('stmtList', p.statmentList, ('stmt', p.statment))
        
    #CONSTANTES
    @_('PI', 'N_E', 'GAMMA', 'PHI', 'DEG')
    def expr(self, p):
        return ('numf', p[0])

    # EXPRESIONES
    @_('SIN "(" expr ")"', 
        'COS "(" expr ")"',
        'ATAN "(" expr ")"',
        'EXP "(" expr ")"',
        'LOG "(" expr ")"',
        'LOG10 "(" expr ")"',
        'SQRT "(" expr ")"',
        'ABS "(" expr ")"')
    def expr(self, p):
        return (p[0], p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('NUMBER_F')
    def expr(self, p):
        return ('numf', p.NUMBER_F)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ("neg", p.expr)
    
    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)
        
    @_('expr SM_EXP expr')
    def expr(self, p):
        return ('exp', p.expr0, p.expr1)
    
    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)
    
    #CONDICIONES
    @_('expr GT expr')  # Mayor que
    def condition(self, p):
        return ('gt', p.expr0, p.expr1)
    @_('expr GE expr')  # Mayor o igual
    def condition(self, p):
        return ('ge', p.expr0, p.expr1)
    @_('expr LT expr')  # Menor que
    def condition(self, p):
        return ('lt', p.expr0, p.expr1)
    @_('expr LE expr')  # Menor o igual
    def condition(self, p):
        return ('le', p.expr0, p.expr1)
    @_('expr EQ expr')  # Igual
    def condition(self, p):
        return ('eq', p.expr0, p.expr1)
    @_('expr NE expr')  # No igual
    def condition(self, p):
        return ('ne', p.expr0, p.expr1)
    
    @_('"(" conditionLogical ")"')
    def superCondition(self, p):
        return p.conditionLogical
    
    @_('condition AND condition')  # Logica AND
    def conditionLogical(self, p):
        return ('and', p.condition0, p.condition1)
    @_('condition OR condition')  # Logica OR
    def conditionLogical(self, p):
        return ('or', p.condition0, p.condition1)
    @_('NOT condition')  # Logica NOT
    def conditionLogical(self, p):
        return ('not', p.condition)

    @_('condition')
    def conditionLogical(self, p):
        return p.condition

class Hoc4Execute:

    def __init__(self, parser):
        self.parser = parser
        self.vars = {}
        self.pc = 0
        self.out = ""
        while self.pc < len(self.parser.lines):
            self.walkTree(self.parser.lines[self.pc])
            # if result is not None and (isinstance(result,int) or isinstance(result, float)):
            #     if line[0] == 'var':
            #         print(result)
            self.pc += 1
        
    #funcion que evalua una condicion sea logica o no
    def evaluateCondition(self, condition):
        #Logicas
        if condition[0] == "or":
            return self.evaluateCondition(condition[1]) or self.evaluateCondition(condition[2])
        elif condition[0] == "and":
            return self.evaluateCondition(condition[1]) and self.evaluateCondition(condition[2])
        elif condition[0] == "not":
            return not self.evaluateCondition(condition[1])
        #Comparacion
        else:
            if condition[0] == "gt":
                return self.walkTree(condition[1]) > self.walkTree(condition[2])
            elif condition[0] == "ge":
                return self.walkTree(condition[1]) >= self.walkTree(condition[2])
            elif condition[0] == "lt":
                return self.walkTree(condition[1]) < self.walkTree(condition[2])
            elif condition[0] == "le":
                return self.walkTree(condition[1]) <= self.walkTree(condition[2])
            elif condition[0] == "eq":
                return self.walkTree(condition[1]) == self.walkTree(condition[2])
            elif condition[0] == "ne":
                return self.walkTree(condition[1]) != self.walkTree(condition[2])
    #Funcion que crea un arreglo para evular una condicion Switch
    def createSwitch(self, node):
        arrayAllCases = list()
        if node[0] == 'caseList':
            retCases1 = self.createSwitch(node[1])
            retCases2 = self.createSwitch(node[2])
            arrayAllCases.extend(retCases1)
            arrayAllCases.extend(retCases2)
        elif node[0] == 'caseSwitch':
            #Creamos Caso
            case = self.walkTree(node[1])
            statements = node[2]
            arrayAllCases.append(('case', case, statements))
        else: #node[0] == 'caseDefault'
            statements = node[1]
            arrayAllCases.append(('default', statements))
        return arrayAllCases

        # ('switchCode', 'a', ('caseList', ('caseList', ('caseList', ('caseList', ('caseSwitch', ('num', 1), ('stmt', ('print', '"Caso 1"'))), ('caseSwitch', ('num', 2), ('stmt', ('print', '"Caso 2"')))), ('caseSwitch', ('num', 3), ('stmt', ('print', '"Caso 3"')))), ('caseSwitch', ('num', 4), ('stmt', ('print', '"Caso 4"')))), ('caseDefault', ('stmt', ('print', '"Caso DEFAULT"')))))

    #Funcion que ejecuta, reduce y evalua los nodos creads por el parser
    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if node is None:
            return None

        if node[0] == 'num':
            return node[1]
        elif node[0] == 'numf':
            return node[1]
        elif node[0] == 'neg':   #Empieza con signo negativo
            return -1 * self.walkTree(node[1])
        #Operaciones Aritmeticas
        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'exp':
            return math.pow(self.walkTree(node[1]), self.walkTree(node[2]))
        #Funciones
        if node[0] == 'SIN':
            return round(math.sin(self.walkTree(node[1])), 6)
        elif node[0] == 'COS':
            return round(math.cos(self.walkTree(node[1])), 6)
        elif node[0] == 'ATAN':
            return math.atan(self.walkTree(node[1]))
        elif node[0] == 'EXP':
            return math.exp(self.walkTree(node[1]))
        elif node[0] == 'LOG':
            return math.log(self.walkTree(node[1]))
        elif node[0] == 'LOG10':
            return math.log10(self.walkTree(node[1]))
        elif node[0] == 'SQRT':
            return math.sqrt(self.walkTree(node[1]))
        elif node[0] == 'ABS':
            return math.fabs(self.walkTree(node[1]))
        # PALABRAS RESERVADAS
        if node[0] == 'print':
            if isinstance(node[1], str):
                print(node[1].replace('"',''))
            else:
                print(self.walkTree(node[1]))
            
        # BLOQUES DE CODIGO
        if node[0] == 'ifCode': #Funcion if
            condition = self.evaluateCondition(node[1])
            if condition:
                self.walkTree(node[2])
        elif node[0] == 'ifCodeElse':  #Funcion if
            condition = self.evaluateCondition(node[1])
            if condition:   #Ejectuar pirmer statment
                self.walkTree(node[2])
            else:
                self.walkTree(node[3])
        elif node[0] == 'whileCode':    #Funcion While
            while self.evaluateCondition(node[1]):
                self.walkTree(node[2])

        elif node[0] == 'switchCode':
            #Traer Casos
            casesSw = self.createSwitch(node[2])
            mainVar = 0
            #Tratar de conseguir el valor de la variable
            try:
                mainVar = self.vars[node[1]]
            except LookupError:
                print("La variabla usada en el switch '"+node[1]+"' no se econtro!")
                sys.exit() 
            #Verificar Casos 
            arrayCases = list()
            for node in casesSw:
                if node[0] == 'case':
                    if node[1] not in arrayCases:
                        arrayCases.append(node[1])
                    else:
                        print("Caso ya definido: ",node[1])
                        sys.exit()
                elif node[0] == 'default':
                    if 'default' not in arrayCases:
                        arrayCases.append('default')
                    else:
                        print("Solo puede existe un default")
                        sys.exit()
            #Buscar y ejecutar
            for node in casesSw: 
                if node[0] == 'case':
                    if mainVar == node[1]:  #Variable Igual al caso
                        self.walkTree(node[2])  #Ejecutar codigo
                        break;
                elif node[0] == 'default':
                    self.walkTree(node[1])
                    break;

        # STATMENTS
        elif node[0] == 'stmtList':
            self.walkTree(node[1])
            self.walkTree(node[2])
        elif node[0] == 'stmt':
            return self.walkTree(node[1])
        #Variables
        if node[0] == 'var_assign':
            self.vars[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.vars[node[1]]
            except LookupError:
                print("Variable indefinida '"+node[1]+"' no se econtro!")
                sys.exit()
                return 0

if __name__ == '__main__':
    lexer = Hoc4Lexer()
    parser = Hoc4Parser()
    
    fileProgram = open('Engine/compiler/progs/programHoc5Mod.txt', 'r')
    text = fileProgram.read()
    # print(text)
    lex = lexer.tokenize(text)
    # for token in lex:
    #     print(token)
    parser.parse(lex)
    # print()
    # for line in parser.lines:
    #     print(line)
    # print()
    hoc3 = Hoc4Execute(parser)
