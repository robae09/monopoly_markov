#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Tkinter and External
import tkinter as tk

"""
    LabelFrame contenant un canvas et dessinant les statistiques
"""
class Statistiques(tk.LabelFrame):

    """
        Création de la fenêtre de statistique

        @param stats_data information à afficher (dictionnaire contenant en clef les cases et en
            valeur la probabilitéde s'y trouver)
        @param fenetre parent
    """
    def __init__(self, stats_data, fenetre):
        tk.LabelFrame.__init__(self, fenetre, text="Graphique", padx=0, pady=0, labelanchor="n")
        self._stats_data = stats_data

        self._listStatCanvas=[] # Stock tous les éléments représentant les statistiques sur le canvas

        self.__drawGraphique()


    """
        Permet de créer le canvas où on va dessiner le graphique
    """
    def __drawGraphique(self):
        # Initialisation des limites
        self.__initLimitAndBorder()

        # Création du canvas
        self._canvas = tk.Canvas(self, 
            width=self._width+(2*self._borderX), 
            height=self._height+(self._borderBottomY+self._borderTopY), 
            background='white')
        
        # Desin des axes et des statistiques
        self.__creerAxeX()
        self.__creerAxeY()
        self.__drawStats()

        self._canvas.pack()


    """
        Permet d'initialiser les variables définissant les bordures et les échelles
    """
    def __initLimitAndBorder(self):
        self._width = 1300
        self._height = 150
        self._borderX = 25
        self._borderBottomY = 210
        self._borderTopY = 50

        self._maxY = int(max(self._stats_data.values())*100 + 1)
        self._nbrCase = len(self._stats_data)
        self._valeurEchelleY = self._height/self._maxY
        self._valeurEchelleX = self._width/self._nbrCase


    """
        Permet d'initialiser l'axe X (et de lui mettre une échelle)
    """
    def __creerAxeX(self):
        self._canvas.create_line(self._borderX, self._height+self._borderTopY, 
            self._width+self._borderX, self._height+self._borderTopY)
        self.__creerEchelleX()
    

    """
        Permet de crer l'échelle des X en fonction des données
    """ 
    def __creerEchelleX(self):
        currentX = self._borderX
        for i in range(self._nbrCase):
            ligne = self._canvas.create_line(currentX, self._height+self._borderTopY, 
                currentX, self._height+self._borderTopY+5)
            self._listStatCanvas.append(ligne)
            # Incrémentation
            currentX += self._valeurEchelleX


    """
        Permet d'initialiser l'axe Y (et de lui mettre une échelle)
    """
    def __creerAxeY(self):
        self._canvas.create_line(self._borderX, self._height+self._borderTopY, 
            self._borderX, self._borderTopY)
        self.__creerEchelleY()


    """
        Permet de crer l'échelle des Y en fonction des données
    """
    def __creerEchelleY(self):
        currentY = self._height+self._borderTopY
        
        for i in range(self._maxY):

            # Dessin de l'ordonnée
            ligne = self._canvas.create_line(self._borderX, currentY, 
                self._borderX-5, currentY)
            self._listStatCanvas.append(ligne)

            # Créer les lignes pointiée grises sur tous le graphique
            if(i > 0 and (self._maxY < 10 or i%2 == 0)):
                pointille = self._canvas.create_line(self._borderX, currentY, 
                    self._borderX+self._width, currentY, 
                    dash=(9, 20), fill="gray")
                self._listStatCanvas.append(pointille)

            # Numéroté l'échelle
            if(self._maxY < 10 or i%2 == 0):
                numero = self._canvas.create_text(self._borderX-15, currentY, text=str(i))
                self._listStatCanvas.append(numero)

            # Incrémentation
            currentY -= self._valeurEchelleY


    """
        Permet de dessiner les carrés représentant les statistiques
    """
    def __drawStats(self):
        currentResultX = self._borderX
        nouveauCurrentResultX = currentResultX
        for case in self._stats_data:
            result = self._stats_data[case]
            valeurPourcent = result*100

            nouveauCurrentResultX += self._width/(len(self._stats_data))
            hauteur = (self._height+self._borderTopY)-(valeurPourcent*self._valeurEchelleY)

            # Ajout du pourcentage
            pourcent = self._canvas.create_text(currentResultX+2, hauteur-10, 
                text=str(round(valeurPourcent, 2)) + "%", anchor="nw", angle=90)
            self._listStatCanvas.append(pourcent)

            # Ajout du rectangle
            rectangle = self._canvas.create_rectangle(currentResultX, hauteur, 
                nouveauCurrentResultX, self._height+self._borderTopY, fill=str(case.getCouleur()))
            self._listStatCanvas.append(rectangle)

            # Ajout du nom
            nom = self._canvas.create_text(currentResultX+5, self._height+self._borderTopY+10, 
                text=str(case.getNom()), angle=80, anchor="ne")
            self._listStatCanvas.append(nom)

            # Incrémentation
            currentResultX = nouveauCurrentResultX


    """
        Permet de supprimer tous les éléments représentant les statisiques sur le canvas
    """
    def __clearStatsCanvas(self):
        for elem in self._listStatCanvas:
            self._canvas.delete(elem)


    """
        Permet de mettre à jour le canvas

        @param new_data nouvelle information à afficher
    """
    def updateCanvas(self, new_data):
        self._stats_data = new_data
        self.__clearStatsCanvas()
        self.__initLimitAndBorder()
        self.__creerEchelleX()
        self.__creerEchelleY()
        self.__drawStats()

        
