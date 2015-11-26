#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
import os
import shutil
from SPARQLWrapper import SPARQLWrapper, JSON

g = rdflib.Graph()
g.parse("teapotGraph.ttl", format="turtle")
tps_graph = "http://vitali.web.cs.unibo.it/raschietto/graph/ltw1543"

query = """INSERT DATA {
    GRAPH <%s> { %s }
}""" % (tps_graph, g.serialize(format="nt"))

# NB: Usare 'DELETE' al posto di 'INSERT' per rimuovere
# i dati dal triplestore

sparql = SPARQLWrapper("http://tweb2015.cs.unibo.it:8080/data/update")
sparql.setQuery(query)
sparql.setMethod('POST')
q = sparql.query()
