from lxml import etree
import os
if os.getcwd() != r"C:\Users\Sylgi\Desktop\Site Assemblee":
    os.chdir(r"C:\Users\Sylgi\Desktop\Site Assemblee")


class Depute:
    def __init__(self):
        self.Nom = "Toto"
        self.Prenom = "toto"
        self.acteurRef = "PA0000"
        self.Vote = {} #Vote est un dictionnaire avec en clé le numéro du scrutin et en valeurs : "Non Votant", "Pour", "Contre", "Abstention"
        self.GroupeRef = ""
    def update(self):
        DicoGroupe[self.GroupeRef].ListeActeurRef.append(self) #Cette methode va dans le dossier acteur et met à jour les coordonnées du député.
        tempTreeDepute = etree.parse("Depute/"+ self.acteurRef + ".xml")
        tempRootDepute = tempTreeDepute.getroot()
        tempEtatCivil = tempRootDepute.getchildren()[1]
        tempIdentite = tempEtatCivil.getchildren()[0]
        self.Nom = tempIdentite.getchildren()[2].text
        self.Prenom = tempIdentite.getchildren()[1].text

ListeDepute = []

class Groupe:
    def __init__(self):
        self.Nom = "Groupe"
        self.Abrege = "Gpe"
        self.PositionPol = "Majoritaire"
        self.GroupeRef = "PO730964" #c'est l'uid dans le xml
        self.ListeActeurRef = []
        self.tempTreeGroup = ""
        self.tempRootGroup = ""
    def update(self):#Fonction qui va chercher dans organisme les informations en utilisant le GroupeRef
        try:
            self.tempTreeGroup = etree.parse("Organe/" + self.GroupeRef + ".xml")
            #print("Organe/" + self.GroupeRef + ".xml")
            self.tempRootGroup = self.tempTreeGroup.getroot()
            #print(self.tempRootGroup.getchildren()[2].text)
            self.Nom = self.tempRootGroup.getchildren()[2].text
            #print(self.Nom)
            self.Abrege = self.tempRootGroup.getchildren()[4].text
            self.PositionPol = self.tempRootGroup.getchildren()[-3].text #Ouvrir "Depute/" + self.GroupeRef
        except:
            print("Groupe " + self.GroupeRef + " pas dans la liste des organes")
    def MajListeActeurRef(self):
        for depute in Liste:
            if depute.GroupeRef == self.GroupeRef:
                self.ListeActeurRef.append(depute.acteurRef)


"""

D'abord on fait la liste des députés (anciens et nouveau). (on fait la durée des mandats plus tard).
Puis on réalise une boucle sur les votes pour attribuer les scrutins aux députés.


Dans un deuxième temps on classera les scrutins en type différents et on cherchera un indicateur (pour savoir à quel point ils sont clivants).

"""

class Scrutin:
    def __init__(self):
        self.uid = ""
        self.date = ""
        self.titre = "Vote de Blabla"
        self.nombreVotants = 0
        self.nombrePours = 0
        self.nombreContres = 0
        self.NonVotants = 0
        self.abstentions = 0
        self.NonVotantsVolontaires =0

DicoGroupe = {} #La clé du dico est le groupe ref la valeur est un objet Groupe

DicoDepute = {} #La clé du dico est le ActeurRef, la valeur est un objet député.

DicoScrutin = {}

def ExploVote(LienVote):
    global DicoGroupe, DicoDepute, DicoScrutin # Il faut Stocker les informations du Scrutin

    tree = etree.parse(LienVote)
    Root = tree.getroot()
    tempScrutin = Scrutin()
    tempScrutin.uid = Root.getchildren()[0].text
    tempScrutin.date = Root.getchildren()[6].text
    tempScrutin.titre  = Root.getchildren()[10].text
    Children1 = Root.getchildren()
    VentilationVote = Children1[-2]
    OrganeScrutin = VentilationVote.getchildren()[0]
    Groupes = OrganeScrutin.getchildren()[1]
    for groupe in Groupes:
        GroupeRef = groupe.getchildren()[0].text
        if GroupeRef not in DicoGroupe:
            tempGroupe = Groupe()
            tempGroupe.GroupeRef = GroupeRef
            #print(tempGroupe.GroupeRef)
            tempGroupe.update()
            #print(tempGroupe.Nom)
            DicoGroupe[GroupeRef] = tempGroupe
        VoteGroupe = groupe.getchildren()[2]
        VoteGroupeDecompte = VoteGroupe.getchildren()[2]
        VVote = {"Non Votant":[],"Pour":[],"Contre":[]} #On met que les noeux dans VVote
        for nonvotant in VoteGroupeDecompte.getchildren()[0]:
            VVote["Non Votant"].append(nonvotant)
        for votantpour in VoteGroupeDecompte.getchildren()[1]:
            VVote["Pour"].append(votantpour)
        for votantcontre in VoteGroupeDecompte.getchildren()[2]:
            VVote["Contre"].append(votantcontre)
        for bulletin in VVote:
            for votant in VVote[bulletin]:
                ActeurRef = votant.getchildren()[0].text
                if ActeurRef not in DicoDepute:
                    tempDepute = Depute()
                    tempDepute.acteurRef = ActeurRef
                    tempDepute.GroupeRef = GroupeRef
                    tempDepute.update()
                    DicoDepute[ActeurRef] = tempDepute
                DicoDepute[ActeurRef].Vote[tempScrutin.uid] = bulletin


def Explo():
    ListeScrutins = os.listdir("Scrutins")
    for LienVote in ListeScrutins:
        print(LienVote)
        ExploVote("Scrutins/" + LienVote)


"""
tempTreeGroup = etree.parse("Organe/PO730964.xml")
RootGroup = tempTreeGroup.getroot()
Nom = RootGroup.getchildren()[2].text
Abrege = RootGroup.getchildren()[4].text
PosPol = RootGroup.getchildren()[-3].text
"""







"""
Archive Lancement



tree = etree.parse("VTANR5L15V1.xml")
Root = tree.getroot()
tempScrutin = Scrutin()
tempScrutin.uid = Root.getchildren()[0].text
tempScrutin.date = Root.getchildren()[6].text
tempScrutin.titre  = Root.getchildren()[10].text
Children1 = Root.getchildren()
VentilationVote = Children1[-2]
OrganeScrutin = VentilationVote.getchildren()[0]
Groupes = OrganeScrutin.getchildren()[1]



for groupe in Groupes:
    GroupeRef = groupe.getchildren()[0].text
    if GroupeRef not in DicoGroupe:
        tempGroupe = Groupe()
        tempGroupe.GroupeRef = GroupeRef
        #print(tempGroupe.GroupeRef)
        tempGroupe.update()
        #print(tempGroupe.Nom)
        DicoGroupe[GroupeRef] = tempGroupe
    VoteGroupe = groupe.getchildren()[2]
    VoteGroupeDecompte = VoteGroupe.getchildren()[2]
    VVote = {"Non Votant":[],"Pour":[],"Contre":[]} #On met que les noeux dans VVote
    for nonvotant in VoteGroupeDecompte.getchildren()[0]:
        VVote["Non Votant"].append(nonvotant)
    for votantpour in VoteGroupeDecompte.getchildren()[1]:
        VVote["Pour"].append(votantpour)
    for votantcontre in VoteGroupeDecompte.getchildren()[2]:
        VVote["Contre"].append(votantcontre)
    for bulletin in VVote:
        for votant in VVote[bulletin]:
            ActeurRef = votant.getchildren()[0].text
            if ActeurRef not in DicoDepute:
                tempDepute = Depute()
                tempDepute.acteurRef = ActeurRef
                tempDepute.GroupeRef = GroupeRef
                tempDepute.update()
                DicoDepute[ActeurRef] = tempDepute
            DicoDepute[ActeurRef].Vote[tempScrutin.uid] = bulletin



"""



"""
Archive






#Maintenant il faut aller chercher dans tous les groupes les députés et les votants.

groupe1 = Groupes[0]
GroupeRef = groupe1.getchildren()[0].text
VoteGroupe1 = groupe1.getchildren()[2]
VoteGroupe1Decompte = VoteGroupe1.getchildren()[2]
VoteGroupe1NonVotants  = VoteGroupe1Decompte.getchildren()[0]
VoteGroupe1Pour = VoteGroupe1Decompte.getchildren()[1]
VoteGroupe1Contre = VoteGroupe1Decompte.getchildren()[2]
VotantPour = VoteGroupe1Pour.getchildren()[0]
VotantPourActeurRef = VotantPour.getchildren()[0]
VotantPourParDeleg = VotantPour.getchildren()[2]


tempTreeDepute = etree.parse("Depute/PA335612.xml")
tempRootDepute = tempTreeDepute.getroot()
tempEtatCivil = tempRootDepute.getchildren()[1]
tempIdentite = tempEtatCivil.getchildren()[0]
Nom = tempIdentite.getchildren()[2].text
Prenom = tempIdentite.getchildren()[1].text

"""