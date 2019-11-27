from sly import Lexer
from sly import Parser
import math

# CALCULADORA CON VARIABLES
# Se integran las funciones:
#   sin, cos, atan, exp, log, log10, sqrt, int, abs
# Ademas de constantes:
#   PI, E, GAMMA, DEG. PHI

class Hoc4Lexer(Lexer):
    tokens = {NUMBER,NUMBER_F, NAME, 
        SM_EXP,
        SIN, COS, ATAN, EXP, LOG, LOG10, SQRT, ABS,
        IF, ENDIF, ELSE, WHILE, ENDWHILE,
        NE, EQ, GT, GE, LT, LE, OR, AND, NOT,
        PI, N_E, GAMMA, DEG, PHI,
        BRANCH, PRINTEX}

    ignore = '\t '
    SM_EXP = r'\^'

    literals = { '+', '-', '/', '*', '(', ')', '=', '{', '}'}

    BRANCH = '\n'
    PRINTEX = 'PRINT'
    #Palabras Reservadas
    SIN = r'SIN'
    COS = r'COS'
    ATAN = r'ATAN'
    EXP = r'EXP'
    LOG10 = r'LOG10'
    LOG = r'LOG'
    SQRT = r'SQRT'
    ABS = r'ABS'

    IF = r'IF'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    WHILE = r'WHILE'
    ENDWHILE = r'ENDWHILE'

    EQ = r'==' 
    NE = r'!='
    GT = r'>' 
    GE = r'>=' 
    LT = r'<' 
    LE = r'<='
    OR = r'OR'
    AND = r'AND'
    NOT = r'NOT'

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

    @_('whileCode superCondition statment end')
    def statment(self, p):
        return ('whileCode', p.superCondition, ('branch', p.statment))
    @_('ifCode superCondition statment end')
    def statment(self, p):
        return ('ifCode', p.superCondition, ('branch', p.statment))    
    @_('ifCode superCondition statment ELSE statment end')
    def statment(self, p):
        return ('ifCodeElse', p.superCondition, ('branch', p.statment0, p.statment1))
    
    @_('"{" statmentList "}"')
    def statment(self, p):
        return (p.statmentList)    
    @_('WHILE')
    def whileCode(self, p):
        return p.WHILE
    @_('IF')
    def ifCode(self, p):
        return ("IF")
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
            return (p.statment)
        else:
            return (p.statmentList, p.statment)
        

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
    
    # @_('"(" conditionLogical ")"')
    # def superCondition(self, p):
    #     return p.conditionLogical
    
    @_(' "(" condition ")" ')
    def superCondition(self, p):
        return p.condition
    

    # @_('condition AND condition')  # Logica AND
    # def conditionLogical(self, p):
    #     return ('and', p.condition0, p.condition1)
    # @_('condition OR condition')  # Logica OR
    # def conditionLogical(self, p):
    #     return ('or', p.condition0, p.condition1)
    # @_('NOT condition')  # Logica NOT
    # def conditionLogical(self, p):
    #     return ('not', p.condition)

    # @_('condition')
    # def conditionLogical(self, p):
    #     return p.condition

class Hoc4Execute:

    def __init__(self, parser):
        self.parser = parser
        self.vars = {}
        for line in self.parser.lines:
                result = self.walkTree(line)
                if result is not None and (isinstance(result,int) or isinstance(result, float)):
                    if line[0] == 'var':
                        print(result)

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
        #Variables
        if node[0] == 'var_assign':
            self.vars[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.vars[node[1]]
            except LookupError:
                print("Variable indefinida '"+node[1]+"' no se econtro!")
                return 0

if __name__ == '__main__':
    lexer = Hoc4Lexer()
    parser = Hoc4Parser()
    
    fileProgram = open('GUI/Engine/compiler/progs/programHoc4.txt', 'r')
    text = fileProgram.read()
    # print(text)
    lex = lexer.tokenize(text)
    # for token in lex:
    #     print(token)
    parser.parse(lex)
    for line in parser.lines:
        print(line)
    # hoc3 = Hoc4Execute(parser)
