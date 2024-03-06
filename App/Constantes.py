# -*- coding: utf-8 -*-

# Afficher ou non les messages de DEBUG
# Type: Boolean
DEBUG = True

# Les cartes prisons n'existent pas physiquement. On leur attribue donc un ID fixé à partir de
# cette valeur
# Type: int
DECALAGE_PRISON = 1000


# La règle permettant d'envoyer un joueur faisant 3 doubles consécutifs nécessite la duplication du
# plateau de jeu.  On décalle les cases de se second plateau de jeu en fonction de la valeur suivante
# Type: int
DECALAGE_PLATEAU = 100


# Permet de définir à partir de combien de double on se retrouve automatiquement en prison
# Type: int
NOMBRE_DOUBLE = 3


# Le numero de la case "prison visible simple".  Il s'agit dans tous les jeux monopoly de la 10ème
# case du plateau
# Type: int
CASE_PRISON_VISITE_SIMPLE = 10


# Permet d'indiquer si on veut afficher ou non les cases créé pour gérer les triples doubles
# (si masqué, les valeurs iront simplement s'additionner aux autres)
# /!\ Surtout utilisé pour le débug ! (affichage pas génial quand)
# Type: boolean
VIEW_ALL_CASE_DOUBLE = False
