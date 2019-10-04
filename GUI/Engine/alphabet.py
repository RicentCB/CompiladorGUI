
class Alphabet():
    range_min = 'min'   #a - z
    range_may = 'may'   #A - Z
    range_num = 'num'   #0 - 9
    symbol_MINUS = '-'  #  -
    symbol_INTER = '?'  #  ?
    symbol_PLUS = '+'   #  +    Cerradrua Positiva
    symbol_STAR = '*'   #  *    Cerradura de Kleene
    symbol_OR = '|'     #  |
    symbol_CONC = '&'   #  &
    symbol_PARI = '('   #  (
    symbol_PARD = ')'   #  )

class Token():
    symbol_PLUS = 10    #  +
    symbol_STAR = 20    #  +
    symbol_OR = 30      #  |
    symbol_CONC = 40    #  &
    symbol_PARI = 50    #  (
    symbol_PARD = 60    #  )
    symbol_MINUS = 70   #  -
    symbol_INTER = 80   #  ?
    symbol_ALL = 90
    symbol_RANGE = 100