# -*- encoding: utf-8 -*-
# Programmed by: israelord <iferminm at gmail dot com>
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
from translator import Translator

class Querier:
    def __init__(self):
        self.__endpoint = "http://localhost:8890/sparql"
        self.__models = {'thesis': 'thesis:model'}

    def __build_sparql(self, conditions):
        query = "SELECT * FROM <%s> WHERE { %s }" % (self.__models['thesis'], ' . '.join(conditions))
        return query

    def __translate_query(self, simple_query):
        translator = Translator()
        conditions = translator.build_conditions_list(simple_query)
        return conditions

    def query(self, simple_query):
        conditions = self.__translate_query(simple_query)
        results = []
        for con in conditions:
            sparql = SPARQLWrapper(self.__endpoint)
            query = self.__build_sparql(con)
            sparql.setQuery(self.__build_sparql(con))
            sparql.setReturnFormat(JSON)
            result_set = sparql.query().convert()
            results.append(result_set)
        return results
            
if __name__ == '__main__':
    while True:
        simple_query = raw_input('query> ')
        querier = Querier()
        print querier.query(simple_query)
