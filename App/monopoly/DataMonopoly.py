# -*- coding: utf-8 -*-
from monopoly.Case import *
from monopoly.CaseChance import CaseChance
from monopoly.CaseCommunaute import CaseCommunaute
from monopoly.CaseGoToPrison import CaseGoToPrison
from monopoly.CasePrison import CasePrison
from copy import deepcopy


# Liste de tous les DataMonopoly
_allDataMonopoly = []


"""
    Class permettant de stocker et récupérer des inforamtions sur un monopoly
"""
class DataMonopoly:

    """
        Permet d'initiliser les informations.

        @param nom des informations monopoly (permettant de le retrouver et de l'identifier)
        @param displayNom nom à afficher
        @param listCase liste (dans l'ordre) des cases (la case départ est ajoutée automatiquement)
    """
    def __init__(self, nom, displayNom, listCase):
        self._nom = nom
        self._displayNom = displayNom
        self._defaultListCase = listCase
        self._nbrCaseClassique = -1     # Nombre de case "normal" du monopoly

        _allDataMonopoly.append(self)


    """
        Permet d'initialiser correctement un Monopoly et de créé a proprement parlé
        l'ensemble des cases où le joueur peut aller
    """
    def initMonopoly(self):
        self._listCase = self.__initAllCases(0)

        # Initialisation des cases prisons
        self._nbrCaseClassique = len(self._listCase)
        self._listCase += self.__initPrisonCases()

        # Règle des triples doubles
        for i in range(self.getNbrDeDouble()-1):
            self._listCase += self.__initAllCases(i+1)


    """
        Permet d'initialiser toutes les cases d'un plateau

        @param nombreDeDouble le nombre de double pour pouvoir atteindre les cases que l'on est
            entrain de créer
    """
    def __initAllCases(self, nombreDeDouble):
        res = [getCaseDepart()] + deepcopy(self._defaultListCase)

        for case in res:
            case.setNbrDeDouble(nombreDeDouble)

        return res


    """
        Permet d'initialiser le nombre de case prison nécessaire

        @return une liste de case prison en fonction des paramètres (définit plus tôt)
    """
    def __initPrisonCases(self):
        return [CasePrison(self._nbrCaseClassique, i) for i in range(self._maxTourPrison)]


    """
        Permet de récupérer le nom des informations monopoly

        @return le nom
    """
    def getNom(self):
        return self._nom


    """
        Permet de récupérer le nom à afficher concernant ces informations monopoly

        @return le nom à afficher
    """
    def getDisplayNom(self):
        return self._displayNom


    """
        Permet de récupérer une case en fonction de son numéro sur le plateau

        @param numeroCase le numero de la case à récupérer
        @param nbrDoubleDe le nombre de double que le joueur à du faire pour arriver à cette case
            (facultatif: 0 par défaut)
        @return la case (ou None si pas trouvé)
    """
    def getCase(self, numeroCase, nbrDoubleDe = 0):
        numeroCase = numeroCase % self._nbrCaseClassique # On fait en sorte que ça ne dépasse pas du plateau
        return self.__getExactCase(numeroCase, nbrDoubleDe)


    """
        Permet de récupérer un numero de case très précis.  Aucune vérification n'est faite

        @param numeroCase le numero de case à récupérer
        @param nbrDoubleDe nombre de double des qu'aura du faire le joueur pour atteindre cette case
            (facultatif: 0 par défaut)
        @return la case (ou None si pas trouvé)
    """
    def __getExactCase(self, numeroCase, nbrDoubleDe = 0):
        for case in self._listCase:
            if(case.getPosition() == numeroCase and case.getNbrDeDouble() == nbrDoubleDe):
                return case
        return None


    """
        Permet de récupérer la case prison (celle correspondant au premier tour du joueur)

        @return la Case prison correspondant au premier tour
    """
    def getCasePrison(self, nbrTourEnPrison = 0):
        return self.__getExactCase(self._nbrCaseClassique+nbrTourEnPrison)


    """
        Permet de récupérer la case "prison visite uniquement"

        @return la case "prison visite uniquement"
    """
    def getPrisonVisiteUniquement(self):
        return self.getCase(CASE_PRISON_VISITE_SIMPLE)


    """
        Permet de récupérer toutes les cases du monopoly

        @return la liste des cases
    """
    def getListeCases(self):
        return self._listCase


    ##### Définition des paramètres pouvant changé la configuration du monpoly #####

    def getMaxTourPrison(self):
        return self._maxTourPrison

    def setMaxTourPrison(self, nbrMaxTour):
        self._maxTourPrison = nbrMaxTour

    def getNbrDeDes(self):
        return self._nbrDeDes

    def setNbrDeDes(self, nbrDeDes):
        self._nbrDeDes = nbrDeDes

    def getProbSortirPrison(self):
        return self._probSortirPrison

    def setProbSortirPrison(self, probSortirPrison):
        self._probSortirPrison = probSortirPrison

    def getNbrDeDouble(self):
        return self._nbrDeDoublePrison

    def setNbrDeDoublePrison(self, nbrDeDouble):
        self._nbrDeDoublePrison = nbrDeDouble


############################ STATIC ############################

"""
    Permet de récupérer un "DataMonopoly" en fonction de son nom

    @param nom du monopoly que l'on cherche
    @return le DataMonopoly ou None si pas trouvé
"""
def getDataMonopoly(nom):
    for data in _allDataMonopoly:
        if(data.getNom() == nom):
            return data
    return None

"""
    Permet de récupérer tous les Monopoly disponibles

    @return une liste avec tous les noms des monopoly
"""
def getAllDataMonopoly():
    res = []
    for data in _allDataMonopoly:
        res.append(data)
    return res



############################ Initialisation ############################

# Couleur en Tkinter: http://wiki.tcl.tk/37701
# nom, position, couleur = "white", prix = 0

DataMonopoly("MONOPOLY_70", "Monopoly édition 70è anniversaire", [
    Case("Wavre Rue du commerce", 1, "sienna", prix=600000, gainVide=20000, gainHotel=2500000, prixAppartement=500000, prixHotel=500000), 
    CaseCommunaute(2),
    Case("Aalst Niewstraat", 3, "sienna", prix=600000, gainVide=40000, gainHotel=4500000, prixAppartement=500000, prixHotel=500000),
    Case("Impôts sur le revenu", 4, "firebrick4", prix=2000000, vendre=False),
    Case("Aéroport de Bruxelles Zaventem", 5, "lavender", prix=2000000, gainVide=250000),
    Case("Sint-truiden Luiderstraat", 6, "dodger blue", prix=1000000, gainVide=60000, gainHotel=5500000, prixAppartement=500000, prixHotel=500000),
    CaseChance(7),
    Case("Verviers place Verte", 8, "dodger blue", prix=1000000, gainVide=60000, gainHotel=5500000, prixAppartement=500000, prixHotel=500000),
    Case("Mechelen Bruul", 9, "dodger blue", prix=1200000, gainVide=80000, gainHotel=6000000, prixAppartement=500000, prixHotel=500000),
    Case("Prison simple visite", 10),
    Case("Arlon Grand'Rue", 11, "hot pink", prix=1400000, gainVide=100000, gainHotel=7500000, prixAppartement=1000000, prixHotel=1000000),
    Case("Telecoms", 12, "ivory", prix=1500000), # TODO dépend du nombre du dé
    Case("Kortrijk Lange SteenStraat", 13, "hot pink", prix=1400000, gainVide=100000, gainHotel=7500000, prixAppartement=1000000, prixHotel=1000000),
    Case("Mons Grand Rue", 14, "hot pink", prix=1600000, gainVide=120000, gainHotel=9000000, prixAppartement=1000000, prixHotel=1000000),
    Case("Aéroport de Charleroi", 15, "lavender", prix=2000000, gainVide=250000),
    Case("Oostende Kapellestraat", 16, "dark orange", prix=1800000, gainVide=140000, gainHotel=9500000, prixAppartement=1000000, prixHotel=1000000),
    CaseCommunaute(17),
    Case("Leuven Bondgenotenlaan", 18, "dark orange", prix=1800000, gainVide=140000, gainHotel=9500000, prixAppartement=1000000, prixHotel=1000000),
    Case("Knokke Lippenslaan", 19, "dark orange", prix=2000000, gainVide=160000, gainHotel=10000000, prixAppartement=1000000, prixHotel=1000000),
    Case("Parking", 20, "white", vendre=False),
    Case("Charleroi Rue de la Montagne", 21, "orange red", prix=2200000, gainVide=180000, gainHotel=10500000, prixAppartement=1500000, prixHotel=1500000),
    CaseChance(22),
    Case("Liège Rue de la Cathédrale", 23, "orange red", prix=2200000, gainVide=180000, gainHotel=10500000, prixAppartement=1500000, prixHotel=1500000),
    Case("Antwerpen Huidevetterstraat", 24, "orange red", prix=2400000, gainVide=200000, gainHotel=11000000, prixAppartement=1500000, prixHotel=1500000),
    Case("Aéroport de Liège", 25, "lavender", prix=2000000, gainVide=250000),
    Case("Hasselet Hoogstraat", 26, "gold", prix=2600000, gainVide=220000, gainHotel=11500000, prixAppartement=1500000, prixHotel=1500000),
    Case("Brugge Steenstraat", 27, "gold", prix=2600000, gainVide=220000, gainHotel=11500000, prixAppartement=1500000, prixHotel=1500000),
    Case("Internet", 28, "ivory", prix=1500000), # TODO dépend du nombre du dé
    Case("Namur Rue de Fer", 29, "gold", prix=2800000, gainVide=240000, gainHotel=12000000, prixAppartement=1500000, prixHotel=1500000),
    CaseGoToPrison(30),
    Case("Bruxelles Av. Louise", 31, "sea green", prix=3000000, gainVide=260000, gainHotel=12750000, prixAppartement=2000000, prixHotel=2000000),
    Case("Liège Pont d'Île", 32, "sea green", prix=3000000, gainVide=260000, gainHotel=12750000, prixAppartement=2000000, prixHotel=2000000),
    CaseCommunaute(33),
    Case("Gent Veldstraat", 34, "sea green", prix=3200000, gainVide=280000, gainHotel=14000000, prixAppartement=2000000, prixHotel=2000000),
    Case("Luchthaven Antwerpen", 35, "lavender", prix=2000000, gainVide=250000),
    CaseChance(36),
    Case("Antwerpen Meir", 37, "dark slate blue", prix=3500000, gainVide=350000, gainHotel=15000000, prixAppartement=2000000, prixHotel=2000000),
    Case("Taxe de Luxe", 38, "firebrick4", prix=1000000, vendre=False),
    Case("Bruxelles Rue Neuve", 39, "dark slate blue", prix=4000000, gainVide=500000, gainHotel=20000000, prixAppartement=2000000, prixHotel=2000000)
    ])

DataMonopoly("MERVEILLES_MONDE", "Monopoly Merveilles du monde", [
    Case("Les Chutes du Niagara", 1, "orchid", 60), 
    CaseCommunaute(2),
    Case("L'Everest", 3, "orchid", 60),
    Case("Assurance Voyage", 4, "firebrick4", 200, vendre=False),
    Case("Amsterdam Schiphol", 5, "lavender", 200),
    Case("La Grande Barrière de Corail", 6, "deep sky blue", 100),
    CaseChance(7),
    Case("Le Grand Canyon", 8, "deep sky blue", 100),
    Case("Les chutes Angel", 9, "deep sky blue", 120),
    Case("Prison simple visite", 10, "white", 0),
    Case("Le Christ Rédempteur", 11, "dark orchid", 140),
    Case("Bureau de Change", 12, "ivory", 150),
    Case("La Tour Eiffel", 13, "dark orchid", 140),
    Case("Le Colisée", 14, "dark orchid", 160),
    Case("Paris Charles de Gaulle", 15, "lavender", 200),
    Case("Les ruines de Stonehenge", 16, "dark orange", 180),
    CaseCommunaute(17),
    Case("Le Taj Mahal", 18, "dark orange", 180),
    Case("Les statues Moai", 19, "dark orange", 200),
    Case("Parking", 20, "white", vendre=False),
    Case("Machu Picchu", 21, "orange red", 220),
    CaseChance(22),
    Case("Le temple Angkor Wat", 23, "orange red", 220),
    Case("Pétra", 24, "orange red", 240),
    Case("Rhein-Main Frankfurt", 25, "lavender", 200),
    Case("La grande Muraille de Chine", 26, "gold", 260),
    Case("Le phare d'Alexandrie", 27, "gold", 260),
    Case("Agent de voyages", 28, "ivory", 150),
    Case("Le colosse de Rhodes", 29, "gold", 280),
    CaseGoToPrison(30),
    Case("Le mausolée, Halicarnasse", 31, "sea green", 300),
    Case("La statue de Zeus, Olympie", 32, "sea green", 300),
    CaseCommunaute(33),
    Case("Le temple d'Artémis à Ephèse", 34, "sea green", 320),
    Case("London Heathrow", 35, "lavender", 200),
    CaseChance(36),
    Case("Jardins suspendus de Babylone", 37, "dark slate blue", 350),
    Case("Taxe de Luxe", 38, "firebrick4", 100, vendre=False),
    Case("La grande Pyramide de Gizeh", 39, "dark slate blue", 400)
    ])

DataMonopoly("MONDE_2006", "Monopoly Coupe du monde 2006", [
    Case("Australie", 1, "orchid", 60), 
    CaseCommunaute(2),
    Case("Suisse", 3, "orchid", 60),
    Case("Carton Rouge", 4, "firebrick4", 200, vendre=False),
    Case("Olympiastadium", 5, "lavender", 200),
    Case("Corée du sud", 6, "deep sky blue", 100),
    CaseChance(7),
    Case("Tunisie", 8, "deep sky blue", 100),
    Case("Pologne", 9, "deep sky blue", 120),
    Case("Prison simple visite", 10, "white", 0),
    Case("Costa Rica", 11, "violet red", 140),
    Case("Distribution de boissons", 12, "ivory", 150),
    Case("Croatie", 13, "violet red", 140),
    Case("Iran", 14, "violet red", 160),
    Case("Fritz-Walter-Stadion", 15, "lavender", 200),
    Case("Alemagne", 16, "dark orange", 180),
    CaseCommunaute(17),
    Case("Japon", 18, "dark orange", 180),
    Case("Suède", 19, "dark orange", 200),
    Case("Parking", 20, "white", vendre=False),
    Case("Italie", 21, "orange red", 220),
    CaseChance(22),
    Case("Portugal", 23, "orange red", 220),
    Case("Angleterre", 24, "orange red", 240),
    Case("Zentralstadion", 25, "lavender", 200),
    Case("USA", 26, "gold", 260),
    Case("Mexique", 27, "gold", 260),
    Case("Compagnie d'éclairage", 28, "ivory", 150),
    Case("Espagne", 29, "gold", 280),
    CaseGoToPrison(30),
    Case("France", 31, "sea green", 300),
    Case("Argentine", 32, "sea green", 300),
    CaseCommunaute(33),
    Case("Pays-Bas", 34, "sea green", 320),
    Case("Frankenstadion", 35, "lavender", 200),
    CaseChance(36),
    Case("République Tchèque", 37, "dark slate blue", 350),
    Case("Carton jaune", 38, "firebrick4", 100, vendre=False),
    Case("Brésil", 39, "dark slate blue", 400)
    ])

DataMonopoly("STAR_WARS_2", "Monopoly Star Wars (ep 2)", [
    Case("Palais royal", 1, "orchid", 60), 
    CaseCommunaute(2),
    Case("Retraite au bord du lac", 3, "orchid", 60),
    Case("Dégat d'astéroïde", 4, "firebrick4", 200, vendre=False),
    Case("Speeder de Zam Wesell", 5, "lavender", 200),
    Case("Bureau de Palpatine", 6, "deep sky blue", 100),
    CaseChance(7),
    Case("Bibliothèque Jedi", 8, "deep sky blue", 100),
    Case("Temple Jedi", 9, "deep sky blue", 120),
    Case("Prison simple visite", 10, "white", 0),
    Case("Hangar de Speders", 11, "violet red", 140),
    Case("Sabre laser", 12, "ivory", 150),
    Case("Nightclub Coruscant", 13, "violet red", 140),
    Case("Zone de Chargement", 14, "violet red", 160),
    Case("Slave 1", 15, "lavender", 200),
    Case("Ferme de Cliegg Lars", 16, "dark orange", 180),
    CaseCommunaute(17),
    Case("Plaine Désertiques", 18, "dark orange", 180),
    Case("Camp de Jawa", 19, "dark orange", 200),
    Case("Parking", 20, "white", vendre=False),
    Case("Kamino", 21, "orange red", 220),
    CaseChance(22),
    Case("Plateforme d'Atterrissage", 23, "orange red", 220),
    Case("Entraînement de Clones", 24, "orange red", 240),
    Case("Starfighter Jedi", 25, "lavender", 200),
    Case("Cellule d'Obi-Wan", 26, "gold", 260),
    Case("Production de Droïde de combat", 27, "gold", 260),
    Case("Telekinésie", 28, "ivory", 150),
    Case("Chaîne de Production droïde", 29, "gold", 280),
    CaseGoToPrison(30),
    Case("Arène d'exécution", 31, "sea green", 300),
    Case("Loge pour VIP Géonosiens", 32, "sea green", 300),
    CaseCommunaute(33),
    Case("Suite secrète", 34, "sea green", 320),
    Case("Canonnière de République", 35, "lavender", 200),
    CaseChance(36),
    Case("Armée de Droïde de combat", 37, "dark slate blue", 350),
    Case("Homme des sables", 38, "firebrick4", 100, vendre=False),
    Case("Armée Clone", 39, "dark slate blue", 400)
    ])

DataMonopoly("MONOPOLY_PDS", "Monopoly Printemps des Sciences", [
    Case("Gdynia", 1, "saddle brown", 60), 
    CaseCommunaute(2),
    Case("Taipei", 3, "saddle brown", 60),
    Case("impôts sur le revenu", 4, "firebrick4", 200, vendre=False),
    Case("Compagnie ferroviaire", 5, "lavender", 200),
    Case("Tokyo", 6, "light sky blue", 100),
    CaseChance(7),
    Case("Barcelone", 8, "light sky blue", 100),
    Case("Athènes", 9, "light sky blue", 120),
    Case("Prison simple visite", 10, "white", 0),
    Case("Istanbul", 11, "deep pink", 140),
    Case("Energie solaire", 12, "ivory", 150),
    Case("Kyiv", 13, "deep pink", 140),
    Case("Toronto", 14, "deep pink", 160),
    Case("Compagnie aérienne", 15, "lavender", 200),
    Case("Rome", 16, "dark orange", 180),
    CaseCommunaute(17),
    Case("Shanghai", 18, "dark orange", 180),
    Case("Vancouver", 19, "dark orange", 200),
    Case("Parking", 20, "white", vendre=False),
    Case("Sydney", 21, "red", 220),
    CaseChance(22),
    Case("New York", 23, "red", 220),
    Case("Londres", 24, "red", 240),
    Case("Compagnie maritime", 25, "lavender", 200),
    Case("Beijing", 26, "gold", 260),
    Case("Hong Kong", 27, "gold", 260),
    Case("Energie éolienne", 28, "ivory", 150),
    Case("Jérusalem", 29, "gold", 280),
    CaseGoToPrison(30),
    Case("Paris", 31, "sea green", 300),
    Case("Belgrade", 32, "sea green", 300),
    CaseCommunaute(33),
    Case("Le Cap", 34, "sea green", 320),
    Case("Compagnie spatiale", 35, "lavender", 200),
    CaseChance(36),
    Case("Riga", 37, "dark slate blue", 350),
    Case("Taxe de Luxe", 38, "firebrick4", 100, vendre=False),
    Case("Montréal", 39, "dark slate blue", 400)
    ])