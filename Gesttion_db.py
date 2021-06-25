import sqlite3
from lxml import etree
import os




conn = sqlite3.connect('data_full.db')
cursor = conn.cursor()

def Ouverture_organe():
    liste_organe = os.listdir("Organe")
    for organe in liste_organe:
        LienFichier = os.path.join("Organe",organe)
        tree = etree.parse(LienFichier)
        root = tree.getroot()
        root_children = root.getchildren()
        uid = root_children[0].text
        codeType = root_children[1].text
        libelle = root_children[2].text
        cursor.execute("""INSERT INTO Organe(uid,codeType,libelle) VALUES(?,?,?)""", (uid,codeType,libelle))

def Ouverture_depute(): #Je dois le lancer pour mettre à jour Bd
    liste_depute = os.listdir("Depute")
    print(len(liste_depute))
    for depute in liste_depute:
        print(depute)
        LienFichier = os.path.join("Depute",depute)
        tree = etree.parse(LienFichier)
        root = tree.getroot()
        root_children = root.getchildren()
        uid = root_children[0].text
        etat_civil = root_children[1]
        etat_civil_id = etat_civil.getchildren()[0]
        civ = etat_civil_id.getchildren()[0].text
        prenom = etat_civil_id.getchildren()[1].text
        nom = etat_civil_id.getchildren()[2].text
        date_naissance = etat_civil.getchildren()[1][0].text
        profession = root_children[2].getchildren()[0]
        catSocPro = root_children[2].getchildren()[1].getchildren()[0]
        famSocPro = root_children[2].getchildren()[1].getchildren()[1]
        cursor.execute("""INSERT INTO Depute(uid,civ,prenom,nom,dateNais,profession,catSocPro,famSocPro) VALUES(?,?,?,?,?,?,?,?)""", (uid,civ,prenom,nom,date_naissance,profession,catSocPro,famSocPro))


#Prof = root_children[2].getchildren()


def Fin():
    conn.commit()
    conn.close()





#os.system("explorer " + LienFichier)
