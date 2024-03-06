# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy


"""
    Permet de représenter une chaine de markov.
    Cet objet contient donc plusieurs matrices
"""
class Markov:

    """
        Constructeur

        @param matInit matrice contenant les points de départs
        @param matDeplacement matrice contenant tous les changements d'états possible
    """
    def __init__(self, matInit, matDeplacement):
        self._matInit = matInit
        self._matDeplacement = matDeplacement

        # Cache stockant les résultats des exposants de la matrice de déplacement
        self._cacheExpoMatDepl = {0: np.eye(len(self._matDeplacement)), 1: self._matDeplacement} 


    """
        Ajout d'un déplacement/un changement d'état
    """
    def ajouterUnDeplacement(self):
        return ajouterDeplacement(1)


    """
        Ajout d'un déplacement, en d'autres mot: situation après un changement d'état

        @param nbrDeplacement nombre de déplacement/changement d'état à faire
    """
    def ajouterDeplacement(self, nbrDeplacement):
        if(nbrDeplacement in self._cacheExpoMatDepl):
            res = self._cacheExpoMatDepl[nbrDeplacement]
        else:
            initMatDeplacement = self._cacheExpoMatDepl[1]
            res = np.linalg.matrix_power(initMatDeplacement, nbrDeplacement)
            self._cacheExpoMatDepl[nbrDeplacement] = res

        self._matDeplacement = res

        return res


    """
        Permet de récupérer la matrice de déplacement de la chaine de markov

        @return la matrice représentant les déplacements possibles
    """
    def getMatriceDeplacement(self):
        return self._cacheExpoMatDepl[1]
        

    """
        Permet de trouver les points fix à partir d'un point de départ précis
    """
    def trouverPointFix(self):
        matriceDeplacement = self._cacheExpoMatDepl[1]

        # Le but final du calcul est de faire:
        # (P-I)^T w = (0, ..., 0, 1)
        # Où p est la matrice de déplacement et w la matrice que l'on cherche

        nbrLigne = len(matriceDeplacement)
        nbrColonne = len(matriceDeplacement[0])

        # Matrice avec laquelle on va travailler (histoire de ne pas modifier par erreur)
        # la matrice de déplacement
        matriceTravail = deepcopy(matriceDeplacement)

        if(nbrLigne != nbrColonne):
            print("[WARNING] Le nombre de ligne n'est pas le même que le nombre de colonne " \
                    "(" + nbrLigne + ", " + nbrColonne + ")")

        matriceUnite = np.eye(nbrLigne)
        matriceTravail = matriceTravail - matriceUnite

        # On rajoute une colonne de un à la matrice de déplacement
        colonneDeUn = np.ones((nbrLigne, 1))
        matriceTravail = np.append(matriceTravail, colonneDeUn, axis=1)

        # On créé la matrice indiquant les résultats qui seront utilisé pour réalisé le calcul
        # C'est à dire une matrice colonne remplis de 0 sauf le dernier élément qui est un 1
        matriceResultat = np.zeros((nbrColonne+1, 1))
        matriceResultat[nbrColonne][0] = 1

        invMatriceTravail = matriceTravail.transpose()

        solution = np.linalg.lstsq(invMatriceTravail, matriceResultat)

        return solution[0]


    # TODO changer avec le bon nom
    def multiplicationInitiatialeDeplacement(self):
        return np.dot(self._matInit, self._matDeplacement)

