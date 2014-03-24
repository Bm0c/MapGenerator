from sfml import Color
from xml.dom import minidom

class Lecteur:

    def __init__(self,nom):
     self.nom = nom
     self.racine = {}

    def _parseStr(self,string):
     if "," in string:
      return [self._parseStr(elt) for elt in string.split(",")]
     elif "int" in string:
      return int(string.split(":")[1])
     elif "#" in string:
      return Color(int(string[1:3],16),int(string[3:5],16),int(string[5:7],16))
     else :
      return string

    def _parseNode(self,node):
     if len(node.childNodes) == 1:
      return self._parseStr(node.firstChild.nodeValue)
     else:
      aux = {}
      l = [ elt for elt in node.childNodes if elt.nodeType == elt.ELEMENT_NODE ]
      for elt in l:
       child = self._parseNode(elt)
       id = ""
       if "id" in elt.attributes:
        id = elt.attributes["id"].value
       if elt.nodeName in aux:
        if id in aux[elt.nodeName]:
         liste = aux[elt.nodeName][id]
        else:
         aux[elt.nodeName][id] = child
         continue
        if type(liste) == type([]):
         liste.append(child)
        else:
         aux[elt.nodeName][id] = [ liste,child ]
       else: 
        aux[elt.nodeName] = { id : child }
      return aux  

    def _clean(self,node):
     if type(node) != type("") and type(node) != type(int) and type(node) != type(Color.BLACK):
      for key,elt in node.items():
       for element in elt.values():
        if type(element) == type([]):
         for e in element:
          self._clean(e)  
        else:
         self._clean(element)
       if len(elt) == 1 and "" in elt:
        node[key] = elt[""]

    def parse(self):
     docxml = minidom.parse(self.nom)
     self.racine = self._parseNode(docxml.firstChild)
     self._clean(self.racine)

a = Lecteur("patron.xml")
a.parse()
