# -*- encoding: utf-8 -*-
# Programmed by: israelord <iferminm at gmail dot com>
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON 
import lex_parser as parser
class Translator:
    """
    This class translates the simple queries to
    SPARQL queries
    """
    def __init__(self):
        """
        Initialices my Translator class with
        some important values stored in dictionaries
        """
        self.model_names = {'thesis': 'thesis:model'}
        self.__endpoint = "http://localhost:8890/sparql"
        self.prefixes = {
            'thesis': 'http://localhost/ontologies/ThesisOntology.owl#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
        }
        self.__fix_lower = ["in", "or", "on", "of"]
        self.condition_lists = []

    def __execute_helper_query(self, variables, conditions):
        query = "SELECT %s FROM <%s> WHERE { %s  }" % (variables, self.model_names['thesis'], conditions)
        sparql = SPARQLWrapper(self.__endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings']

    def __get_parsed_tree(self, complete_query):
        """
        Calculates the query's syntactic tree
        according to the grammar defined on the
        parsing module
        """
        return parser.parse(complete_query)

    def __get_annot_properties(self, annot):
        value = self.prefixes['thesis'] + annot
        type_relation = self.prefixes['rdf'] + 'type'
        domain_relation = self.prefixes['rdfs'] + 'domain'
        rel_conditions = "<%s> <%s> ?type . ?prop <%s> ?type " % (value, type_relation.strip(), domain_relation.strip())
        rel_conditions +=  "FILTER regex(?type, '%s') FILTER regex(?prop, '%s')" % (self.prefixes['thesis'], self.prefixes['thesis']) 
        properties = self.__execute_helper_query('?prop', rel_conditions)
        return properties

    def __get_rel_annotations(self, annot, properties):
        pre_result = []
        for p in properties:
            subject = self.prefixes['thesis'] + annot
            condition = "<%s> <%s> ?class" % (subject.strip(), p.strip())
            pre_result.append(self.__execute_helper_query('?class', condition))
       
        result = []
        for res in pre_result:
            annots = [a['class']['value'] for a in res]
            result.extend([a.split('#')[len(a.split('#')) - 1] for a in annots])

        return result
       

    def __process_rel(self, annot):
        result = []
        annot = self.__fix_annotation(annot)
        properties = self.__get_annot_properties(annot)
        prop_values = [p['prop']['value'] for p in properties]
        annots = self.__get_rel_annotations(annot, prop_values)
        simple_query = ' || '.join(annots)
        tree = self.__get_parsed_tree(simple_query)
        self.__process_tree(tree, fix=False)

    def __process_and(self, sub_tree, result, fix=True):
        """
        Goes throught an AND sub-tree and returns
        a list with all the SPARQL conditions 
        built from the tree's sleves
        """
        if type(sub_tree) == str:
            if fix:
                sub_tree = self.__fix_annotation(sub_tree)
            condition = self.prefixes['thesis'] + 'has-annotation'
            value = self.prefixes['thesis'] + sub_tree
            result.append("?s <%s> <%s>" % (condition.strip(), value.strip()))
            return result
        elif (sub_tree[0] == '-'):
            result.append(self.__process_not(sub_tree[1]))
            return result
        else:
            result = self.__process_and(sub_tree[1], result)
            result = self.__process_and(sub_tree[2], result)
            return result

    def __process_not(self, annot, fix=True):
        """
        Processes the not operator and translate it's semaintic
        to a SPARQL filter
        """
        if fix:
            annot = self.__fix_annotation(annot)
        condition = self.prefixes['thesis'] + 'has-annotation'
        value = self.prefixes['thesis'] + annot
        result = "FILTER NOT EXISTS { ?s <%s> <%s> }" % (condition.strip(), value.strip())
        return result

    def __fix_annotation(self, value):
        """
        This fixes the annotation and puts the
        string in CamelCase form
        """
        tokens = value.split()
        for i in range(0, len(tokens)):
            if not tokens[i].isupper() and not tokens[i] in self.__fix_lower:
                tokens[i] = tokens[i].capitalize()
        return ''.join(tokens)

    def __process_tree(self, tree, fix=True):
        """
        Goes throught the tree and separates the OR
        operators to be processed as separate queries
        """
        if type(tree) == str and fix:
            tree = self.__fix_annotation(tree)
        if (tree[0] == "||"):
            self.__process_tree(tree[1], fix=fix)
            self.__process_tree(tree[2], fix=fix)
        elif (tree[0] == "&&"):
            result = []
            result = self.__process_and(tree[1], [], fix=fix)
            result.extend(self.__process_and(tree[2], []))
            self.condition_lists.append(result)
        elif (tree[0] == '-'):
            result = self.__process_not(tree[1], fix=fix)
            self.condition_lists.append([result])
        elif (tree[0] == "?rel:"):
            self.__process_rel(tree[1])
        else:
            condition = self.prefixes['thesis'] + 'has-annotation'
            value = self.prefixes['thesis'] + tree
            self.condition_lists.append(["?s <%s> <%s>" % (condition.strip(), value.strip())])

    def build_conditions_list(self, query):
        """
        takes a query on the very simple query language
        and returns a list of SPARQL conditions for several
        SPARQL Queries
        """
        tree = self.__get_parsed_tree(query)
        self.__process_tree(tree)
        return self.condition_lists

if __name__ == '__main__':
    while True:
        t = Translator()
        complete_query = raw_input("query> ")
        print t.build_conditions_list(complete_query)
