#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

class Help(tk.Toplevel):

    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("Aide")

        self.__addAllText()

        self.__initEvent()


    """
        Permet d'initialiser les events
    """
    def __initEvent(self):
        self.bind("<Escape>", self.__closeAide)


    def __addAllText(self):
        tk.Label(self, text="Plusieurs racourcis sont présent dans cette application\n" \
            "<Ctr+h> Ouvre cette fenêtre\n" \
            "<Ctr+l> Affiche la liste des cases ordonnés\n"\
            "<Ctr+p> Permet de modifier les paramètres\n"\
            "<Ctr+m> Permet de changer de Monopoly\n"\
            "<Ctr+▶> Simuler un tour de plus\n"\
            "<Ctr+◀> Simuler un tour de moins\n"\
            "<Ctr+▲> Simulation de la chaîne de Markov au point fixe\n"\
            "<Escape> Permet de fermer les Popup (tel que celui-ci)",
            justify=tk.LEFT, padx=10).pack()


    """
        Fonction appellé lorsque l'on veut fermer la fenêtre
    """
    def __closeAide(self, event = None):
        self.quit()
        self.destroy()