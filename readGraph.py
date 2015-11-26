#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
import os
import shutil
from json import JSONEncoder
from SPARQLWrapper import SPARQLWrapper, JSON

tps_graph = "http://vitali.web.cs.unibo.it/raschietto/graph/ltw1543"

query = """SELECT ?s ?p ?o {
    GRAPH <%s> {?s ?p ?o .}
}""" % (tps_graph)

# NB: Usare 'DELETE' al posto di 'INSERT' per rimuovere
# i dati dal triplestore

sparql = SPARQLWrapper("http://tweb2015.cs.unibo.it:8080/data/query", returnFormat="json")
sparql.setQuery(query)
sparql.setMethod('POST')
q = sparql.query()
print JSONEncoder().encode(q.convert())
