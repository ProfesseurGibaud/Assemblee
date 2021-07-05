__authors__ = {"Sylvain Gibaud"}
__contact__ = {"mail@professeurgibaud.ovh"}
__date__ = "27/06/2021"


import sqlite3

import numpy as np
from sklearn.cluster import DBSCAN




conn = sqlite3.connect('data_full.db')
cursor = conn.cursor()

cursor.execute("SELECT uid,suffragesExprimes,pour,contre,abstentions FROM Scrutin")

liste_scrutin = cursor.fetchall()

pre_array_scrutin = [[int(scrutin[0].split("V")[-1]),scrutin[1],scrutin[2],scrutin[3],scrutin[4]] for scrutin in liste_scrutin]

array_scrutin = np.array(pre_array_scrutin)

def distance_renormalise(V1,V2):
    """


    Parameters
    ----------
    V1 : item de array_srutin
        Scrutin 1
    V2 : item de array_scrutin
        Scrutin 2

    Returns
    -------
    d : real number
        Renvoie la distance (normalisé sur le nombre de votants).

    """
    d = abs(V1[2]/V1[1] - V2[2]/V2[1])  \
        + abs(V1[3]/V1[1] - V2[3]/V2[1]) \
        + abs(V1[4]/V1[1] - V2[4]/V2[1])
    return d




def min_max_distance(array_scrutin,distance):
    L = []
    for V1 in array_scrutin:
        for V2 in array_scrutin:
            if V1[0] != V2[0]:
                L.append(distance(V1,V2))
    return min(L),max(L)
mini,maxi = min_max_distance(array_scrutin,distance_renormalise)


dico = {}
taille_class_liste = []
for eps_test in np.linspace(mini + 0.1 ,maxi/2,100):
    for size_test in np.linspace(5,10,5):
        print(eps_test,size_test)
        m = DBSCAN(eps=eps_test, min_samples=size_test,metric = distance_renormalise).fit(array_scrutin)
        labels = m.labels_
        if len(set(labels)) >1:
            temp_list = []
            for label in set(labels):
                temp_list.append(list(labels).count(3))
            taille_classe_plus_petite = min(temp_list)
            print("taille classe plus petite : {}".format(taille_classe_plus_petite))
            taille_class_liste.append(taille_classe_plus_petite)
            dico[eps_test,size_test] = (m,taille_classe_plus_petite)

print(min(taille_class_liste))
print()
