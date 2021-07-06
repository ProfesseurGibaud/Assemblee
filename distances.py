# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:20:23 2021

@author: Sylgi
"""


def distance_renormalise(V1,V2):
    """


    Parameters
    ----------
    V1 : item de array_srutin : uid,suffragesExprimes,pour,contre,abstentions
        Scrutin 1
    V2 : item de array_scrutin : uid,suffragesExprimes,pour,contre,abstentions
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

def distance_eucli(V1,V2,poids_pour = 1/3,poids_contre = 1/3,poids_abstention = 1/3):
    """
    

    Parameters
    ----------
   V1 : item de array_srutin : uid,suffragesExprimes,pour,contre,abstentions
        Scrutin 1
    V2 : item de array_scrutin : uid,suffragesExprimes,pour,contre,abstentions
        Scrutin 2

    Returns
    -------
    d : la distance

    """
    
    d = poids_pour*abs(V1[2] - V2[2]) + poids_contre*abs(V1[3] - V2[3]) + poids_abstention*abs(V1[4] - V2[4])
    return d
