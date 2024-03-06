# -*- coding: utf-8 -*-
from monopoly.Case import Case

"""
    Permet de réprésenter une case Communauté

    Informations:
    - 12 cartes inutiles (payements)  -> 12/16
    - 1 cartes sortir de prison      -> 1/16
    - 3 cartes déplacement           -> 3/16
    Total = 16

"""
class CaseCommunaute(Case):


    """
        Permet d'initiliser une case communauté

        @param position de la case sur le plateau de jeu
    """
    def __init__(self, position):
        super().__init__("Caisse de Communauté", position, "LightYellow2", vendre=False)


    """
        Permet de récupérer les cases accèssibles depuis la case actuelle

        @param dataMonopoly les informations liées au plateau monopoly (permettant de récupérer 
            les autres cases)
        @return un dictionnaire avec en clef la Case accèssible et avec comme valeur la probabilité 
        de rejoindre cette case
        @Override
    """
    def getCasesSuivantes(self, dataMonopoly):
        res = {}

        proportion = 1/16

        # Case départ
        res[dataMonopoly.getCase(0)] = proportion 
        # Première case du jeu
        res[dataMonopoly.getCase(1)] = proportion 
        # Case prison 
        res[dataMonopoly.getCasePrison()] = proportion

        # Ajout des autres cases où le joueur peut lancer le dé
        casesPourDes = self.getCasesSuivanteDes(dataMonopoly, 13/16)
        for case in casesPourDes:
            if case in res:
                res[case] += casesPourDes[case]
            else:
                res[case] = casesPourDes[case]

        return res


