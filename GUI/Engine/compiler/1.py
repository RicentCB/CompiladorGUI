from sly import Lexer
from sly import Parser

#=========================================================
# --------- A N A L I Z A D O R    L E X I C O ---------
#=========================================================
class BasicLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, NAME, ALL,
        PLUS, MINUS, ASSIGN, EQUAL,
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
    FOR = r'FOR'
    TO = r'TO'
    #Simbolos
    PLUS = r'\+'
    MINUS = r'\-'
    EQUAL = r'=='
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
# class BasicParser(Parser):
    
if __name__ == '__main__':

    data = '''
        // Counting
        x = 0;
        while (x < 10) {
            print x:
            x = x + 1;
        }
        '''

    lexer = BasicLexer()
    for tok in lexer.tokenize(data):
        print(tok)