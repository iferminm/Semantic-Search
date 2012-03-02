# -*- encoding: utf-8 -*-
# Programmed by israelord <iferminm at gmail dot com>



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

_fix_lower = ["in", "or", "on", "of"]


def fix_annotation(value):
    """
    This fixes the annotation and puts the
    string in CamelCase form
    """
    tokens = value.split()
    for i in range(0, len(tokens)):
        if not tokens[i].isupper() and not tokens[i] in _fix_lower:
            tokens[i] = tokens[i].capitalize()
    return ''.join(tokens)


def t_ANNOTATION(t):
    r'[a-zA-Z0-9][a-zA-Z0-9\ ]*'
    t.value = fix_annotation(t.value)
    return t

# Ignored characters
t_ignore = " \t\n"
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules
precedence = ( )

# Q : QOr | QAnd
#
# QOr : QAnd || QOr | QAnd
#
# QAnd : QAnd && QUnit | QUnit
#
# QUnit : ANNOTATION | REL ANNOTATION
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

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
yacc.yacc()

def parse(text):
    return yacc.parse(text)

