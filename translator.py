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
        self.__condition_lists = []

    def __get_parsed_tree(self, complete_query):
        """
        Calculates the query's syntactic tree
        according to the grammar defined on the
        parsing module
        """
        return parser.parse(complete_query)

    def __process_rel(self, annot):
        print "RELATED QUERIES FOR: ", annot


    def __proccess_and(self, sub_tree, result):
        """
        Goes throught an AND sub-tree and returns
        a list with all the SPARQL conditions 
        built from the tree's sleves
        """
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
        """
        Goes throught the tree and separates the OR
        operators to be processed as separate queries
        """
        if (tree[0] == "||"):
            self.__proccess_tree(tree[1])
            self.__proccess_tree(tree[2])
        elif (tree[0] == "&&"):
            result = []
            result = self.__proccess_and(tree[1], [])
            result.extend(self.__proccess_and(tree[2], []))
            self.__condition_lists.append(result)
        elif (tree[0] == "?rel:"):
            self.__process_rel(tree[1])
        else:
            condition = self.prefixes['thesis'] + 'has-annotation'
            value = self.prefixes['thesis'] + tree
            self.__condition_lists.append(["?s <%s> <%s>" % (condition, value)])

    def build_conditions_list(self, query):
        """
        takes a query on the very simple query language
        and returns a list of SPARQL conditions for several
        SPARQL Queries
        """
        tree = self.__get_parsed_tree(query)
        self.__proccess_tree(tree)
        for con in self.__condition_lists:
            print ' . '.join(con)

        return self.__condition_lists

if __name__ == '__main__':
    while True:
        t = Translator()
        complete_query = raw_input("query> ")
        print t.build_conditions_list(complete_query)

