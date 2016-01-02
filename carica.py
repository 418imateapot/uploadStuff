# coding: utf-8

from lxml import html, etree
import httplib
import urlparse
import json

import requests

# dato un URL di un'issue di dlib o statistica crea un json con titoli e URL degli articoli di quel numero
def getURLandTitle(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)

	res = []
	if "dlib" in url:
		pref = url.rsplit("/", 1).pop(0) + "/" # ad esempio http://www.dlib.org/dlib/november14/	
		for i,a in enumerate(tree.xpath("(//p[@class='contents']/a)[position()<last()]")): ### dlib nov14
			res.append({"url": pref + a.attrib.get('href'), "title": a.text})
	else: # significa che e' rivista di statistica 
		for i,a in enumerate(tree.xpath('//div[@class="tocTitle"]//a')):
			res.append({"url": a.attrib.get('href'), "title": a.text})
	return res


## in input prende un json con chiavi: url e title.
def createTriples(someJson):
	retv = ""
	for obj in someJson:
		print "current object: " + str(obj)
		objPref = obj["url"] if "statistica" in obj["url"] else obj["url"].rsplit(".", 1).pop(0)
		#print "cur obj has prefix" + objPref
		#print "\n"

		retv += "<" + objPref + ">" + "\n\ta\tfabio:Work ;\n"
		retv += "\tfabio:hasPortrayal\n\t\t<" + objPref + ".html> ;\n"
		retv += "\tfrbr:realization\n\t\t<" + objPref + "_ver1> .\n\n"
		retv += "<" + objPref + "_ver1>\n\ta\tfabio:Expression ;\n"
		retv += "\tfabio:hasRepresentation\n\t\t<" + objPref + ".html> .\n\n"
		retv += "<" + objPref + ".html>\n\ta\tfabio:Item .\n\n"
		retv += "<" + objPref + "_ver1>\n\tdcterms:title \"" + obj["title"] + "\"^^xmls:string .\n\n"
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

print createTriples(getURLandTitle("http://rivista-statistica.unibo.it/issue/view/467?acceptCookies=1")).encode('utf-8')
#print "\n\n\n\naaaaaaaaa\n\n"
print createTriples(getURLandTitle("http://www.dlib.org/dlib/november14/11contents.html")).encode('utf-8')

print createTriples(getURLandTitle("http://rivista-statistica.unibo.it/issue/view/514")).encode('utf-8')
