from sly import Lexer
from sly import Parser

class Hoc1Lexer(Lexer):
    tokens = {NUMBER, BRANCH}
    ignore = '\t '

    literals = { '+', '-', '/', '*', '(', ')'}

    BRANCH = '\n'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

class Hoc1Parser(Parser):
    tokens = Hoc1Lexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
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
    
    #EXPR
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
    
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

    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)

class Hoc1Execute:

    def __init__(self, parser):
        self.parser = parser
        

if __name__ == '__main__':
    lexer = Hoc1Lexer()
    parser = Hoc1Parser()
    
    fileProgram = open('GUI/Engine/compiler/programHoc1.txt', 'r')
    text = fileProgram.read()
    print(text)
    lex = lexer.tokenize(text)
    tree = parser.parse(lex)
    for line in parser.lines:
        print(line)

    # print(parser.lines)