# -*- encoding: utf-8 -*-
# Programmed by: israelord <iferminm at gmail dot com>
from mako.template import Template
from mako.lookup import TemplateLookup
from querier import Querier
import cherrypy
from itertools import chain
import os

lookup = TemplateLookup(directories=['html'])

class Searcher:
    def serve_template(self, template_name, **kwargs):
        """
        Serves any existing template by name
        """
        template = lookup.get_template(template_name)
        return template.render(**kwargs)

    def unpack_results(self, results):
        return list(chain(*results))

    @cherrypy.expose
    def do_query(self, query):
        """
        Renders the results page
        """
        q = Querier()
        results = None
        try:
            # extracts only the bindings from the result dictionary
            bindings = [r['results']['bindings'] for r in q.query(str(query)) if r['results']['bindings'] != []]
            results = self.unpack_results(bindings)
        except:
            # in case of any exception should render an error page
            results = "ERROR"
        return self.serve_template('results.txt', results=results)

    @cherrypy.expose
    def index(self):
        """
        Renders the main search page
        """
        return self.serve_template('index.txt')

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 2112})
    cherrypy.quickstart(Searcher(), '/', 'searcher.cfg')
