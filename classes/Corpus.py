from classes.Author import Author
from classes.Document import Document
from scipy.sparse import lil_matrix, csr_matrix
import numpy as np
import re
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')
# =============== 2.7 : CLASSE CORPUS ===============
class Corpus:
    def __init__(self, nom):
        # Attributs de la classe Corpus
        self.nom = nom  # Le nom du corpus
        self.authors = {}  # Dictionnaire des auteurs
        self.aut2id = {}  # Dictionnaire d'index des auteurs
        self.id2doc = {}  # Dictionnaire d'index des documents
        self.ndoc = 0  # Comptage des documents
        self.naut = 0  # Comptage des auteurs
     
        # Attribut de classe pour stocker la chaîne construite
        Corpus.full_text = None
        # Dictionnaire pour stocker les informations sur le vocabulaire
        self.vocabulaire = {}
        self.mat_tf = None
        self.mat_tfidf = None

    def get_vocabulaire(self):
        return self.vocabulaire
  
    def get_mattdidf(self):
        return self.mat_tfidf
    
    def get_id2doc(self):
        return self.id2doc
    
    def get_aut2id(self):
        return self.aut2id

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
        data = {'ID': [], 'Titre': [], 'Auteur': [], 'Date': [], 'URL': [], 'Texte': [], 'Type': []}
        for doc_id, doc in self.id2doc.items():
            data['ID'].append(doc_id)
            data['Titre'].append(doc.titre)
            data['Auteur'].append(doc.auteur)
            data['Date'].append(doc.date)
            data['URL'].append(doc.url)
            data['Texte'].append(doc.texte)
            data['Type'].append(doc.type)


        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)


    # =============== 3.4 : LOAD ===============
    def load(self, filename='corpus.csv'):
        # Charger le corpus depuis un fichier CSV
        df = pd.read_csv(filename)

        # Supprimer les doublons basés sur les colpreproconnes spécifiées
        df = df.drop_duplicates(subset=['Titre', 'Auteur', 'Date','URL', 'Texte','Type'])

        # Supprimer les lignes avec un texte de moins de 200 caractères
        df = df[df['Texte'].apply(lambda x: len(str(x)) >= 200)]
        print(len(df))

        for i, row in df.iterrows():
            doc = Document(row['Titre'], row['Auteur'], row['Date'],row['URL'], row['Texte'],row['Type'])
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


## ===Methode search 
    
    
    def search(self, keyword):
        passages = {}

        # Vérifier si la chaîne a déjà été construite
        if Corpus.full_text is None:
            # Construire la chaîne en concaténant l'intégralité des textes
            Corpus.full_text = " ".join([doc.texte for doc in self.id2doc.values()])

        # Utiliser la bibliothèque re pour trouver les passages
        matches = re.finditer(keyword, Corpus.full_text, flags=re.IGNORECASE)

        for match in matches:
            for doc_id, document in self.id2doc.items():
                if match.start() < len(document.texte
                                       ):
                    debut_passage = max(0, match.start() - 50)
                    fin_passage = min(len(document.texte), match.end() + 50)
                    passage = document.texte[debut_passage:fin_passage]
                    passages[doc_id] = passage

        return passages
    
    # Méthode CONCORDE
    def concorde(self, keyword, context_size=50):
        data = {'contexte_gauche': [], 'motif_trouve': [], 'contexte_droit': []}


       # Vérifier si la chaîne a déjà été construite
        if Corpus.full_text is None:
            # Construire la chaîne en concaténant l'intégralité des textes
            Corpus.full_text = " ".join([doc.texte for doc in self.id2doc.values()])

        # Utiliser la bibliothèque re pour trouver les passages
        matches = re.finditer(keyword, Corpus.full_text, flags=re.IGNORECASE)

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
    
    # Méthode pour nettoyer le texte
   # Import des modules nécessaires
    def nettoyer_texte(self,texte):
        texte = str(texte)
        # Mise en minuscules
        texte = texte.lower()

        # Remplacement des retours à la ligne
        texte = texte.replace("\n", " ")
        # Suppression des chiffres
        texte = re.sub(r'\d', ' ', texte)

        # Utilisation de regex pour supprimer les caractères non alphabétiques et les chiffres
        texte = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ\s]', ' ', texte)

        # Remplacement des ponctuations et chiffres par des espaces
        texte = re.sub(r'[^\w\s]', ' ', texte)

        # Supprimer les espaces en double
        texte = ' '.join(texte.split())

        # Enlever les stop words
        stop_words = set(stopwords.words('english'))
        mots = texte.split()
        
        mots = [mot for mot in mots if mot not in stop_words] 
        mots = [mot for mot in mots if len(mot) >= 2] 

        

        # Rejoindre les mots sans stop words en une chaîne
        texte_propre = ' '.join(mots)


        return texte_propre
        

    # Méthode STATS
    def stats(self, n_mots_frequents=30):
        # Construction du vocabulaire
        self.full_text = " ".join([doc.texte for doc in self.id2doc.values()])
        self.full_text=self.nettoyer_texte(self.full_text)
        
        # Supprimer les doublons et trier en ordre alphabétique
        mots_uniques = sorted(self.full_text.split())

        # Utilisation de Counter pour compter les occurrences
        freq_mots = Counter(mots_uniques)

        # Ajout des informations au vocabulaire
        for mot, freq in freq_mots.items():
            # Si le mot n'est pas déjà présent dans le vocabulaire, l'ajouter
            if mot not in self.vocabulaire:
                self.vocabulaire[mot] = {'id': len(self.vocabulaire) + 1}

            # Ajouter les informations de fréquence
            self.vocabulaire[mot]['occurrences'] = freq
            self.vocabulaire[mot]['doc_frequency'] = sum(mot in doc.texte for doc in self.id2doc.values())

        # Conversion du dictionnaire en DataFrame Pandas
        df_freq = pd.DataFrame(list(freq_mots.items()), columns=['Mot', 'Occurences'])

        # Ajout de la colonne de fréquence documentaire
        df_freq['Doc Frequency'] = df_freq['Mot'].apply(lambda mot: self.vocabulaire[mot]['doc_frequency'])

        # Affichage des résultats
        print(df_freq.head(n_mots_frequents))
        
    #Methode stat auteur
    def statistiques_auteur(self,nom_auteur):
        if nom_auteur in self.aut2id:
            id_auteur =  self.aut2id[nom_auteur]
            auteur = self.authors[id_auteur]

            nombre_documents = len(auteur.production)
            taille_moyenne_documents = sum(len(doc) for doc in auteur.production) / nombre_documents

            print(f"\nStatistiques pour l'auteur {nom_auteur}:")
            print(f"Nombre de documents produits : {nombre_documents}")
            print(f"Taille moyenne des documents : {taille_moyenne_documents:.2f} caractères\n")
        else:
            print(f"L'auteur {nom_auteur} n'est pas connu dans la collection.\n")


    #MATRICE TF

    def construire_mat_tf(self):
        # Vérifier si le vocabulaire a été construit
        if not self.vocabulaire:
            self.stats()

        # Nombre de documents et de mots dans le vocabulaire
        nb_documents = len(self.id2doc)
        nb_mots = len(self.vocabulaire)

        # Initialiser la matrice LIL à zéro
        mat_lil = lil_matrix((nb_documents, nb_mots), dtype=np.float64)

        # Créer un dictionnaire pour mapper les identifiants de document aux indices de ligne
        doc_id_to_row = {doc_id: i for i, doc_id in enumerate(self.id2doc)}

        # Remplir la matrice LIL avec les occurrences de mots dans chaque document
        for doc_id, document in self.id2doc.items():
            row_index = doc_id_to_row[doc_id]
            for mot, info in self.vocabulaire.items():
                mot_id = info['id']
                occurrences = document.texte.lower().split().count(mot)
                mat_lil[row_index, mot_id - 1] = occurrences  # -1 car les indices commencent à 0

        # Convertir la matrice LIL en matrice CSR
        self.mat_tf = csr_matrix(mat_lil)

        # Calculer le nombre total d'occurrences de chaque mot dans le corpus
        total_occurrences_par_mot = self.mat_tf.sum(axis=0)

        # Calculer le nombre total de documents contenant chaque mot
        documents_contenant_mot = self.mat_tf.astype(bool).sum(axis=0)

        # Mettre à jour les informations dans le vocabulaire
        for mot, info in self.vocabulaire.items():
            mot_id = info['id']
            info['total_occurrences'] = total_occurrences_par_mot[0, mot_id - 1]
            info['total_documents_contenant'] = documents_contenant_mot[0, mot_id - 1]

        return self.mat_tf
        

    #MATRICE TF-IDF
    def construire_mat_tfidf(self):
        # Vérifier si la matrice TF a été construite
        if self.mat_tf is None:
            self.construire_mat_tf()

        # Nombre total de documents dans le corpus
        nb_documents = len(self.id2doc)

        # Calculer la Matrice IDF
        idf = np.zeros(len(self.vocabulaire))
        for mot, info in self.vocabulaire.items():
            doc_frequency = info['doc_frequency']
            idf[info['id'] - 1] = np.log(nb_documents / (1 + doc_frequency))

        # Initialiser la matrice LIL à zéro
        mat_lil_tfidf = lil_matrix(self.mat_tf.shape, dtype=np.float64)

        # Multiplication de la matrice TF par les valeurs IDF
        mat_lil_tfidf[:, :] = self.mat_tf.multiply(idf)

        # Convertir la matrice LIL en matrice CSR
        self.mat_tfidf = mat_lil_tfidf.tocsr()

         # Calculer le nombre total d'occurrences de chaque mot dans le corpus
        total_occurrences_par_mot = self.mat_tfidf.sum(axis=0)

        # Calculer le nombre total de documents contenant chaque mot
        documents_contenant_mot = self.mat_tfidf.astype(bool).sum(axis=0)

        # Mettre à jour les informations dans le vocabulaire
        for mot, info in self.vocabulaire.items():
            mot_id = info['id']
            info['total_occurrences'] = total_occurrences_par_mot[0, mot_id - 1]
            info['total_documents_contenant'] = documents_contenant_mot[0, mot_id - 1]


        return self.mat_tfidf
   