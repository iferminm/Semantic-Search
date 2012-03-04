# -*- encoding: utf-8 -*-
# Programmed by: israelord <iferminm at gmail dot com>
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
from translator import Translator

class Querier:
    def __init__(self):
        self.__endpoint = "http://localhost:8890/sparql"
        self.__models = {'thesis': 'thesis:model'}

    def query(self):
        sparql = SPARQLWrapper(self.__endpoint)
        sparql.setQuery("""
            SELECT * FROM <thesis:model> WHERE {?s <http://localhost/ontologies/ThesisOntology.owl#has-annotation> ?o}
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results



if __name__ == '__main__':
    querier = Querier()
    querier.query()
