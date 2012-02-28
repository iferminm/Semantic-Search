# -*- encoding: utf-8 -*-
from query_classes import * 

tokens = (
    'AND',
    'OR',
    'REL',
    'ANNOTATION',
)

# Tokens

t_AND         = r'&&'
t_OR          = r'\|\|'
t_REL         = r'\?rel:'

# A rule to remove the white spaces from ANNOTATION tokens
def t_ANNOTATION(t):
    r'[a-zA-Z0-9][a-zA-Z0-9\ ]*'
    t.value = t.value.replace(' ', '')
    return t

# Ignored characters
t_ignore = " \t\n"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Testing my lexer
data = """
hola || chao && tuma tupa
"""

lexer.input(data)
print data
for tok in lexer:
    print tok.type, tok.value, tok.lexpos
"""
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

def print_t(t):
    for x in t:
        print x

def p_andquery_and(t):
    'andquery : andquery AND orquery'
#    print 'AND:', t[1], ' and ', t[3]
#    t[0] = AndQuery(t[1], t[3])
    print "AND: "
    print_t(t)

def p_andquery_or(t):
    'andquery : orquery'
#    print 'AND:', t[1]
#    t[0] = t[1]
    print "AND_OR: ", len(t)
    print_t(t)

def p_orquery_or(t):
    'orquery : orquery OR unitquery'
#    print 'OR:', t[1], ' or ', t[3]
#    t[0] = OrQuery(t[1], t[3])
    print "OR: ", len(t)
    print_t(t)

def p_orquery_unit(t):
    'orquery : unitquery'
#    print 'OR:', t[1]
    print "OR_UNIT: ", len(t)
    print_t(t)
    
def p_unitquery_annot(t):
    'unitquery : ANNOTATION'
#    print 'ANNOT: ', t[1]
#    t[0] = AnnotationQuery(t[1].replace(' ', ''))
    print "UNIT_ANNOT: ", len(t)
    print_t(t)

def p_unitquery_rel(t):
    'unitquery : REL ANNOTATION'
#    print 'ANNOT: rel:', t[2]
#    t[0] = RelatedQuery(t[2].replace(' ', ''))
    print "REL: ", len(t)
    print_t(t)

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
"""
