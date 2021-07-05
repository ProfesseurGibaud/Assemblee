__authors__ = {"Sylvain Gibaud"}
__contact__ = {"mail@professeurgibaud.ovh"}
__date__ = "27/06/2021"


import sqlite3

import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets

iris = datasets.load_iris()
targets = iris.target
colors = ["red","blue","green"]
labels = ["C1","C2","C3"]

kmeans = KMeans(n_clusters = 3)
dbscan  = DBSCAN(eps=0.7, min_samples=5)
dbscan.fit(iris.data)
kmeans.fit(iris.data)
y_kmeans = kmeans.predict(iris.data)




for target in targets:
    plt.scatter(iris.data[iris.target == target][:,0]
                ,iris.data[iris.target == target][:,1]
                ,c = colors[target]
                ,label = labels[target]
                ,s = 50)
    labels[target] = None

plt.grid()
centers = kmeans.cluster_centers_
plt.scatter(centers[:,0],centers[:,1],marker = 'o',c = 'gray', s = 300, alpha = 0.5, label = "Centers")
plt.legend(loc = 1)
plt.show()



























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

m = DBSCAN(eps=0.7, min_samples=5,metric = distance_renormalise).fit(array_scrutin)


dico = {}
for eps_test in np.linspace(mini,maxi,100):
    for size_test in np.linspace(5,10,5):
        m = DBSCAN(eps=eps_test, min_samples=size_test,metric = distance_renormalise).fit(array_scrutin)
        labels = m.labels_
        if set(labels) >1:
            temp_list = []
            for label in set(labels):
                temp_list.append(list(labels).count(3))
            taille_classe_plus_petite = min(temp_list)
            dico[eps_test,size_test] = m,taille_classe_plus_petite


