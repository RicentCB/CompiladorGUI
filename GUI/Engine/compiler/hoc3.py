from sly import Lexer
from sly import Parser
import math

# CALCULADORA CON VARIABLES
# Se integran las funciones:
#   sin, cos, atan, exp, log, log10, sqrt, int, abs
# Ademas de constantes:
#   PI, E, GAMMA, DEG. PHI

class Hoc3Lexer(Lexer):
    tokens = {NUMBER,NUMBER_F, NAME, 
        SM_EXP,
        SIN, COS, ATAN, EXP, LOG, LOG10, SQRT, ABS,
        PI, N_E, GAMMA, DEG, PHI,
        BRANCH}

    ignore = '\t '
    SM_EXP = r'\^'

    literals = { '+', '-', '/', '*', '(', ')', '='}

    BRANCH = '\n'
    #Palabras Reservadas
    SIN = r'SIN'
    COS = r'COS'
    ATAN = r'ATAN'
    EXP = r'EXP'
    LOG = r'LOG'
    LOG10 = r'LOG10'
    SQRT = r'SQRT'
    ABS = r'ABS'
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
    

class Hoc3Parser(Parser):
    tokens = Hoc3Lexer().tokens

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
    
    @_('listStmt expr')
    def listStmt(self, p):
        self.lines.append(p.expr)
        return p.listStmt

    #CONSTANTES
    @_('PI', 'N_E', 'GAMMA', 'PHI', 'DEG')
    def expr(self, p):
        return p[0]

    # EXPRESIONES
    # Funciones Artimeticas
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
        return ('num', p.NUMBER_F)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)
    
    @_('NAME "=" expr')
    def expr(self, p):
        return ('var_assign', p.NAME, p.expr)

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
    

class Hoc3Execute:

    def __init__(self, parser):
        self.parser = parser
        self.vars = {}
        for line in self.parser.lines:
            result = self.walkTree(line)
            if result is not None and isinstance(result, int):
                print(result)

    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if node is None:
            return None

        if node[0] == 'num':
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
        #Funciones
        if node[0] == "SIN":
            return math.sin(self.walkTree(node[1]))
        # 'SIN "(" expr ")"', 
        # 'COS "(" expr ")"',
        # 'ATAN "(" expr ")"',
        # 'EXP "(" expr ")"',
        # 'LOG "(" expr ")"',
        # 'LOG10 "(" expr ")"',
        # 'SQRT "(" expr ")"',
        # 'ABS
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
    lexer = Hoc3Lexer()
    parser = Hoc3Parser()
    
    fileProgram = open('GUI/Engine/compiler/progs/programHoc3.txt', 'r')
    text = fileProgram.read()
    # print(text)
    lex = lexer.tokenize(text)
    # for token in lex:
    #     print(token)
    parser.parse(lex)
    print()
    for line in parser.lines:
        print(line)

    # hoc2 = Hoc2Execute(parser)
