# -*- encoding: utf-8 -*-
# Programmed by israelord <iferminm at gmail dot com>

import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'AND',
    'OR',
    'REL',
    'NOT',
    'ANNOTATION',
)

# Tokens

t_AND = r'&&'
t_OR = r'\|\|'
t_REL = r'\?rel:'
t_NOT = r'\-'
t_ANNOTATION = r'[a-zA-Z0-9][a-zA-Z0-9\ ]*'


# Ignored characters
t_ignore = " \t\n"
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
def build_lexer():
    lex.lex()

# Parsing rules
precedence = ( )

# Q : QOr | QAnd
#
# QOr : QAnd || QOr | QAnd
#
# QAnd : QAnd && QUnit | QUnit
#
# QUnit : ANNOTATION | REL ANNOTATION | NOT ANNOTATION
#
# a | b & c | d
# 
#  rel:x && y

def p_orquery_or(t):
    'orquery : orquery OR andquery'
    t[0] = (t[2], t[1], t[3])

def p_orquery_and(t):
    'orquery : andquery'
    t[0] = t[1]

def p_andquery_and(t):
    'andquery : andquery AND unitquery'
    t[0] = (t[2], t[1], t[3])

def p_andquery_unit(t):
    'andquery : unitquery'
    t[0] = t[1]

def p_unitquery_annot(t):
    'unitquery : ANNOTATION'
    t[0] = t[1]

def p_unitquery_rel(t):
    'unitquery : REL ANNOTATION'
    t[0] = (t[1], t[2])

def p_unitquery_not(t):
    'unitquery : NOT ANNOTATION'
    t[0] = (t[1], t[2])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

def parse(text):
    build_lexer()
    yacc.yacc()
    return yacc.parse(text)

if __name__ == '__main__':
    while True:
        text = raw_input("text> ")
        print parse(text)
