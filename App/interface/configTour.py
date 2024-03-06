#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Tkinter and External
import tkinter as tk
from tkinter import messagebox
# Utils
from Constantes import *


"""
    LabelFrame permettant de modifier le nombre de tour à simuler/afficher
"""
class ConfigTour(tk.LabelFrame):


    """
        Création de la fenêtre

        @param fenetre parent
    """
    def __init__(self, fenetre, parent):
        tk.LabelFrame.__init__(self, fenetre, text="Gestion des tours", padx=3, pady=3, labelanchor="n", \
                relief=tk.RAISED)

        self._parent = parent

        self.__addLabelNbrTour()
        self.__addNbrTourEntry()
        self.__addNextTourButton()
        self.__addPrevTourButton()
        self.__addSubmitButton()

        self.__addFixedEtatButton()


    """
        Permet d'afficher un texte indiquant que cette partie s'occupe de la gestion des tour
    """
    def __addLabelNbrTour(self):
        tk.Label(self, text="Nombre de tour:", anchor="n").grid(row=0, column=0, padx=5, 
            columnspan=2)


    """
        Permet d'ajouter un bouton permettant de passer au tour suivant
    """
    def __addNextTourButton(self):
        tk.Button(self, text="->", command=self.commandNextTourButton)\
            .grid(row=2, column=1, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)


    """
        Permet d'ajouter un bouton permettant de revenir au tour précédent
    """
    def __addPrevTourButton(self):
        tk.Button(self, text="<-", command=self.commandPrevTourButton)\
            .grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)


    """
        Fonction appellé lorsqu'on veut avancé de 1 le nombre de tour
    """
    def commandNextTourButton(self, event = None):
        self.__setNbrTourASimuler(self.getNbrTourASimuler()+1)
        self.__submitChange()


    """
        Fonction appellé lorsqu'on veut reculé (retourné au nombre de tour précédent) de 1 le 
        nombre de tour
    """
    def commandPrevTourButton(self, event = None):
        nbrASimuler = self.getNbrTourASimuler()-1
        self.__setNbrTourASimuler(nbrASimuler)
        self.__submitChange()


    """
        Permet d'ajouter une entrée permettant de directement rentrer le nombre de tour que l'on
        veut simuler
    """
    def __addNbrTourEntry(self):
        self._valeurEntry = tk.StringVar()
        tk.Entry(self, textvariable=self._valeurEntry, justify='right', width=7)\
            .grid(row=1, column=0)
        self.__setNbrTourASimuler(1)


    """
        Permet d'ajouter un bouton pour envoyer les informations à la fenêtre parent
    """
    def __addSubmitButton(self):
        tk.Button(self, text="Valider", command=self.__submitChange, anchor="s")\
            .grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)


    """
        Permet d'ajouter un bouton permettant d'afficher l'état fixe des états
    """
    def __addFixedEtatButton(self):
        tk.Button(self, text="Point fixe", command=self.commandFixedEtat, anchor="center")\
            .grid(row=4, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W, pady=5)

    """
        Fonction appellée lorsqu'on clic sur le bouton "Fixed Etat".
    """
    def commandFixedEtat(self, event = None):
        self._parent.updateNewTour(True)


    """
        Permet de valider les choix du nombre de tour et de mettre à jour le graphique
    """
    def __submitChange(self):
        self._parent.updateNewTour()


    """
        Permet de définir le nombre de tour qui doit être simulé

        @param newNbrTour le nouveau nombre de tour qui doivent être simulé
    """
    def __setNbrTourASimuler(self, newNbrTour):
        newNbrTour = self.__isNbrTourValideAndGet(newNbrTour)
        self._valeurEntry.set(str(newNbrTour))


    """
        Permet de savoir si le nombre de tour définit est valide
        Si il ne l'est pas, un message d'avertissement est définit 

        @param testNbrTour le nombre de tour à tester
        @return le nombre de tour correcte (0 si incorrecte)
    """
    def __isNbrTourValideAndGet(self, testNbrTour):
        if(testNbrTour < 0):
            messagebox.showwarning("Opération impossible", "Vous ne pouvez pas définir un nombre " \
                "en dessous de 0")
            testNbrTour = 0
        
        return testNbrTour



    ################# PUBLIC #####################

    """
        Permet de récupérer le nombre de tour que l'on veut simuler

        @return le nombre de tour que l'on doit simuler
    """
    def getNbrTourASimuler(self):
        nbrTour = int(self._valeurEntry.get())
        newNbrTour = self.__isNbrTourValideAndGet(nbrTour)
        if(newNbrTour != nbrTour):
            self.__setNbrTourASimuler(newNbrTour)
            nbrTour = newNbrTour
        return nbrTour
