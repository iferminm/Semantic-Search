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
        self.condition_lists = []

    def __get_parsed_tree(self, complete_query):
        """
        Calculates the query's syntactic tree
        according to the grammar defined on the
        parsing module
        """
        return parser.parse(complete_query)
    
    def __proccess_and(self, sub_tree, result):
        if type(sub_tree) == str:
            condition = self.prefixes['thesis'] + 'has-annotation'
            value = self.prefixes['thesis'] + sub_tree
            result.append("?s <%s> <%s>" % (condition, value))
            return result
        else:
            result = self.__proccess_and(sub_tree[1], result)
            result = self.__proccess_and(sub_tree[2], result)
            return result

    def __proccess_tree(self, tree):
        if (tree[0] == "||"):
            self.__proccess_tree(tree[1])
            self.__proccess_tree(tree[2])
        elif (tree[0] == "&&"):
            result = []
            result = self.__proccess_and(tree[1], [])
            result.extend(self.__proccess_and(tree[2], []))
            self.condition_lists.append(result)
        elif (tree[0] == "?rel:"):
            print "rel\n"
        else:
            self.condition_lists.append([tree])

    def main(self, query):
        tree = self.__get_parsed_tree(query)
        self.__proccess_tree(tree)
        for con in self.condition_lists:
            print ' . '.join(con)

if __name__ == '__main__':
    while True:
        t = Translator()
        complete_query = raw_input("query>")
        t.main(complete_query)
