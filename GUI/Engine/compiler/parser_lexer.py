from sly import Lexer
from sly import Parser

class Hoc5Lexer(Lexer):
    tokens = { 
        NAME, NUMBER, STRING,
        ENDSTMT, ASSIGN, 
        IF, THEN, ELSE, ENDIF,
        EQ, GT, GE, LT, LE, NE,
        PAR_L, PAR_D, PLUS, MINUS, TIMES, DIVIDE }

    ignore = '\t ' #Ignora Espacios y tabulaciones
    # ignore_newline = r'\n+'

    literals = {'/', '*', ';' }

    # Define tokens
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    # S I M B O L O S
    ENDSTMT = r';'
    ASSIGN = r'='
    PAR_L = r'\('
    PAR_D = r'\)'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    # C O N D I C I O N E S
    EQ = r'=='
    GT = r'>'
    GE = r'>='
    LT = r'<'
    LE = r'<='
    NE = r'!='
    

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class Hoc5Parser(Parser):
    tokens = Hoc5Lexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        )

    def __init__(self):
        self.env = { }
    
    @_('')
    def statement(self, p):
        pass

    @_('expr EQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME ASSIGN STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)
    @_('IF condition THEN statement ENDIF')
    def statement(self, p):
        return ('if_statement', p.condition, ('branch', p.statement0))
    @_('IF condition THEN statement ELSE statement ENDIF')
    def statement(self, p):
        return ('if_statement', p.condition, ('branch', p.statement0, p.statement1))

    # C O N D I T I O N S
    @_('PAR_L expr PAR_D')
    def condition(self, p):
        return ('condition')

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

if __name__ == '__main__':
    lexer = Hoc5Lexer()
    parser = Hoc5Parser()
    fileProgram = open('GUI/Engine/compiler/programEx.txt', 'r')
    # flines = fileProgram.readlines()
    text = fileProgram.read()
    # for line in flines:
    #     text += line
    print(text)
    # while True:
    #     try:
    #         text = input('basic > ')
    #     except EOFError:
    #         break
    #     if text:
    lex = lexer.tokenize(text)
    # for token in lex:
    #     print(token)
    tree = parser.parse(lex)
    print(tree)