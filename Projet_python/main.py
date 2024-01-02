
# =============== PARTIE 1 =============
# =============== 1.1 : REDDIT ===============
# Library
import praw

# Fonction affichage hiérarchie dict
def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-"*i, k)
                recursivePrint(d[k], i+2)
            else:
                print("-"*i, k, ":", d[k])
    recursivePrint(d, 1)

# Identification
reddit = praw.Reddit(client_id='fn27HawSFmbzFu4QYVflJg', client_secret='dMhZaFsap7Gx2x8PCgmO5DTBtyyo1w', user_agent='MAARIR YASMINE')

# Requête
limit = 100
hot_posts = reddit.subreddit('all').hot(limit=limit)#.top("all", limit=limit)#

# Récupération du texte
docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):
    if i%10==0: print("Reddit:", i, "/", limit)
    if afficher_cles:  # Pour connaître les différentes variables et leur contenu
        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)

    if post.selftext != "":  # Osef des posts sans texte
        pass
        #print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))

#print(docs)

# =============== 1.2 : ArXiv ===============
# Libraries
import urllib, urllib.request
import xmltodict

# Paramètres
query_terms = ["clustering", "Dirichlet"]
max_results = 50

# Requête
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

#showDictStruct(data)

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"].get("entry", [])):
    if i % 10 == 0:
        print("ArXiv:", i, "/", limit)
    docs.append(entry.get("summary", "").replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))
    #showDictStruct(entry)

# =============== 1.3 : Exploitation ===============
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print(f"# docs sans doublons : {len(docs)}")

for i, doc in enumerate(docs):
    print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)

# =============== PARTIE 2 =============
# =============== 2.1, 2.2 : CLASSE DOCUMENT ===============
from Document import Document

# =============== 2.3 : MANIPS ===============
import datetime
collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

        doc_classe = Document(titre, authors, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(titre, auteur, date, url, texte)

        collection.append(doc_classe)

# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

# =============== 2.4, 2.5 : CLASSE AUTEURS ===============
from Author import Author

# =============== 2.6 : DICT AUTEURS ===============
authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)

# =============== 2.7, 2.8 : CORPUS ===============
from Corpus import Corpus
corpus = Corpus("Mon corpus")

# Construction du corpus à partir des documents
for doc in collection:
    corpus.add(doc)
#corpus.show(tri="abc")
#print(repr(corpus))
import pandas as pd
 # =============== 2.2 : Construction du Vocabulaire ===============
# Créez un ensemble vide pour stocker le vocabulaire
vocabulaire = set()

# Bouclez sur les documents de votre corpus
for doc in collection:
    print(f"Processing document: {doc.titre}")
    print(f"Texte du document ({doc.titre}): {doc.texte}")
    # Divisez le texte en mots en utilisant la fonction split
    mots = doc.texte.split()

    # Ajoutez les mots à l'ensemble du vocabulaire
    vocabulaire.update(mots)

# Le vocabulaire est maintenant stocké dans l'ensemble 'vocabulaire'
# Vous pouvez convertir l'ensemble en liste si vous avez besoin d'indices spécifiques pour chaque mot
liste_vocabulaire = list(vocabulaire)

# Affichez le vocabulaire
print("liste de vocabulaire",liste_vocabulaire)
import pandas as pd



import pandas as pd

# =============== 2.3 : Comptage des occurrences de chaque mot ===============
# Créer un dictionnaire pour stocker les fréquences de chaque mot
freq_dict = {mot: 0 for mot in liste_vocabulaire}

# Boucler sur les documents de votre corpus
for doc in collection:
    print(f"Processing document: {doc.titre}")
    print(f"Texte du document ({doc.titre}): {doc.texte}")
    # Diviser le texte en mots en utilisant la fonction split
    mots = doc.texte.split()

    # Mettre à jour les fréquences dans le dictionnaire
    for mot in mots:
        freq_dict[mot] += 1

# Convertir le dictionnaire en DataFrame pandas
df_freq = pd.DataFrame(list(freq_dict.items()), columns=['Mot', 'Fréquence'])

# =============== 2.4 : Nombre de documents contenant chaque mot ===============
# Ajouter une colonne 'Nombre de documents' initialisée à zéro
df_freq['Nombre de documents'] = 0

# Boucler sur les documents de votre corpus
for doc in collection:
    # Diviser le texte en mots en utilisant la fonction split
    mots = doc.texte.split()

    # Mettre à jour le nombre de documents dans lequel chaque mot apparaît
    for mot in set(mots):
        df_freq.loc[df_freq['Mot'] == mot, 'Nombre de documents'] += 1

# Afficher le DataFrame mis à jour
print("Le DataFrame mis à jour :", df_freq)

# =============== 2.9 : SAUVEGARDE ===============
import pickle

# Ouverture d'un fichier, puis écriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# La variable est réapparue
print(corpus)

# Importez les classes RedditDocument et ArxivDocument si ce n'est pas déjà fait
from Document import RedditDocument
from Document import ArxivDocument

# Création d'instances de RedditDocument et ArxivDocument
reddit_doc = RedditDocument("Titre Reddit", "Auteur Reddit", "2023/11/30", "https://reddit.com", "Texte Reddit", 42)
arxiv_doc = ArxivDocument("Titre ArXiv", "Auteur ArXiv", "2023/11/30", "https://arxiv.org", "Résumé ArXiv", ["Co-Auteur1", "Co-Auteur2"])

# Ajout au corpus
corpus.add(reddit_doc)
corpus.add(arxiv_doc)

# Affichage du corpus
corpus.show(tri="abc")


print(repr(corpus))


# Appel de la méthode stats
corpus.stats(n_mots_frequents=10)


# Création du vocabulaire à partir des documents
vocabulaire = set()
for doc in collection:
    mots = doc.texte.split()
    vocabulaire.update(mots)

# Retirer les doublons et trier par ordre alphabétique
vocabulaire = sorted(list(vocabulaire))

# Construction du dictionnaire vocab
vocab = {}
for i, mot in enumerate(vocabulaire):
    vocab[mot] = {'Identifiant': i + 1, 'NombreOccurrences': 0}

# Bouclez sur les documents de votre corpus
for doc in collection:
    # Diviser le texte en mots en utilisant la fonction split
    mots = doc.texte.split()

    # Mettre à jour les occurrences dans le dictionnaire vocab
    for mot in mots:
        vocab[mot]['NombreOccurrences'] += 1

# Afficher le dictionnaire vocab mis à jour
print("Dictionnaire vocab mis à jour :", vocab)



from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix



# =============== 1.2 : Construction de la matrice TF ===============
# Créez une instance de CountVectorizer avec le vocabulaire
vectorizer = CountVectorizer(vocabulary=vocabulaire)

# Appliquez la transformation sur les documents pour obtenir la matrice d'occurrences des mots
tf_matrix = vectorizer.fit_transform([doc.texte for doc in collection])

# Convertissez la matrice en une sparse.csr_matrix
matTF = csr_matrix(tf_matrix)

# Affichez la matrice TF si nécessaire
print("Matrice TF :\n", matTF)

# =============1.3 : Calculer le nombre total d'occurrences de chaque mot dans le corpus ==========================
occurrences_totales = matTF.sum(axis=0)

# Mettre à jour le dictionnaire vocab avec le nombre total d'occurrences et le nombre total de documents
for mot, info in vocab.items():
    info['NombreOccurrencesTotales'] = occurrences_totales[0, info['Identifiant'] - 1]
    info['NombreDocumentsAvecMot'] = (matTF[:, info['Identifiant'] - 1] > 0).sum()

# Afficher le dictionnaire vocab mis à jour
print("Dictionnaire vocab mis à jour :", vocab)

from sklearn.feature_extraction.text import TfidfTransformer

# =============== 1.4 : Construction de la matrice TF-IDF ===============
# Pour créez une instance de TfidfTransformer
tfidf_transformer = TfidfTransformer()

# Pour apliquez la transformation sur la matrice TF pour obtenir la matrice TF-IDF
tfidf_matrix = tfidf_transformer.fit_transform(tf_matrix)

# Convertissez la matrice en une sparse.csr_matrix
matTFIDF = csr_matrix(tfidf_matrix)

# Affichage de la matrice TF-IDF si nécessaire
print("Matrice TF-IDF :\n", matTFIDF)







