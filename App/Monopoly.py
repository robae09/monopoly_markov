# -*- coding: utf-8 -*-
from Constantes import *
from monopoly.DataMonopoly import *
from structure.Markov import Markov
from collections import OrderedDict
import numpy as np


"""
    Représente le plateau de jeu monopoly et contient une chaine de Markov pour faire différentes
    simulation
"""
class Monopoly:

    """
        Constructeur

        @param dataMonopoly les informations pour construire l'objet monopoly
        @param markov (facultatif) il permet de définir manuellement la chaine de markov du Monopoly
    """
    def __init__(self, dataMonoply):
        dataMonoply.initMonopoly()
        self._dataMonopoly = dataMonoply
        self._matDeplacement = self.__creerMatriceDeplacementMonopoly()
        self._matInit = self.__creerMatriceInitialMonopoly()
        self._markov = Markov(self._matInit, self._matDeplacement)


    """
        Permet de créer une matrice contenant la probabilité d'accéder à une case se trouvant sur
        une colonne j à partir d'une case en ligne i.

        @return une matrice carré
    """
    def __creerMatriceDeplacementMonopoly(self):
        res = []

        for case in self._dataMonopoly.getListeCases():
            caseAccessible = case.getCasesSuivantes(self._dataMonopoly)

            ligne = []

            for selectCase in self._dataMonopoly.getListeCases():
                if(selectCase in caseAccessible):
                    ligne.append(caseAccessible[selectCase])
                else:
                    ligne.append(0)

            res.append(ligne)

        return np.array(res)


    """
        Permet de créer une matrice à une colonne avec la probabilité de commencé en une case donnée
        (par défaut, seule la case départ)

        @return une matrice à une colonne
    """
    def __creerMatriceInitialMonopoly(self):
        res = [[0 for i in range(len(self._dataMonopoly.getListeCases()))]]
        res[0][0] = 1
        return np.array(res)


    """
        Permet de simuler des tours sur le Monopoly actuelle

        @param nbrTour que l'on veut simuler

    """
    def simulerDesTours(self, nbrTour = 1):
        self._markov.ajouterDeplacement(nbrTour)

    """
        Permet de créer un "OrderDict" à partir des informations de répartition passé en paramètre

        @param data les informations de répartition qui seront utilisé pour créé l'objet
        @return un OrderDict contenant en clef la case et en valeur la probabilité
    """
    def __generateOrderDictFromData(self, data):
        res = OrderedDict()
        listCase = self._dataMonopoly.getListeCases()

        for i in range(len(listCase)):
            selectCase = listCase[i]
            valeur = data[i]
            if(isinstance(valeur, np.ndarray)):
                valeur = valeur[0]
            res[selectCase] = valeur

        return res

    """
        Permet de retourner chaque case et la probabilité de tomber dessus

        @return un OrderedDict contenant en clef la case et en valeur la probabilité
    """
    def getResultatSimulation(self):
        valeurCase = self._markov.multiplicationInitiatialeDeplacement()[0]
        return self.__generateOrderDictFromData(valeurCase)

    """ 
        Permet de simuler une "infinité" de tour.  C'est à dire trouver les points fixe
        de la chaine de Markov

        @return un OrderDict contenant en clef la case et en valeur la probabilité
    """
    def simulerInfini(self):
        valeurCase = self._markov.trouverPointFix()

        return self.__generateOrderDictFromData(valeurCase)

    """
        Permet de récupérer la matrice de déplacement

        @return la matrice de déplacement
    """
    def getMatriceDeplacement(self):
        return self._markov.getMatriceDeplacement()



"""
    Permet de créer un objet Monopoly avec des données spécifique au nom donné

    @param le nom des données du monopoly à charger
    @return l'objet Monopoly
"""
def getMonopoly(nom = "MONOPOLY_70"):
    return Monopoly(getDataMonopoly(nom))