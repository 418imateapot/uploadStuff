# coding: utf-8

from lxml import html, etree
import httplib
import urlparse
import json

import requests

## l'xpath si riferisce a rivista di statistica
## todo: mettere un case e a seconda che sia dlib, statistica o altro scegliere l'xpath corrispondente
##
def getURLandTitle(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)

	res = []
	for i,a in enumerate(tree.xpath('//div[@class="tocTitle"]//a')):
		res.append({"id": a.attrib.get('href').split('/').pop(-1), "url": a.attrib.get('href'), "title": a.text})

	return res


## in input prende un json con chiavi: url, title, id.
## todo: fare modifiche in modo che funzioni indipendentemente dalla rivista
## adesso e' corretto solo per statistica. in teoria dovrei usare prefisso+id invece dell'url
def createTriples(someJson):
	rivstat = "http://rivista-statistica.unibo.it/article/view/"
	retv = ""
	for obj in someJson:
		retv += "<" + rivstat + obj["id"] + ">" + "\n\ta\tfabio:Work ;\n"
		retv += "\tfabio:hasPortrayal\n\t\t<" + obj["url"] + ".html> ;\n"
		retv += "\tfrbr:realization\n\t\t<" + obj["url"] + "_ver1> .\n\n"
		retv += "<" + obj["url"] + "_ver1>\n\ta\tfabio:Expression ;\n"
		retv += "\tfabio:hasRepresentation\n\t\t<" + obj["url"] + "> .\n\n"
		retv += "<" + obj["url"] + ">\n\ta\tfabio:Item .\n\n"
		retv += "<" + obj["url"] + "_ver1>\n\tdcterms:title \"" + obj["title"] + "\"^^xmls:string .\n\n"
	return retv


# <http://www.dlib.org/dlib/november14/beel/11beel>
# 	a	fabio:Work ;
# 	fabio:hasPortrayal
# 		<http://www.dlib.org/dlib/november14/beel/11beel.html> ;
# 	frbr:realization
# 		<http://www.dlib.org/dlib/november14/beel/11beel_ver1> .

# <http://www.dlib.org/dlib/november14/beel/11beel_ver1>
# 	a	fabio:Expression ;
# 	fabio:hasRepresentation
# 		<http://www.dlib.org/dlib/november14/beel/11beel.html> .

# <http://www.dlib.org/dlib/november14/beel/11beel.html>
# 	a	fabio:Item .

# <http://www.dlib.org/dlib/november14/beel/11beel_ver1>
# 	dcterms:title "The Architecture and Datasets of Docear's Research Paper Recommender System"^^xmls:string .



resJson = getURLandTitle("http://rivista-statistica.unibo.it/issue/view/467?acceptCookies=1")
print createTriples(resJson)
