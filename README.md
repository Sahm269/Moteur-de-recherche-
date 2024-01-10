# Moteur-de-recherche-
## Bibliothèques utilisées
### Bibliothèques pour la construction de l'interface Dash
- import dash
- from dash import dcc
- from dash import html
- from dash.dependencies import Input, Output, State
- import dash_core_components as dcc

### Bibliothèques pour la récupération de données
- import praw  
- import urllib.request
- import xmltodict 

### Bibliothèques pour le traitement du texte et la similarité cosinus
- from sklearn.metrics.pairwise import cosine_similarity
- from scipy.sparse import lil_matrix, csr_matrix
- import numpy as np
- import re
- import pandas as pd
- from nltk.corpus import stopwords
- import ipywidgets as widgets
- from IPython.display import display

### Classes personnalisées pour la modélisation des données
- from classes.Document import Document, RedditDocument, ArxivDocument
- from classes.Author import Author
- from classes.Corpus import Corpus

### Autres bibliothèques
- import datetime
- from collections import Counter
- import nltk

## Organisation des dossiers
Notre projet est structuré de manière claire et organisée, comprenant trois dossiers distincts et des fichiers racines définissant les points d'entrée principaux.

1. Dossiers :
   
- Classes : Contient les définitions des classes utilisées dans notre application, facilitant une gestion modulaire et ordonnée de notre code.
- Tests : Ce dossier regroupe les tests unitaires pour s'assurer du bon fonctionnement de nos classes et modules, contribuant ainsi à la robustesse de notre application.
- Assets : Destiné à stocker les fichiers CSS permettant une personnalisation esthétique de notre interface Dash.

2. Fichiers Racines :
- app.py : Le dossier principal pour l'interface Dash version 3. Il contient la logique et la configuration nécessaires pour l'exécution de l'application web.

- interface.ipynb : Le fichier principal pour l'interface notebook version 2. Il agit comme un notebook interactif pour les utilisateurs, permettant une exploration aisée des fonctionnalités de recherche.

- main.py : Bien que ce fichier soit actuellement inutilisé, il a servi initialement comme point d'entrée lors des premières phases de développement. Il a été conservé pour des raisons de traçabilité, même s'il n'est pas nécessaire à l'exécution du projet
main.py : il sert à rien, juste on avait commencer à travailler et tester avec ce fichier principale avant d'avoir tout interface.

## Modee d'emploie pour l'interface dash(app.py)
- Chargement initial du Corpus :
L'utilisateur entre dans le programme et lance l’application dash en exécutant la commande python app.py.
Le programme charge automatiquement le corpus existant à partir du fichier "corpus.csv" dans le dossier du programme.
Accès au Moteur de Recherche :
- L'utilisateur peut accéder directement au moteur de recherche depuis l'interface en cliquant sur le bouton “ accéder au moteur de recherche”.
Il saisit les mots-clés dans la barre de recherche . 
Exemple de mots clé à chercher : The best player oh the year, Neymar,  accurate , achieved, who is Zidane, balloon , penalty for Liverpool, the world cup, Haaland created chances. 
- Lancement de la Recherche :
L'utilisateur appuie sur le bouton "Rechercher" pour lancer la recherche basée sur les mots-clés saisis.
Le programme utilise la matrice TF-IDF pour calculer la similarité cosinus entre la requête et les documents du corpus. 

- Filtrage des Résultats par Source :
L'utilisateur peut utiliser la liste déroulante pour filtrer les résultats par source (Reddit, Arxiv).
Il doit appuyer à nouveau sur le bouton "Rechercher" pour appliquer le filtre.
- Suppression du Corpus Actuel :
L'utilisateur doit manuellement supprimer le corpus actuel en accédant au dossier du projet, puis peut charger un nouveau corpus via le formulaire en spécifiant les détails nécessaires
- Récupération des données  :
L'utilisateur utilise le formulaire pour saisir les informations de son propre corpus (titre, auteur, texte, etc.).
Après avoir rempli le formulaire, il clique sur le bouton "Récupérer Données" pour charger son propre corpus.
- Enregistrement du Nouveau Corpus :
Une fois les données récupérées, l'utilisateur peut enregistrer son nouveau corpus en cliquant sur le bouton "Enregistrer".
- Chargement du corpus : 
L’utilisateur doit charger le corpus en appuyant sur le bouton “ouvrir le corpus “ et le corpus sera chargé par le programme.
- Affichage des Données (repr) :
L'utilisateur peut choisir d'afficher les informations du corpus en utilisant la méthode __repr__ pour chaque document.
Cela peut être fait en appuyant sur le bouton "Afficher Données".
- Retour au Moteur de Recherche :
Après avoir exploré le corpus ou effectué des actions spécifiques, l'utilisateur peut revenir au moteur de recherche pour effectuer de nouvelles recherches ou explorer davantage les résultats.

- Exemple de mots clé à chercher :
  The best player of the year, Neymar,  accurate , achieved, who is Zidane, balloon , penalty for Liverpool, the world cup, Haaland created chances. 


## Mode d'emploi pour l'interface notebook (interface.ipynb)
il faut ouvrir le fichier notebook sur Jupiter Notebook.
1. Via les API :

Rendez-vous sur le formulaire de gestion des données.
Remplissez le formulaire avec les critères de votre choix pour récupérer dynamiquement les données depuis les API.
Cliquez sur "Recuperer les données". , vous pouvez l'enregistrer et il sera enregistrer au nom de corupus1.csv dans le dossier , vous pouvez ne pas l'enregitrer et continuer directement sur la recherche. vous pouvez afficher, le corpus.

2. À partir de Données Préexistantes :
Vous pouvez juste ouvir un corpus en en mettant le chemin du corpus exemple : "corpus.csv" va charger le chemin présent dans le dossier ensuite appuyer sur charger le corpus.
vous pouvez l'afficher pour voir son contenu. 

- Effectuer une Recherche :
Dans la  recherche dans le notebook interfac.ipynb.
Utilisez le champ dédié pour saisir les mots-clés que vous souhaitez rechercher.
Sélectionnez le nombre d'articles à afficher (topn) selon vos préférences.

- Lancer la Recherche :
Cliquez sur le bouton "Rechercher" pour lancer votre requête.
Patientez pendant que le moteur de recherche analyse les résultats.

- Explorer les Résultats :
Les résultats seront affichés par ordre de score de similarité.
Même si un document ne contient pas tous les mots-clés, il peut être pertinent en fonction du score.
Utilisez la barre de défilement pour parcourir tous les résultats.

- Effacer les Résultats :
Pour effacer les résultats actuels, cliquez une fois sur le bouton "Effacer".
Pour une réinitialisation complète, effectuez un double-clic sur le bouton "Effacer".

Conseils: 
pour tester les deux methodes n'oubliez pas de detruire l'instance créer (en utilsant del(corpus))
