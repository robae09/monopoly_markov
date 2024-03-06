#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Tkinter and External
import tkinter as tk

from math import ceil
from interface.caseCercle import CaseCercle

import math


"""
    LabelFrame contenant un canvas et permettant de dessiner la chaine de Markov
"""
class viewMarkov(tk.LabelFrame):

    CIRCLE_SIZE = 10
    ESPACE = 50
    CASE_PAR_LIGNE = 10
    ARC_DECALAGE = -40
    TAILLE_PLATEAU = 300 # Taille que prend la représentation d'un plateau


    """
        Permet d'initialiser la fenêtre

        @param fenetre la fenêtre parente à celle-ci
        @param nbrDeDoubles avant d'aller en prison
        @param listCase liste des cases à afficher
        @param matriceDeplacement matrice contenant tous les déplacements des états possibles
    """
    def __init__(self, fenetre, nbrDeDoubles, listCase, matriceDeplacement):
        tk.LabelFrame.__init__(self, fenetre, text="Chaine de Markov", padx=0, pady=0, labelanchor="n")

        self._listeCercleCase = {} # Liste stockant l'id du cercle en fonction de l'id de la case
        self._listeLigneDepl = {}  # Liste stockant l'id de la ligne en fonction de l'id de la case de départ

        self._nbrDeDoubles = nbrDeDoubles
        self._listeCase = listCase
        self._matriceDeplacement = matriceDeplacement
        self.__drawMarkov()


    """
        Permet de remettre à jour tout le canvas

        @param listeCases la nouvelle liste des cases
        @param nbrDeDoubles le nombre de double avant d'aller en prison
        @param matriceDeplacement la matrice de déplacement
    """
    def updateAll(self, listeCases, nbrDeDoubles, matriceDeplacement):
        self._canvas.delete("all")
        self._canvas.destroy()
        self._listeCercleCase = {}
        self._listeLigneDepl = {}


        self._listeCase = listeCases
        self._nbrDeDoubles = nbrDeDoubles
        self._matriceDeplacement = matriceDeplacement

        self.__drawMarkov()


    """
        Permet de dessiner la chaine de Markov en tant que tel
    """
    def __drawMarkov(self):
        self.__initLimitAndBorder()

        # Création du canvas
        self._canvas = tk.Canvas(self, 
            width=self._width+(2*self._borderX), 
            height=self._height+(2*self._borderY), 
            background='white')

        self._canvas.pack()
        self.__drawAllNodes()
        self.__drawAllDeplacement()


    """
        Permet d'initialiser les variables définissant les bordures et les échelles
    """
    def __initLimitAndBorder(self):
        self._width = 1200
        self._height = viewMarkov.TAILLE_PLATEAU * ((1 if self._nbrDeDoubles <= 0 else self._nbrDeDoubles) +1)
        self._borderX = 150
        self._borderY = 150


    """
        Permet de dessiner les cases du Monopoly, représenté par des noeud
    """
    def __drawAllNodes(self):
        index = [0]
        for case in self._listeCase:
            # Nombre de double pour atteindre cette case
            nbrDeDouble = case.getNbrDeDouble()

            # Gestion des index
            while(nbrDeDouble >= len(index)):
                index.append(0)
            currentIndex = index[nbrDeDouble]

            (x, y, angle) = self.__generatePlateauCoord(currentIndex, nbrDeDouble)
            self.__drawCase(case, x, y, angle)
            index[nbrDeDouble] += 1


    """
        Permet de dessiner les déplacements possibles
    """
    def __drawAllDeplacement(self):
        index = 0
        for case in self._listeCase:
            colonne = 0

            for elem in self._matriceDeplacement[index]:
                caseDest = self._listeCase[colonne]
                if(elem > 0):
                    self.__drawDeplacement(case, caseDest)

                colonne += 1
            index += 1


    """
        Permet d'afficher une case sur le canvas

        @param case qu'il faut représenter
        @param x coordonnée x
        @param y coordonnée y
    """
    def __drawCase(self, case, x, y, angle):
        coordLeftX = x - viewMarkov.CIRCLE_SIZE + self._borderX
        coordTopY = y - viewMarkov.CIRCLE_SIZE + self._borderY
        coordRightX = x + viewMarkov.CIRCLE_SIZE + self._borderX
        coordBottomY = y + viewMarkov.CIRCLE_SIZE + self._borderY

        nbrDeDouble = case.getNbrDeDouble()
        idCase = case.getPosition()
        caseCercle = CaseCercle(self._canvas, case, coordLeftX, coordRightX, coordTopY, coordBottomY,
            angle)
        self._listeCercleCase[(idCase, nbrDeDouble)] = caseCercle


    """
        Permet de retrouver les coordonnées central à partir des informations concernant les 
        coordonnées que nous donnent tkinter

        @param allCoordinate toutes les informations concernant les coordonnées de tkinter (
            coordonnées du point en haut à gauche et en bas à droite)
        @return un tuple contenant les coordonnées x, y
    """
    def __getCenterOfOval(self, allCoordinate):
        x0 = allCoordinate[0]
        y0 = allCoordinate[1]

        x1 = allCoordinate[2]
        y1 = allCoordinate[3]

        diffX = max(x0, x1) - min(x0, x1)
        diffY = max(y0, y1) - min(y0, y1)

        return min(x0, x1) + diffX/2, min(y0, y1) + diffY/2


    """
        Permet de dessiner une ligne entre deux cases (représentant donc un déplacement possible sur
            le plateau de Monopoly)

        @param caseSource la case de départ
        @param caseDest la case de destination
    """
    def __drawDeplacement(self, caseSource, caseDest):
        idCaseSource = caseSource.getPosition()
        idCercleSource = self._listeCercleCase[(idCaseSource, caseSource.getNbrDeDouble())]
        idCercleDest = self._listeCercleCase[(caseDest.getPosition(), caseDest.getNbrDeDouble())]

        self.__createArc(idCercleSource, idCercleDest)


    """
        Permet de tracer un arc de cercle entre deux points

        @param caseSource l'objet caseCercle source
        @param caseDest l'objet caseCercle destination
    """
    def __createArc(self, caseSource, caseDest):
        variableSource = caseSource.getCoords()
        variableDest = caseDest.getCoords()

        coordsSource = self.__getCenterOfOval(variableSource)
        coordsDest = self.__getCenterOfOval(variableDest)

        minX = min(coordsSource[0], coordsDest[0])
        minY = min(coordsSource[1], coordsDest[1])

        milieuX = minX
        milieuY = minY
        
        diffX = max(coordsSource[0], coordsDest[0]) - minX
        diffY = max(coordsSource[1], coordsDest[1]) - minY

        if(diffY == 0):
            milieuX += diffX/2
            milieuY += viewMarkov.ARC_DECALAGE

        elif(diffX == 0):
            milieuX += viewMarkov.ARC_DECALAGE
            milieuY += diffY/2

        else:
            milieuX += diffX/2 + viewMarkov.ARC_DECALAGE
            milieuY += diffY/2 + viewMarkov.ARC_DECALAGE

        milieu = (milieuX, milieuY)

        idLine = self._canvas.create_line(coordsSource, milieu, coordsDest, smooth=True, fill="gray83")
        self._canvas.tag_lower(idLine)

        caseSource.addRelation(idLine, caseDest)


    """
        Permet de récupérer la position de la ième case

        @param index de la case à placer
        @param nbrDeDouble nombre de double pour atteindre cette case
        @return un tuple x, y, position du text
    """
    def __generatePlateauCoord(self, index, nbrDeDouble = 0):
        angle = 0
        x = 650 if (nbrDeDouble % 2 == 1) else 0
        y = nbrDeDouble * viewMarkov.TAILLE_PLATEAU

        if(index < viewMarkov.CASE_PAR_LIGNE):
            x += index * viewMarkov.ESPACE
            # y = 0
            angle = 90

        elif(index < viewMarkov.CASE_PAR_LIGNE * 2):
            x += viewMarkov.CASE_PAR_LIGNE * viewMarkov.ESPACE
            y += (index-viewMarkov.CASE_PAR_LIGNE) * viewMarkov.ESPACE

        elif(index < viewMarkov.CASE_PAR_LIGNE * 3):
            maxX = viewMarkov.CASE_PAR_LIGNE * viewMarkov.ESPACE
            x += maxX - ((index - (2 * viewMarkov.CASE_PAR_LIGNE)) * viewMarkov.ESPACE)
            y += viewMarkov.CASE_PAR_LIGNE * viewMarkov.ESPACE
            angle = 90

        elif(index < viewMarkov.CASE_PAR_LIGNE * 4):
            # x = 0
            maxY = viewMarkov.CASE_PAR_LIGNE * viewMarkov.ESPACE
            y += maxY - ((index - (3 * viewMarkov.CASE_PAR_LIGNE)) * viewMarkov.ESPACE)

        else:
            newIndex = (index - viewMarkov.CASE_PAR_LIGNE * 4)
            x += (viewMarkov.CASE_PAR_LIGNE + 2) * viewMarkov.ESPACE
            y += newIndex * viewMarkov.ESPACE

        return x, y, angle


