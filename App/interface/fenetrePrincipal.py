#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Tkinter and External
import tkinter as tk
from collections import OrderedDict
# Utils
from Constantes import *
from Monopoly import Monopoly
import monopoly.DataMonopoly as dataMonopoly
# Interface
from interface.scrollTk import scrollTk
from interface.choixMonopoly import ChoixMonopoly
from interface.parametres import Parametres_2
from interface.statistiques import Statistiques
from interface.viewMarkov import viewMarkov
from interface.configTour import ConfigTour
from interface.viewParametres import ViewParametres
from interface.listeStatistiques import ListeStatistiques
from interface.help import Help



"""
    FenetrePrincipal qui hérite de tkinter.Tk et contenant toutes les autres fenêtres à afficher
"""
class FenetrePrincipal(scrollTk):

    def __init__(self):
        scrollTk.__init__(self)
        self.wm_title("Stats")
        self.config(padx=5, pady=5) # TODO check que c'est bon

        # Init attributs
        self._selectedDataMonopoly = None
        self._nbrTourFrame = None
        self._viewParam = None
        self._markovFrame = None
        self._listStatistique = None

        # Choix des paramètres
        self.__choixParametres()

        # Choix du monopoly
        try:
            self.__choixMonopoly()
        except TypeError:
            return

        # Affichage des paramètres choisi
        self._viewParam = ViewParametres(self.getMainFrame(), self._selectedDataMonopoly)
        self._viewParam.grid(row=1, column=1, padx=7, sticky=tk.N+tk.S+tk.E+tk.W)

        # Création de la fenêtre de gestion de tour
        self._nbrTourFrame = ConfigTour(self.getMainFrame(), self)
        self._nbrTourFrame.grid(row=0, column=1, padx=7, sticky=tk.N+tk.E+tk.W)

        # Permet de récupérer toutes les informations sur les cases
        caseData = self.__sumSameCase(self._selectedMonopoly.getResultatSimulation())
        self._dataSimulation = caseData

        # Création de la fenêtre de statistique
        self._statFrame = Statistiques(self._dataSimulation, self.getMainFrame())
        self._statFrame.grid(row=0, column=0, rowspan=2)

        self._markovFrame = viewMarkov(self.getMainFrame(), self._selectedDataMonopoly.getNbrDeDouble(), \
                                    self._selectedDataMonopoly.getListeCases(), \
                                    self._selectedMonopoly.getMatriceDeplacement())
        self._markovFrame.grid(row=2, column=0, columnspan=2)

        # Création de la bar de menu
        self.__createMenuBar()

        self.__refreshScroll()
        self.__initEvent()

        self.wait_window(self)


    def __initEvent(self):
        self.bind("<Control-l>", self.__viewListStats)
        self.bind("<Control-h>", self.__viewHelp)
        self.bind("<Control-Right>", self._nbrTourFrame.commandNextTourButton)
        self.bind("<Control-Left>", self._nbrTourFrame.commandPrevTourButton)
        self.bind("<Control-Up>", self._nbrTourFrame.commandFixedEtat)
        self.bind("<Control-m>", self.__choixMonopoly)
        self.bind("<Control-p>", self.__choixParametres)


    """
        Permet de créer la bar de menu en haut de la fenêtre
    """
    def __createMenuBar(self):
        menubar = tk.Menu(self)

        ###### Menu ######
        paramMenu = tk.Menu(menubar, tearoff=0)
        paramMenu.add_command(label="Changer les paramètres", command=self.__choixParametres)
        paramMenu.add_command(label="Changer de Monopoly", command=self.__choixMonopoly)
        paramMenu.add_separator()
        paramMenu.add_command(label="Aide", command=self.__viewHelp)
        paramMenu.add_separator()
        paramMenu.add_command(label="Quitter", command=self.quit)

        menubar.add_cascade(label="Options", menu=paramMenu)

        ###### View ###### 
        paramView = tk.Menu(menubar, tearoff=0)
        paramView.add_command(label="Statistiques ordonnée", command=self.__viewListStats)

        menubar.add_cascade(label="Fenêtre", menu=paramView)

        # Afficher le mneu menu
        self.config(menu=menubar)


    """
        Permet de choisir le Monopoly que l'on veut simuler
    """
    def __choixMonopoly(self, event = None):

        newDataMonopoly = dataMonopoly.getAllDataMonopoly()[4] # selectionne le Monopoly printemps des sciences

        # newDataMonopoly = self.__displayChoixDuMonopoly()

        # Si on ne chosi aucun Monopoly
        if(newDataMonopoly == None and self._selectedDataMonopoly == None):
            raise TypeError('Aucun Monopoly sélectionné')

        if(newDataMonopoly != self._selectedDataMonopoly and newDataMonopoly != None):
            self._selectedDataMonopoly = newDataMonopoly
            self.__refrechMonopolyData()


    """
        Permet d'afficher la fenêtre permettant de choisir le Monopoly à utiliser et récupèré 
        proprement le résultat

        @return l'objet DataMonopoly contenant toutes les informations du Monopoly choisi
    """
    def __displayChoixDuMonopoly(self):
        choixMonopoly = ChoixMonopoly()
        selectedDataMonopoly = choixMonopoly.getSelectedMonopoly();

        if(selectedDataMonopoly == None):
            self.wait_window(choixMonopoly)
            selectedDataMonopoly = choixMonopoly.getSelectedMonopoly();

            # Si même après avoir attendu on a toujours un Monopoly vide
            if(selectedDataMonopoly == None):
                print("[WARNING] Aucun Monopoly n'a été choisi.")
                return None

        if(DEBUG):
            print("[DEBUG] Monopoly sélectionné: " + selectedDataMonopoly.getNom())

        return selectedDataMonopoly


    """
        Permet de choisir les paramètres qui seront utilisé pour modéliser le Monopoly
    """
    def __choixParametres(self, event = None):
        # self._choixParametres = Parametres(self._selectedDataMonopoly)
        self._choixParametres = Parametres_2(self._selectedDataMonopoly)
        # self.wait_window(self._choixParametres)
        if(self._selectedDataMonopoly != None):
            self.__refrechMonopolyData()


    """
        Permet d'appliqué les choix fait lors du paramétrage sur le Monopoly
    """
    def __applyParamOnDataMonopoly(self):
        nbrDes = self._choixParametres.getNbrDeDes()
        nbrMaxTourPrison = self._choixParametres.getNbrTourMaxPrison()
        probSortirPrison = self._choixParametres.getProbPayerSortirPrison()
        nbrDeDoublePrison = self._choixParametres.getNbrDeDoublePrison()
        print((nbrDes,nbrMaxTourPrison,probSortirPrison,nbrDeDoublePrison))

        # nbrDes = 0
        # nbrMaxTourPrison = 2
        # probSortirPrison = 0.5
        # nbrDeDoublePrison = 2

        if(DEBUG):
            print("[DEBUG] Paramètres: nombre de dés: " + str(nbrDes))
            print("[DEBUG] Paramètres: nombre max de tour en prison: " + str(nbrMaxTourPrison))
            print("[DEBUG] Paramètres: probabilité de payer pour sortir de prison: " + \
                str(probSortirPrison))
            print("[DEBUG] Paramètres: nombre de double avant d'aller en prison: " + \
                str(nbrDeDoublePrison))

        if(nbrDes != None):
            self._selectedDataMonopoly.setNbrDeDes(nbrDes)
        if(nbrMaxTourPrison != None):
            self._selectedDataMonopoly.setMaxTourPrison(nbrMaxTourPrison)
        if(probSortirPrison != None):
            self._selectedDataMonopoly.setProbSortirPrison(probSortirPrison)
        if(nbrDeDoublePrison != None):
            self._selectedDataMonopoly.setNbrDeDoublePrison(nbrDeDoublePrison)


    """
        Permet de mettre à jour le graphique en fonction du nombre de tour choisi

        @param pointFixe permet de savoir si on veut mettre à jour le graphique en fonction des 
            probabilité après une "infinité" de tour (c'est à dire lorsqu'il n'y a plus de variation
            des états)
    """
    def updateNewTour(self, pointFixe = False):
        nbrTour = self._nbrTourFrame.getNbrTourASimuler()

        if(pointFixe):
            newData = self._selectedMonopoly.simulerInfini()
            if(DEBUG):
                print("[DEBUG] Simulation des points fixe")

        else:
            if(DEBUG):
                print("[DEBUG] Simulation de " + str(nbrTour))

            newData = self._selectedMonopoly.simulerDesTours(nbrTour)
            newData = self._selectedMonopoly.getResultatSimulation()

        newData = self.__sumSameCase(newData)
        self._dataSimulation = newData
        self._statFrame.updateCanvas(self._dataSimulation)
        if(self._listStatistique != None):
            self._listStatistique.updateData(self._dataSimulation)


    """
        Permet d'additionné la probabilité de tomber sur deux cases ayant le même ID.  Il s'agit
        des cases "dupliqué" pour permettre de prendre en compte la règle de triples doubles

        @param listeCase dictionnaire contenant en clef les cases et en valeur la probabilitéde 
            s'y trouver
        @return un dictionnaire (identique à celui passé en entré) mais en ayant retiré les doublons
    """
    def __sumSameCase(self, listeCase):
        if(VIEW_ALL_CASE_DOUBLE):
            res = listeCase
        else:
            res = OrderedDict()
            saveIndexCase = {}

            for case in listeCase:
                probabilite = listeCase[case]
                position = case.getPosition()

                if(position in saveIndexCase):
                    res[saveIndexCase[position]] += probabilite

                else:
                    res[case] = probabilite
                    saveIndexCase[position] = case

        return res

    """
        Permet de mettre à jour l'affichage des statistiques en fonction des paramètres et du 
        Monopoly choisi
    """
    def __refrechMonopolyData(self):
        self.__applyParamOnDataMonopoly()
        self._selectedMonopoly = Monopoly(self._selectedDataMonopoly)
        if(self._nbrTourFrame != None):
            self.updateNewTour()

        if(self._viewParam != None):
            self._viewParam.setNewMonopolyData(self._selectedDataMonopoly)

        if(self._markovFrame != None):
            self._markovFrame.updateAll(self._selectedDataMonopoly.getListeCases(), \
                                        self._selectedDataMonopoly.getNbrDeDouble(), \
                                        self._selectedMonopoly.getMatriceDeplacement())

        if(self._listStatistique != None):
            self._listStatistique.updateData(self._dataSimulation)


        self.__refreshScroll()

    def __refreshScroll(self):
        self.after(100, lambda: scrollTk.updateScroll(self))


    def __viewListStats(self, event = None):
        self._listStatistique = ListeStatistiques(self._dataSimulation)
        self.wait_window(self._listStatistique)
        self._listStatistique = None

    def __viewHelp(self, event = None):
        help = Help()
        self.wait_window(help)
