from sly import Lexer
from sly import Parser

# CALCULADORA CON VARIABLES

class Hoc2Lexer(Lexer):
    tokens = {NUMBER, NAME, 
    BRANCH}
    ignore = '\t '

    literals = { '+', '-', '/', '*', '(', ')', '='}

    BRANCH = '\n'
    NAME = r'[a-zA-Z_][a-zA-Z0-9]*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

class Hoc2Parser(Parser):
    tokens = Hoc2Lexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS')
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

    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)

class Hoc2Execute:

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
    lexer = Hoc2Lexer()
    parser = Hoc2Parser()
    
    fileProgram = open('GUI/Engine/compiler/progs/programHoc2.txt', 'r')
    text = fileProgram.read()
    # print(text)
    lex = lexer.tokenize(text)
    parser.parse(lex)
    hoc2 = Hoc2Execute(parser)
