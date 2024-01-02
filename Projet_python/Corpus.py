# Correction de G. Poux-Médard, 2021-2022
from collections import Counter

from Author import Author
import re
import pandas as pd

# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    _instance = None  # Variable de classe pour stocker l'unique instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
            # Initialisation du corpus uniquement si c'est la première instance
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    # Méthode pour nettoyer le texte
    @staticmethod
    def nettoyer_texte(texte):
        # Mise en minuscules
        texte = texte.lower()

        # Remplacement des retours à la ligne
        texte = texte.replace("\n", " ")

        # Remplacement des ponctuations et chiffres par des espaces
        texte = re.sub(r'[^\w\s]', ' ', texte)

        # Supprimer les espaces en double
        texte = ' '.join(texte.split())

        return texte

    # Méthode STATS
    def stats(self, n_mots_frequents=10):
        mots_corpus = " ".join([self.nettoyer_texte(doc.texte) for doc in self.id2doc.values()]).split()
        mots_differents = set(mots_corpus)

        # Ajout de déclarations print pour le débogage
        print(f"Texte brut du corpus: {' '.join([doc.texte for doc in self.id2doc.values()])}")
        print(f"Texte nettoyé du corpus: {' '.join([self.nettoyer_texte(doc.texte) for doc in self.id2doc.values()])}")

        # Afficher le nombre de mots différents dans le corpus
        print(f"Nombre de mots différents dans le corpus : {len(mots_differents)}")

        # Afficher les n mots les plus fréquents
        mots_frequents = Counter(mots_corpus).most_common(n_mots_frequents)
        print(f"\nLes {n_mots_frequents} mots les plus fréquents dans le corpus :")
        for mot, freq in mots_frequents:
            print(f"{mot}: {freq}")

    # Méthode SEARCH
    def search(self, keyword):
        passages = {}

        # Concaténer l'intégralité des chaînes de caractères
        full_text = " ".join([doc.texte for doc in self.id2doc.values()])

        # Utiliser la bibliothèque re pour trouver les passages
        matches = re.finditer(keyword, full_text, flags=re.IGNORECASE)

        for match in matches:
            for doc_id, document in self.id2doc.items():
                if match.start() < len(document.texte):
                    passages[doc_id] = document.texte[
                                       max(0, match.start() - 50):min(len(document.texte), match.end() + 50)]

        return passages

    # Méthode CONCORDE
    def concorde(self, keyword, context_size=50):
        data = {'contexte_gauche': [], 'motif_trouve': [], 'contexte_droit': []}

        # Concaténer l'intégralité des chaînes de caractères
        full_text = " ".join([doc.texte for doc in self.id2doc.values()])

        # Utiliser la bibliothèque re pour trouver les passages
        matches = re.finditer(keyword, full_text, flags=re.IGNORECASE)

        for match in matches:
            for doc_id, document in self.id2doc.items():
                if match.start() < len(document.texte):
                    start_context = max(0, match.start() - context_size)
                    end_context = min(len(document.texte), match.end() + context_size)

                    left_context = document.texte[start_context:match.start()]
                    right_context = document.texte[match.end():end_context]

                    data['contexte_gauche'].append(left_context)
                    data['motif_trouve'].append(document.texte[match.start():match.end()])
                    data['contexte_droit'].append(right_context)

        return pd.DataFrame(data)

    # =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
