import praw
from classes.Document import Document 
from classes.Author import Author
from classes.Corpus import Corpus
from classes.Document import RedditDocument, ArxivDocument
import datetime 
import pandas as pd 
import urllib.request
import xmltodict
#===========================  Document ===========
# ============================= chargement de données reddit en instanciant un objet document
reddit = praw.Reddit(client_id='_jjmAvQmLvyPWeH7mSTYrw', client_secret='j7vF0wxXN9VuvOrIri3dt3W4fSvH4w', user_agent='td3')
theme = 'Football'
subr = reddit.subreddit(theme)

#textes_Reddit = []
collection = []

# Utilisez la fonction dir() pour voir tous les champs de l'objet subr
#print(dir(subr))
limit=0
for doc in subr.controversial(limit=limit):
    titre = doc.title.replace("\n", '')
    auteur = str(doc.author)
    date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
    url = "https://www.reddit.com/"+doc.permalink
    texte = doc.selftext.replace("\n", "")

    doc_class = Document(titre, auteur, date, url, texte)
    collection.append(doc_class)

# ...

#==========================chargement des données Arxiv en instanciant un objet docyment
#textes_arxiv=[]
query = "foot"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

# url_read est un "byte stream" qui a besoin d'être décodé
data =  url_read.decode()

dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
docs = dico['feed']['entry']
for doc in docs:
    titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
    try:
        authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
    except:
        authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
    summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
    date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

    doc_class = Document(titre, authors, date, doc["id"], summary)  # Création du Document
    collection.append(doc_class)  # Ajout du Document à la liste.

#print(len(collection))
#del(collection)


# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc

print(id2doc)


##=========================== Partie 2 Author  ========
# ===============  : DICT AUTEURS ===============
authors = {}
id2aut = {}

num_auteurs_vus = 0
# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in id2aut:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        id2aut[doc.auteur] = num_auteurs_vus
    authors[id2aut[doc.auteur]].add(doc.texte)
print(id2aut)


#================ code necessaire pour afficher les stat d'un auteur  
def statistiques_auteur():
    nom_auteur = input("Entrez le nom de l'auteur : ")

    if nom_auteur in id2aut:
        id_auteur = id2aut[nom_auteur]
        auteur = authors[id_auteur]

        nombre_documents = len(auteur.production)
        taille_moyenne_documents = sum(len(doc) for doc in auteur.production) / nombre_documents

        print(f"\nStatistiques pour l'auteur {nom_auteur}:")
        print(f"Nombre de documents produits : {nombre_documents}")
        print(f"Taille moyenne des documents : {taille_moyenne_documents:.2f} caractères\n")
    else:
        print(f"L'auteur {nom_auteur} n'est pas connu dans la collection.\n")

# Appel de la fonction
#statistiques_auteur()


###=================================  Classe corpus   =======================
#del(mon_corpus)
####====================== test des classes filles documents
# Création du corpus
mon_corpus = Corpus(nom="Corpus_article")
# Ajoutez les documents à l instance de Corpus
for doc in collection:
    if "reddit" in doc.url.lower():
        # Créer un objet RedditDocument en utilisant les propriétés du document actuel
        reddit_doc = RedditDocument(
            titre=doc.titre,
            auteur=doc.auteur,
            date=doc.date,
            url=doc.url,
            texte=doc.texte,
            #num_comments=doc.num_comments
        )
        doc.type = "Reddit"
        
        mon_corpus.add(doc)
        # Ajouter l'objet à votre corpus ou effectuer toute autre opération nécessaire
    else:
        # Créer un objet ArxivDocument en utilisant les propriétés du document actuel
        arxiv_doc = ArxivDocument(
            titre=doc.titre,
            auteurs=doc.auteur,
            date=doc.date,
            url=doc.url,
            texte=doc.texte,
            
        )
        doc.type = "Arxiv"
        mon_corpus.add(doc)

# Taille du corpus 
taille_corpus = mon_corpus.ndoc
print(f"Taille du corpus : {taille_corpus} documents")

# Affichage du corpus
mon_corpus.show()


#========================Créez un DataFrame à partir des objets Document ===================
# Créez une instance de la classe Corpus
mon_corpus = Corpus(nom="Corpus_article")

# Sauvegardez le corpus dans un fichier CSV
mon_corpus.save("corpus.csv")

# Chargez le corpus depuis un fichier CSV
mon_corpus.load('corpus.csv')
print(repr(mon_corpus ))

#Test de notre singleton 
#corpus1 = Corpus("Corpus1")
#corpus2 = Corpus("Corpus2")
#corpus3 = Corpus("Corpus3")

#print(corpus1 is corpus2 is corpus3)
