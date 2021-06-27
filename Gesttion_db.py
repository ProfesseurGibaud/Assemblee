"""Le programme prend l'open data de l'Assemblée Nationale et le met dans dans la base de données data_full

Usage :
======

1°) Copy/Paste data_save.db et renommer data_save en data_full
2°) Lancer Ouverture_scrutin()
3°) Lancer Ouverture_organe() et Ouverture_elu()


"""

__authors__ = {"Sylvain Gibaud"}
__contact__ = {"mail@professeurgibaud.ovh"}
__date__ = "27/06/2021"


import sqlite3
from lxml import etree
import os

# Variables globale pour mettre dans la base les mandats et les groupes des élus
dico_elu_groupe = {}
dico_elu_mandat = {}

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

def Ouverture_elu(): #Je dois le lancer pour mettre à jour Bd
    global dico_elu_groupe, dico_elu_mandat
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
        profession = root_children[2].getchildren()[0].text
        catSocPro = root_children[2].getchildren()[1].getchildren()[0].text
        famSocPro = root_children[2].getchildren()[1].getchildren()[1].text
        if uid in dico_elu_groupe.keys():
            groupeRef = dico_elu_groupe[uid]
            mandat = dico_elu_mandat[uid]
        else :
            groupeRef = ""
            mandat = ""
        cursor.execute("""INSERT INTO Elu(uid,civ,prenom,nom,dateNais
                        ,profession,catSocPro,famSocPro,groupeRef,mandat)
                        VALUES(?,?,?,?,?,?,?,?,?,?)""",
                        (uid,civ,prenom,nom,date_naissance,profession,
                        catSocPro,famSocPro,groupeRef,mandat))


def Ouverture_Scrutin():
    liste_scrutin = os.listdir("Scrutin")
    for scrutin in liste_scrutin:
        # On prépare le lien fichier.
        LienFichier = os.path.join("Scrutin",scrutin)

        tree = etree.parse(LienFichier)
        root = tree.getroot()
        root_children = root.getchildren()

        uid = root_children[0].text
        organeRef = root_children[2].text
        legislature = int(root_children[3].text)
        sessionRef =  root_children[4].text
        seanceRef = root_children[5].text
        dateScrutin = root_children[6].text
        quantiemeJourSeance = int(root_children[7].text)
        sort = root_children[9].getchildren()[0].text
        titre = root_children[10].text
        demandeur = root_children[11].getchildren()[0].text
        objet = root_children[12].getchildren()[0].text
        synthese_vote_children = root_children[14].getchildren()

        # On récupère les entiers (suffrages, votants etc...)
        nombreVotants = int(synthese_vote_children[0].text)
        suffragesExprimes = int(synthese_vote_children[1].text)
        nbrSuffragesRequis = int(synthese_vote_children[2].text)
        nonVotants = int(synthese_vote_children[4].getchildren()[0].text)
        pour = int(synthese_vote_children[4].getchildren()[1].text)
        contre = int(synthese_vote_children[4].getchildren()[2].text)
        abstentions = int(synthese_vote_children[4].getchildren()[3].text)
        nonVotantsVolontaires = int(synthese_vote_children[4].getchildren()[4].text)

        # On passe aux votes nominatifs
        groupe_votants = root_children[15].getchildren()[0].getchildren()[1].getchildren()  #groupe_votants représentent les groupes politiques

        dico_vote_liste = {"Non Votant" : "", "Pour" : "", "Contre":"","Abstention":""}

        listeUidNonVotants = ""
        listeUidPours = ""
        listeUidContres = ""
        listeUidAbstentions = ""


        for groupe in groupe_votants:
            groupeRef = groupe[0].text
            groupe_vote_nom = groupe[2].getchildren()[2]

            groupe_dico_vote_nom = {"Non Votant" : groupe_vote_nom[0], "Pour" : groupe_vote_nom[1], "Contre" : groupe_vote_nom[2], "Abstention" : groupe_vote_nom[3]}

            for vote,liste in groupe_dico_vote_nom.items():
                print(vote)
                for elu in liste: #Attention elu est un objet, acteurRef est le nom (string)
                    acteurRef = elu.getchildren()[0].text
                    print(acteurRef)
                    mandatRef = elu.getchildren()[1].text
                    if acteurRef not in dico_elu_groupe:
                        dico_elu_groupe[acteurRef] = groupeRef
                    elif not groupeRef in dico_elu_groupe[acteurRef]:
                        dico_elu_groupe[acteurRef] += "/" + groupeRef
                    if elu not in dico_elu_mandat:
                        dico_elu_mandat[acteurRef] = groupeRef
                    elif not groupeRef in dico_elu_mandat[acteurRef]:
                        dico_elu_mandat[acteurRef] += "/" + mandatRef
                    dico_vote_liste[vote] += acteurRef + "/"




        listeUidNonVotants = dico_vote_liste["Non Votant"][:-1]
        listeUidPours = dico_vote_liste["Pour"][:-1]
        listeUidContres = dico_vote_liste["Contre"][:-1]
        listeUidAbstentions = dico_vote_liste["Abstention"][:-1]
        cursor.execute("""INSERT INTO Scrutin
                        (uid,organeRef,legislature,sessionRef,
                        seanceRef,dateScrutin,quantiemeJourSeance,
                        sort,titre,demandeur,objet,nombreVotants,
                        suffragesExprimes,nbrSuffragesRequis,
                        nonVotants,pour,contre,abstentions,
                        nonVotantsVolontaires,
                        listeUidNonVotants,listeUidPours,
                        listeUidContres,listeUidAbstentions)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,
                                ?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (uid,organeRef,legislature,sessionRef,
                        seanceRef,dateScrutin,quantiemeJourSeance,
                        sort,titre,demandeur,objet,nombreVotants,
                        suffragesExprimes,nbrSuffragesRequis,
                        nonVotants,pour,contre,abstentions,
                        nonVotantsVolontaires,
                        listeUidNonVotants,listeUidPours,
                        listeUidContres,listeUidAbstentions))




def Fin():
    conn.commit()
    conn.close()


#LienFichier = os.path.join("Depute","PA267285.xml")

os.system("explorer " + LienFichier)
