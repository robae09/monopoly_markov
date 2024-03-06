# -*- coding: utf-8 -*-
from monopoly.Case import Case
from Constantes import *


"""
    Permet de réprésenter une case Prison

    Informations: 
    La case prison fait soit référence à la prochaine case prison (de base 3 chances), soit à une 
    case pouvant être atteint via un double.

    /!\ Warning !  La case prison est donc dupliqué pour représenter les différents tours que l'on 
    peut passer sur celle-ci.
"""
class CasePrison(Case):

    """
        Permet d'initiliser une case Prison

        @param numero de la case prison (représentant le nombre de tour passé sur cette case)
    """
    def __init__(self, decalage, numero):
        super().__init__("Prison " + str(numero+1), decalage+numero, "black", vendre=False)
        self._tourEnPrison = numero


    """
        Permet de récupérer les cases accèssibles depuis la case actuelle

        @param dataMonopoly les informations liées au plateau monopoly (permettant de récupérer 
            les autres cases)
        @return liste des objets cases étant accèssibles
        @Override
    """
    def getCasesSuivantes(self, dataMonopoly):
        res = {}

        # On récupère la prison suivante
        nextPrison = self.__getNextCasePrison(dataMonopoly)

        # Case "prison visite uniquement" (qui sert de case de départ)
        casePrisonVisiteUniquement = dataMonopoly.getPrisonVisiteUniquement()

        # Définit par défaut que le joueur ne doit pas payer
        proportionPayer = 0

        # Si on est sur la première case prison, le joueur peut décider de sortir de prison
        if(self._tourEnPrison == 0):
            proportionPayer = dataMonopoly.getProbSortirPrison()
            res = casePrisonVisiteUniquement.getCasesSuivanteDes(dataMonopoly, proportionPayer)

        # Si c'est le dernier tour que l'on peut faire en prison, il faut payer
        elif(nextPrison == None):
            proportionPayer = 1
            res = casePrisonVisiteUniquement.getCasesSuivanteDes(dataMonopoly)


        # Si on est pas obligé de payer
        if(proportionPayer < 1):
            proportionJouer = 1-proportionPayer
            self.__getCaseSuivanteLanceDes(res, dataMonopoly, nextPrison, \
                                casePrisonVisiteUniquement, proportionJouer)

        return res


    """
        Permet de calculer la probabilité de faire un double et met en relation cette probabilité avec
        la case où le joueur se trouvera

        @param res permet de stocker le résultat
        @param dataMonopoly les informations liées au plateau monopoly (permettant de récupérer 
            les autres cases)
        @param nextPrison case indiquant la prison suivante (un tour de plus)
        @param caseVisitePrison case a partir de laquelle on commence à compté lorsqu'on sort de prison
        @param probabiliteJouer quel est la probabilité que le joueur joue (à la place de payer)
        @return liste des objets cases étant accèssibles
    """
    def __getCaseSuivanteLanceDes(self, res, dataMonopoly, nextPrison, caseVisitePrison, \
                            probabiliteJouer):
        # Nombre de dés utilisé pour la partie
        nbrDeDes = dataMonopoly.getNbrDeDes()

        # Récupère la position de la case "visite simple"
        posCasePrisonVisite = caseVisitePrison.getPosition()

        # => Lancer les dés
        nbrLancePossible = pow(6, nbrDeDes) # Nombre de combinaisont possible

        # Faire un double
        nombreDeDouble = 0
        for i in range(nbrDeDes, nbrDeDes*6+1, nbrDeDes):
            res[dataMonopoly.getCase(posCasePrisonVisite+i)] = (1/nbrLancePossible)*probabiliteJouer
            nombreDeDouble += 1

        # Aucun double n'a été fait
        res[nextPrison] = ((nbrLancePossible-nombreDeDouble)/nbrLancePossible)*probabiliteJouer



    """
        Permet de récupérer la case prison juste après la case actuelle (si elle n'existe pas, 
        on renvoie None)

        @parma dataMonopoly les informations liées au plateau monopoly
        @return la prochaine case prison ou None si pas trouvé
    """
    def __getNextCasePrison(self, dataMonopoly):
        res = None # Resultat

        # Si ce n'est pas notre dernier tour en prison
        if(self._tourEnPrison < dataMonopoly.getMaxTourPrison()):
            res = dataMonopoly.getCasePrison(self._tourEnPrison+1)

        return res
