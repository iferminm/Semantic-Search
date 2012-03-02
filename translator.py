# -*- encoding: utf-8 -*-
# Programmed by: israelord <iferminm at gmail dot com>

import lex_parser as parser

class Translator:
    
    def __init__(self):
        """
        Initialices my Translator class with
        some important values stored in dictionaries
        """
        self.model_names = {'thesis': 'thesis:model'}
        self.prefixes = {
            'thesis': 'http://localhost/ontologies/ThesisOntology.owl#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl': 'http://www.w3.org/2002/07/owl#',
        }

    def get_parsed_tree(self, complete_query):
        """
        Calculates the query's syntactic tree
        according to the grammar defined on the
        parsing module
        """
        return parser.parse(complete_query)
    
    def proccess_tree(self, tree):
        pass
