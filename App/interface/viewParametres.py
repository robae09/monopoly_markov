#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Tkinter and External
import tkinter as tk
from tkinter import messagebox
# Utils
from Constantes import *


"""
    LabelFrame permettant d'afficher les paramètres sélectionné précédemment
"""
class ViewParametres(tk.LabelFrame):


    """
        Création de la fenêtre

        @param fenetre parent
    """
    def __init__(self, fenetre, selectMonopolyData):
        tk.LabelFrame.__init__(self, fenetre, text="Paramètres choisis", padx=3, pady=3, labelanchor="n", \
                relief=tk.RAISED)

        self._parent = fenetre
        self._monopolyData = selectMonopolyData

        self.__initAllLabel()
        self.__updateAllValues()


    """
        Permet d'initialiser tous les labels
    """
    def __initAllLabel(self):
        self.__addLabelNom()
        self.__addLabelNbrDeDes()
        self.__addLabelNbrMaxPrisonTour()
        self.__addLabelProbSotirPrison()
        self.__addLabelNbrDoublePrison()


    """
        Permet de mettre à jour toutes les valeurs dans les labels
    """
    def __updateAllValues(self):
        # Nom du Monopoly
        self._nomMonopoly.set(self._monopolyData.getDisplayNom())
        # Nombre de dés
        self._nbrDeDes.set("Nombre de dés: " + str(self._monopolyData.getNbrDeDes()))
        # Nombre max de tour en prison
        self._nbrMaxPrison.set("Nombre de tour maximum en prison: " + \
            str(self._monopolyData.getMaxTourPrison()))
        # Probabilité de payer pour sortir de prison
        self._probSortirPrison.set("Probabilité de payer pour sortir de prison: " + \
            str(self._monopolyData.getProbSortirPrison()))
        # Nombre de double avant d'aller en prison
        self._nbrDoublePrison.set("Nombre de double avant d'aller en prison: " + \
            str(self._monopolyData.getNbrDeDouble()))


    """
        Permet d'ajouer un label avec le nom du Monopoly actuellement affiché
    """
    def __addLabelNom(self):
        self._nomMonopoly = tk.StringVar()
        tk.Label(self, textvariable=self._nomMonopoly, anchor="n", wraplength=130, \
            justify=tk.CENTER).pack(pady=5)


    """
        Permet d'ajouter un label affichant le nombre de dés qui a été choisi
    """
    def __addLabelNbrDeDes(self):
        self._nbrDeDes = tk.StringVar()
        tk.Label(self, textvariable=self._nbrDeDes, anchor="n", wraplength=130, justify=tk.LEFT)\
            .pack(pady=5)

    """
        Permet d'ajouter un label affichant le nombre de tour que l'on peut passer en prison
    """
    def __addLabelNbrMaxPrisonTour(self):
        self._nbrMaxPrison = tk.StringVar()
        tk.Label(self, textvariable=self._nbrMaxPrison, anchor="n", wraplength=130, \
            justify=tk.LEFT).pack(pady=5)


    """
        Permet d'ajouter un label permettant d'afficher la probabiliter que le joueur décide
        de payer pour sotir de prison
    """
    def __addLabelProbSotirPrison(self):
        self._probSortirPrison = tk.StringVar()
        tk.Label(self, textvariable=self._probSortirPrison, anchor="n", wraplength=130, \
            justify=tk.LEFT).pack(pady=5)


    """
        Permet d'ajouter un label permettant d'afficher le nombre de double que le joueuer peut faire
        avant de se retrouver automatiquement en prison
    """
    def __addLabelNbrDoublePrison(self):
        self._nbrDoublePrison = tk.StringVar()
        tk.Label(self, textvariable=self._nbrDoublePrison, anchor="n", wraplength=130, \
            justify=tk.LEFT).pack(pady=5)


    """
        Permet de mettre à jour les informations du Monopoly actuellement affiché
    """
    def setNewMonopolyData(self, newMonopolyData):
        self._monopolyData = newMonopolyData
        self.__updateAllValues()
