tokens = (
    'AND','OR',
    'REL','ANNOTATION',
    )

# Tokens

t_AND         = r'&&'
t_OR          = r'\|\|'
t_REL         = r'\?rel:'
t_ANNOTATION  = r'[a-zA-Z0-9][a-zA-Z0-9\ ]*'

#def t_NUMBER(t):
#    r'\d+'
#    try:
#        t.value = int(t.value)
#    except ValueError:
#        print("Integer value too large %d", t.value)
#        t.value = 0
#    return t

# Ignored characters
t_ignore = " \t\n"

#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules
precedence = ( )

# Q : QAnd | QOr
#
# QAnd : QAnd && QAnd | QOr 
#
# QOr : QOr || QUnit | QUnit
#
# QUnit : ANNOTATION | REL ANNOTATION
#
# a | b & c | d
# 
#  rel:x && y

def p_andquery_and(t):
    'andquery : andquery AND orquery'
    print 'AND:', t[1], ' and ', t[3]
    t[0] = AndQuery(t[1], t[3])
	
def p_andquery_or(t):
    'andquery : orquery'
    print 'AND:', t[1]
    t[0] = t[1]

def p_orquery_or(t):
    'orquery : orquery OR unitquery'
    print 'OR:', t[1], ' or ', t[3]
    t[0] = OrQuery(t[1], t[3])

def p_orquery_unit(t):
    'orquery : unitquery'
    print 'OR:', t[1]
    t[0] = t[1]
    
def p_unitquery_annot(t):
    'unitquery : ANNOTATION'
    print 'ANNOT: ', t[1]
    t[0] = AnnotationQuery(t[1].replace(' ', ''))

def p_unitquery_rel(t):
    'unitquery : REL ANNOTATION'
    print 'ANNOT: rel:', t[2]
    t[0] = RelatedQuery(t[2].replace(' ', ''))

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    yacc.parse(s)