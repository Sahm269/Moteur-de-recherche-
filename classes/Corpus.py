# Correction de G. Poux-Médard, 2021-2022
from classes.Author import Author
from classes.Document import Document
import pandas as pd
# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:

    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
            # Initialisation du corpus uniquement si c'est la première instance
            cls._instance.__init__(*args, **kwargs)
        return cls._instance
    
    def __init__(self, nom):
        # Attributs de la classe Corpus
        self.nom = nom  # Le nom du corpus
        self.authors = {}  # Dictionnaire des auteurs
        self.aut2id = {}  # Dictionnaire d'index des auteurs
        self.id2doc = {}  # Dictionnaire d'index des documents
        self.ndoc = 0  # Comptage des documents
        self.naut = 0  # Comptage des auteurs

    def add(self, doc):
        # Ajouter un document au corpus
        if doc.auteur not in self.aut2id:
            # Si l'auteur n'est pas encore dans le corpus, l'ajouter
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        # Ajouter le texte du document à l'auteur correspondant
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        # Ajouter le document au corpus
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

     # =============== 3.3 : SAVE ===============
    def save(self, filename='corpus.csv'):
        # Sauvegarder le corpus dans un fichier CSV
        data = {'ID': [], 'Titre': [], 'Auteur': [], 'Date': [], 'Texte': [], 'Type' : []}
        for doc_id, doc in self.id2doc.items():
            data['ID'].append(doc_id)
            data['Titre'].append(doc.titre)
            data['Auteur'].append(doc.auteur)
            data['Date'].append(doc.date)
            data['Texte'].append(doc.texte)
            data['Type'].append(doc.type)

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    # =============== 3.4 : LOAD ===============
    def load(self, filename='corpus.csv'):
        # Charger le corpus depuis un fichier CSV
        df = pd.read_csv(filename)
        for i, row in df.iterrows():
            doc = Document(row['Titre'], row['Auteur'], row['Date'], row['Texte'], row['Type'])
            self.add(doc)

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        # Afficher les éléments du corpus triés par titre ou date
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique par titre
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri chronologique par date
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]


        # Afficher la représentation des documents
        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        # Représentation du corpus (utilisée par print)
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
