# Etude du Monopoly via les chaînes de Markov
Ce projet comporte un rapport écrit décrivant les chaînes de Markov, la modélisation
du Monopoly à travers des chaînes de Markov et également les résultats obtenus grâce à ce
programme.

### Structure des fichiers
[![Folder](http://findicons.com/files/icons/1156/fugue/16/folder_horizontal_open.png) **App**](App)            
L'application permettant de simuler l'évolution du monopoly.

[![Folder](http://findicons.com/files/icons/1156/fugue/16/folder_horizontal_open.png) **Rapport**](Rapport)            
Dossier contenant tous les fichiers permettant de générer le rapport.

[![Folder](http://findicons.com/files/icons/1156/fugue/16/folder_horizontal_open.png) **Ressource**](Ressource)            
Tous les documents (exclus donc ceux directement consulté sur internet) utilisé comme réference 
pour la réalisation de ce projet (les autres références se trouvent dans le rapport).

### Dépendances

**Python**               
Pour que le projet `Python` fonctionne il faut posséder la libraire `Tkinter` et également `numpy`
utilisé respectivement pour l'interface graphique et les calculs matriciels.


### Compliation
Seul le `LaTeX` doit être compilé.  Il est possible de le faire via le [`Makefile`](Makefile) et la commande
suivante:
```
make rapport
```

### Utilisation de l'application
Pour lancer l'application il suffit de faire la commande suivante
```
App/python3 main.py
```

