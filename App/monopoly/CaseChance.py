# -*- coding: utf-8 -*-
from monopoly.Case import Case

"""
    Permet de réprésenter une case Chance

    Informations:
    - 8 cartes inutiles (payements)  -> 8/16
    - 1 carte sortir de prison      -> 1/16
    - 7 cartes déplacement           -> 7/16
    Total = 16

"""
class CaseChance(Case):


    """
        Permet d'initiliser une case chance

        @param position de la case sur le plateau de jeu
    """
    def __init__(self, position):
        super().__init__("Chance", position, "RosyBrown1", vendre=False)


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

        # Recule de 3 cases
        res[dataMonopoly.getCase(self._position-3)] = proportion 
        # Case départ
        res[dataMonopoly.getCase(0)] = proportion 
        # Première du 2ème côté
        res[dataMonopoly.getCase(11)] = proportion 
        # "Aeroport" du 2ème côté
        res[dataMonopoly.getCase(15)] = proportion
        # Fin de la première série de cases du 3ème côté
        res[dataMonopoly.getCase(24)] = proportion 
        # Case la plus cher
        res[dataMonopoly.getCase(39)] = proportion
        # Case prison 
        res[dataMonopoly.getCasePrison()] = proportion

        # Ajout des autres cases où le joueur peut lancer le dé
        casesPourDes = self.getCasesSuivanteDes(dataMonopoly, 9/16)
        for case in casesPourDes:
            if case in res:
                res[case] += casesPourDes[case]
            else:
                res[case] = casesPourDes[case]

        return res


