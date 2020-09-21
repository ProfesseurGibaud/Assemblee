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