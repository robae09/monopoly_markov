# -*- coding: utf-8 -*-
from monopoly.Case import Case
from Constantes import *


"""
    Permet de réprésenter une case "Aller en prison"

    Informations: cette case redirige automatiquement vers la case Prison_1
"""
class CaseGoToPrison(Case):

    """
        Permet d'initiliser une case "Aller en prison"

        @param position de la carte sur le plateau de jeu
    """
    def __init__(self, position):
        super().__init__("Aller en prison", position, "gray", vendre=False)


    """
        Permet de récupérer les cases accèssibles depuis la case actuelle

        @param dataMonopoly les informations liées au plateau monopoly (permettant de récupérer 
            les autres cases)
        @return un dictionnaire avec en clef la Case accèssible et avec comme valeur la probabilité 
        de rejoindre cette case
        @Override
    """
    def getCasesSuivantes(self, dataMonopoly):
        return {dataMonopoly.getCasePrison(): 1}

