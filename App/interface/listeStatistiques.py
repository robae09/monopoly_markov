#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

from operator import itemgetter
# from math import round

from interface.scrollTopFrame import scrollTopFrame


"""
    Permet de montrer les statistiques sous forme de liste ordonné en fonction des probabilités
"""
class ListeStatistiques(scrollTopFrame):

    COLOR_WIDTH = 50
    COLOR_HEIGHT = COLOR_WIDTH
    TITLE_STYLE = "Arial 11 bold"

    INDEX_COL = {"Couleur": 0, "Case": 1, "ProbaVisiter": 2, "PrixAchat": 3, "LocationVide": 4,
                "RatioVide": 5, "RevenuParTourVide": 6, "NbrRentabVide": 7, 
                "LocationHotel": 8, "RatioHotel": 9, "RevenuParTourHotel": 10, "NbrRentabHotel": 11}


    def __init__(self, listeCases):
        scrollTopFrame.__init__(self, width=1300, background="gray")
        self.title("Liste statistiques")
        
        self._listeCases = listeCases

        self.__initAllWidgets()
        self.__initEvent()
        self.__refreshScroll()


    def __initAllWidgets(self):
        self.__addCouleur()
        self.__addCasesName()
        self.__addProbaVisiter()
        self.__addPrixAchat()
        self.__addLocationVide()
        self.__addRatioVide()
        self.__addRevenuTourVideAndNbrRenta()
        self.__addLocationHotel()
        self.__addRatioHotel()
        self.__addRevenuTourHotelAndNbrRenta()

    """
        Permet de supprimer tous les widgets se trouvant sur la fenêtre principale
    """
    def __destroyAllWidget(self):
        for widget in self.getMainFrame().winfo_children():
            widget.destroy()


    def updateData(self, newListeCases):
        self._listeCases = newListeCases
        self.__destroyAllWidget()
        self.__initAllWidgets()

    """
        Permet d'initialiser les events
    """
    def __initEvent(self):
        self.bind("<Escape>", self.__closeStats)


    """
        Permet de récupérer les cases une a une afin de faire une boucle dans un ordre bien précis

        @return un "generator" (yield) retournant l'index actuelle et la case
    """
    def __getGeneratorCases(self):
        i = 0
        for case in sorted(self._listeCases, key=self._listeCases.get, reverse=True):
            i += 1
            yield i, case


    """
        Permet d'ajouter la couleur des cases
    """
    def __addCouleur(self):
        tk.Label(self.getMainFrame(), text="Couleur", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["Couleur"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            canvas = tk.Canvas(self.getMainFrame(), width=ListeStatistiques.COLOR_WIDTH, \
                            height=ListeStatistiques.COLOR_HEIGHT, background=case.getCouleur())
            canvas.grid(column=ListeStatistiques.INDEX_COL["Couleur"], row=row, sticky="nsew", padx=1, pady=1)

    """
        Permet d'ajouter le nom des cases
    """
    def __addCasesName(self):
        tk.Label(self.getMainFrame(), text="Case", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["Case"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            tk.Label(self.getMainFrame(), text=case.getNom()).grid(column=ListeStatistiques.INDEX_COL["Case"], \
                    row=row, sticky="nsew", padx=1, pady=1)


    """
        Ajoute la probabilité qu'une case soit visitée
    """
    def __addProbaVisiter(self):
        tk.Label(self.getMainFrame(), text="Probabilité\nde visiter", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["ProbaVisiter"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            strPourcent = self.__formatBigNumber(self._listeCases[case]*100)
            tk.Label(self.getMainFrame(), text=strPourcent + " %").grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["ProbaVisiter"], padx=1, pady=1)

    """
        Permet d'ajouter le prix d'achat
    """
    def __addPrixAchat(self):
        tk.Label(self.getMainFrame(), text="Prix achat", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["PrixAchat"], sticky="nsew",padx=(1, 3), pady=2)

        for row, case in self.__getGeneratorCases():
            strPrix = "-" if case.getPrix() <= 0 else (str(self.__formatBigNumber(case.getPrix())) + " $")
            tk.Label(self.getMainFrame(), text=strPrix, foreground="red").grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["PrixAchat"], padx=(1, 3), pady=1)

    """
        Permet d'ajouter le prix de location de la case vide
    """
    def __addLocationVide(self):
        tk.Label(self.getMainFrame(), text="Location\nvide", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["LocationVide"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            strGainVide = "-" if case.getGainVide() <= 0 else (self.__formatBigNumber(case.getGainVide()) + " $")
            tk.Label(self.getMainFrame(), text=strGainVide, foreground="green").grid(row=row, \
                    column=ListeStatistiques.INDEX_COL["LocationVide"], sticky="nsew", padx=1, pady=1)

    """
        Permet d'ajouter le ratio entre le prix et le gain lorsque la case est vide
    """
    def __addRatioVide(self):
        tk.Label(self.getMainFrame(), text="Ratio Prix/\nRentabilité\nvide", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["RatioVide"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            strRatioVide = "-"
            if(case.getRatioPrixGainVide() > 0):
                strRatioVide = self.__formatBigNumber(case.getRatioPrixGainVide())

            tk.Label(self.getMainFrame(), text=strRatioVide).grid(column=ListeStatistiques.INDEX_COL["RatioVide"], \
                    row=row, sticky="nsew", padx=1, pady=1)

    """
        Permet d'ajouter le revenu espéré lors d'un tour adverse si la case est vide et le nombre de
        tour où un adversaire tombe sur cette case pour rentabiliser l'achat
    """
    def __addRevenuTourVideAndNbrRenta(self):
        tk.Label(self.getMainFrame(), text="Revenu espéré\npar tour (vide)", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["RevenuParTourVide"], sticky="nsew", padx=1, pady=2)

        tk.Label(self.getMainFrame(), text="Nombre de tour\npour rentabiliser\n(vide)", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["NbrRentabVide"], sticky="nsew", padx=(1, 3), pady=2)

        for row, case in self.__getGeneratorCases():
            revenuParTourVide = 0 if case.getGainVide() <= 0 else case.getGainVide()*self._listeCases[case]

            strRevenuEspereParTourVide = "-" if revenuParTourVide <= 0 else (self.__formatBigNumber(revenuParTourVide) + " $")
            tk.Label(self.getMainFrame(), text=strRevenuEspereParTourVide).grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["RevenuParTourVide"], padx=1, pady=1)

            strNbrTourRentaVide = "-" if revenuParTourVide <= 0 else self.__formatBigNumber(case.getPrix()/revenuParTourVide)
            tk.Label(self.getMainFrame(), text=strNbrTourRentaVide).grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["NbrRentabVide"], padx=(1, 3), pady=1)

    """
        Permet d'ajouter le prix de la location d'une case contenant un hotel
    """
    def __addLocationHotel(self):
        tk.Label(self.getMainFrame(), text="Location\nhotel", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["LocationHotel"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            strGainHotel = "-" if case.getGainHotel() <= 0 else (self.__formatBigNumber(case.getGainHotel()) + " $")
            tk.Label(self.getMainFrame(), text=strGainHotel, foreground="green").grid(row=row, \
                    column=ListeStatistiques.INDEX_COL["LocationHotel"], sticky="nsew", padx=1, pady=1)

    """
        Permet d'ajouter le ratio entre le prix et le gain lorsque la case contient un hotel (en 
            prennant en compte le prix d'achat des appartements et hotel)
    """
    def __addRatioHotel(self):
        tk.Label(self.getMainFrame(), text="Ratio Prix/\nRentabilité\nhotel", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["RatioHotel"], sticky="nsew", padx=1, pady=2)

        for row, case in self.__getGeneratorCases():
            strRatioHotel = "-"
            if(case.getRatioPrixGainHotel() > 0):
                strRatioHotel = self.__formatBigNumber(case.getRatioPrixGainHotel())
            tk.Label(self.getMainFrame(), text=strRatioHotel).grid(column=ListeStatistiques.INDEX_COL["RatioHotel"], \
                    row=row, sticky="nsew", padx=1, pady=1)

    """
        Permet d'ajouter le revenu espéré lors d'un tour adverse si la case contient un hotel et le nombre de
        tour où un adversaire tombe sur cette case pour rentabiliser l'achat
    """
    def __addRevenuTourHotelAndNbrRenta(self):
        tk.Label(self.getMainFrame(), text="Revenu espéré\npar tour (hotel)", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["RevenuParTourHotel"], sticky="nsew", padx=1, pady=2)

        tk.Label(self.getMainFrame(), text="Nombre de tour\npour rentabiliser\n(hotel)", font=ListeStatistiques.TITLE_STYLE).grid(row=0, \
                column=ListeStatistiques.INDEX_COL["NbrRentabHotel"], sticky="nsew", padx=(1, 3), pady=2)

        for row, case in self.__getGeneratorCases():
            revenuParTourHotel = 0 if case.getGainHotel() <= 0 else case.getGainHotel()*self._listeCases[case]
            strRevenuEspereParTourHotel = "-" if revenuParTourHotel <= 0 else (self.__formatBigNumber(revenuParTourHotel) + " $")
            tk.Label(self.getMainFrame(), text=strRevenuEspereParTourHotel).grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["RevenuParTourHotel"], padx=1, pady=1)

            strNbrTourRentaHotel = "-" if revenuParTourHotel <= 0 else self.__formatBigNumber(case.getPrixHotel()/revenuParTourHotel)
            tk.Label(self.getMainFrame(), text=strNbrTourRentaHotel).grid(row=row, sticky="nsew", \
                    column=ListeStatistiques.INDEX_COL["NbrRentabHotel"], padx=(1, 3), pady=1)


    """
        Permet de rajouter des espaces pour les grands nombres

        @param number le nombre à transformer
        @return un String avec le bon format
    """
    def __formatBigNumber(self, number):
        return '{:,}'.format(round(number, 3)).replace(',', ' ')



    """
        Fonction appellé lorsque l'on veut fermer la fenêtre
    """
    def __closeStats(self, event = None):
        self.quit()
        self.destroy()

    def __refreshScroll(self):
        self.after(100, lambda: scrollTopFrame.updateScroll(self))
