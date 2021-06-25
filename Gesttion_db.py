import sqlite3
from lxml import etree
import os




conn = sqlite3.connect('data_full.db')




LienFichier = os.path.join("Organe","PO58974.xml")
tree = etree.parse(LienFichier)
root = tree.getroot()
root_children = Root.getchildren()
uid = root_children[0].text
codeType = root_children[1].text
libelle = root_children[2].text
secretariat = root_children[-1].getchildren()[0].text



