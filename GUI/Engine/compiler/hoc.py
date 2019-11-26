from sly import Lexer
from sly import Parser

#=========================================================
# --------- A N A L I Z A D O R    L E X I C O ---------
#=========================================================
class HocLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, NAME, ALL,
        PLUS, MINUS, TIMES, SDIVIDE, SPOW, 
        ASSIGN, EQUAL, LEQ, LT, GEQ, GT,
        WHILE, IF, THEN, ELSE,
        FOR, TO }


    literals = { '(', ')', '{', '}', ';'}   #Se ecriben entre "" en el parser

    # String containing ignored characters
    ignore = ' \t'
    #Palabras Reservadas
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    WHILE = r'WHILE'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    FOR = r'FOR'
    TO = r'TO'
    #Simbolos
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    SDIVIDE = r'/'
    SPOW  = r'PW'
    EQUAL = r'=='
    LEQ   = r'<='
    LT    = r'<'
    GEQ   = r'>='
    GT    = r'>'
    ASSIGN = r'='

    ALL = r'\".*?\"'

    ignore_comment = r'//.*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Salto de Linea
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Linea %d: Caracter erroneo %r' % (self.lineno, t.value[0]))
        self.index += 1
#=========================================================
# ---------          P A R S E R         ---------
#=========================================================
class HocParser(Parser):
    tokens = HocLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, SDIVIDE),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self.env = {}
    # ------- DEFINIMOS LAS REGLAS GRAMATICALAES -------
    @_('')
    def statment(self, p):
        pass
    @_('IF condition THEN statment ELSE statment ')
    def statment(self, p):
        return ('if_statment', p.condition, ('branch', p.statment0, p.statment1))
    @_('var_assign')
    def statment(self, p):
        return p.var_assign
    @_('NAME ASIGN expr')
    def var_assign(self, p):
        return('var_assign', p.NAME, p.expr)        
    @_('NAME ASIGN ALL')
    def var_assign(self, p):
        return('var_assign', p.NAME, p.ALL)
    # EXPRESIONES
    @_('expr')
    def statment(self, p):
        return (ṕ.expr)
    @_('expr PLUS expr')
    def statment(self, p):
        return ('add', p.expr0, p.expr1)
    @_('expr MINUS expr')
    def statment(self, p):
        return ('sub', p.expr0, p.expr1)
    @_('expr TIMES expr')
    def statment(self, p):
        return ('mul', p.expr0, p.expr1)
    @_('expr SDIVIDE expr')
    def statment(self, p):
        return ('div', p.expr0, p.expr1)
    # CONDICIONES
    @_('expr EQUAL expr')
    def condition(self, p):
        return('condition_equal', p.expr0, p.expr1)
    # TERMINALES
    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)
    @_('NUMBER')
    def expr(self, p):
        return('num', p.NUMBER)
#=========================================================
# ---------        I N T E R P R E T E R       ---------
#=========================================================
class HocExecute():
    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '""':
            print(result)

    def walkTree(self, node):
        if isinstance(node, int) or isinstance(node, str) or node is None:
            return node
        if node[0] == 'program': 
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])
        
        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

    
if __name__ == '__main__':

    data = '''
        // Counting
        x = 0;
        IF (x<10) {
            print x
            x = xPW1;
        }
        '''

    lexer = HocLexer()
    parser = HocParser()
    env {}
    tree = parser.parse(lexer.tokenize(text))