import praw
from classes.Document import Document 
from classes.Author import Author
from classes.Corpus import Corpus
from classes.Document import RedditDocument, ArxivDocument
import datetime 
import pandas as pd 
import urllib.request
import xmltodict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
#===========================  Document ===========
# ============================= chargement de données reddit en instanciant un objet document
reddit = praw.Reddit(client_id='_jjmAvQmLvyPWeH7mSTYrw', client_secret='j7vF0wxXN9VuvOrIri3dt3W4fSvH4w', user_agent='td3')
theme = 'Football'
subr = reddit.subreddit(theme)

#textes_Reddit = []
collection = []

# Utilisez la fonction dir() pour voir tous les champs de l'objet subr
#print(dir(subr))
limit=10
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
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=10'
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

#============EXPLOITATIO?=========================
# Enlever les doublons en se basant sur tout le contenu
seen_documents = set()
unique_collection = []

for doc in collection:
    doc_tuple = (doc.titre, doc.auteur, doc.date, doc.texte, doc.type)
    if doc_tuple not in seen_documents:
        seen_documents.add(doc_tuple)
        unique_collection.append(doc)

# Garder uniquement les documents avec plus de 200 caractères dans le texte
filtered_collection = [doc for doc in unique_collection if len(doc.texte) > 200]

# Afficher le nombre de documents avant et après le nettoyage
print(f"Nombre de documents avant le nettoyage : {len(collection)}")
print(f"Nombre de documents après le nettoyage : {len(filtered_collection)}")

# Réaffecter la liste filtrée à votre collection
collection = filtered_collection


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
        doc.type = "Reddit"
    else:
        doc.type = "Arxiv"
    # Ajouter l'objet à votre corpus ou effectuer toute autre opération nécessaire
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
#del(mon_corpus)
# Chargez le corpus depuis un fichier CSV
mon_corpus.load('corpus.csv')
print(repr(mon_corpus))


#===================================================Test de notre singleton 
#corpus1 = Corpus("Corpus1")
#corpus2 = Corpus("Corpus2")
#corpus3 = Corpus("Corpus3")

#print(corpus1 is corpus2 is corpus3)

#============================================Test de search 
# Créer une instance de Corpus
moncorpus = Corpus('test')

# Ajouter quelques documents
#doc1 = Document("Titre 1", "Auteur 1", "2022/01/01", "URL 1", "Texte du document 1", "Type 1")
#doc2 = Document("Titre 2", "Auteur 2", "2022/01/02", "URL 2", "Texte du document 2", "Type 2")
#moncorpus.add(doc1)
#moncorpus.add(doc2)

# Effectuer une recherche avec un mot-clé
#keyword = "document"
#resultats = mon_corpus.search(keyword)

# Afficher les résultats
#for doc_id, passage in resultats.items():
    #print(f"Document ID: {doc_id}")
    #print(f"Passage: {passage}\n")

#============================Test Concord 
# Créer une instance de la classe Corpus et ajouter quelques documents
#doc1 = Document("Titre 1", "Auteur 1", "2022/01/01", "URL 1", "Ceci est un exemple de texte contenant le mot recherché.")
#doc2 = Document("Titre 2", "Auteur 2", "2022/01/02", "URL 2", "Un autre exemple de texte avec le mot recherché.")
#moncorpus.add(doc1)
#moncorpus.add(doc2)

# Appeler la méthode concorde avec une expression régulière
#results = moncorpus.concorde(r'\bmot\b', context_size=20)

# Afficher les résultats
#for i in range(len(results['contexte_gauche'])):
 #   print(f"Contexte Gauche: {results['contexte_gauche'][i]}")
  #  print(f"Motif Trouvé: {results['motif_trouve'][i]}")
   # print(f"Contexte Droit: {results['contexte_droit'][i]}")
    #print("=" * 50)
# ============================== test stat===========
mon_corpus = Corpus('test')

# Ajout de quelques documents à mon_corpus
doc1 = Document("Title 1", "Author 1", "2023/01/01", "URL1", "The present study focused on the effects of trunk extensor muscles fatigue onpostural control during quiet standing under different somatosensory conditionsfrom the foot and the ankle. With this aim, 20 young healthy adults were askedto stand as immobile as possible in two conditions of No fatigue and Fatigue oftrunk extensor muscles. In Experiment 1 (n = 10), somatosensation from the footand the ankle was degraded by standing on a foam surface. In Experiment 2 (n =10), somatosensation from the foot and ankle was facilitated through theincreased cutaneous feedback at the foot and ankle provided by strips ofathletic tape applied across both ankle joints. The centre of foot pressuredisplacements (CoP) were recorded using a force platform. The results showedthat (1) trunk extensor muscles fatigue increased CoP displacements undernormal somatosensatory conditions (Experiment 1 and Experiment 2), (2) thisdestabilizing effect was exacerbated when somatosensation from the foot and theankle was degraded (Experiment 1), and (3) this destabilizing effect wasmitigated when somatosensation from the foot and the ankle was facilitated(Experiment 2). Altogether, the present findings evidenced re-weighting ofsensory cues for controlling posture during quiet standing following trunkextensor muscles fatigue by increasing the reliance on the somatosensory inputsfrom the foot and the ankle. This could have implications in clinical andrehabilitative areas")
doc2 = Document("Title 2", "Author 2", "2023/02/02", "URL2", "We propose a novel method for fitting planar B-spline curves to unorganizeddata points. In traditional methods, optimization of control points and footpoints are performed in two very time-consuming steps in each iteration: 1)control points are updated by setting up and solving a linear system ofequations; and 2) foot points are computed by projecting each data point onto aB-spline curve. Our method uses the L-BFGS optimization method to optimizecontrol points and foot points simultaneously and therefore it does not need toperform either matrix computation or foot point projection in every iteration.As a result, our method is much faster than existing methods.")
doc3 = Document("Title 3", "Author 3", "2023/03/03", "URL3", "In this paper we are interested to the zygodactyly phenomenon in birds, andin particolar in parrots. This arrangement, common in species living on trees,is a distribution of the foot with two toes facing forward and two back. Wegive a model for the foot, and thanks to the methods of iterated functionsystem we are able to describe the reachability set. Moreover we give anecessary and sufficient condition for the grasping problem. Finally weintroduce a hybrid dynamical system modeling owl's foot in various stages ofhunting (flying, attack, grasp")

mon_corpus.add(doc1)
mon_corpus.add(doc2)
mon_corpus.add(doc3)

# Appel de la méthode stats
mon_corpus.stats()




# Appel de la méthode stats
# Afficher le vocabulaire



mon_corpus.construire_mat_tfidf()
vocab = mon_corpus.get_vocabulaire()
print(vocab)

#===============================Moteur de recherche test
#================================Methode sarch
mots_clefs_utilisateur = 'example of special ' #demand eà l'utilisateur de mettre un mot 
 #nettoie les mots clées 
passages = mon_corpus.search(mots_clefs_utilisateur)

for doc_id, passage in passages.items():
    document = mon_corpus.id2doc[doc_id]
    print(f"Document ID: {doc_id}")
    print(f"Auteur: {document.auteur}")
    print(f"Titre: {document.titre}")
    print(f"Passage: {passage}")
    print("\n")
#keyword = "document"
#resultats = mon_corpus.search(keyword)

# Afficher les résultats
#for doc_id, passage in resultats.items():
    #print(f"Document ID: {doc_id}")
    #print(f"Passage: {passage}\n")
# Methode recherche cosinus 
mots_clefs_utilisateur = 'cumulative footpressure images as a biometric.' #demand eà l'utilisateur de mettre un mot 
 #transforme les mots cles en vecteur vecteur_requete = np.zeros(len(self.vocabulaire))
vecteur_requete = np.zeros(len(vocab))

mots_clefs_propres = mon_corpus.nettoyer_texte(mots_clefs_utilisateur)
for mot in mots_clefs_propres.split():
    if mot in vocab:
        mot_id = vocab[mot]['id'] - 1
        vecteur_requete[mot_id] += 1

#calcule la similarité6


mat_tfidf = mon_corpus.get_mattdidf()
similarites = cosine_similarity([vecteur_requete], mat_tfidf)

indices_tries = np.argsort(similarites[0])[::-1]
top_n = 5
id2doc = mon_corpus.get_id2doc()
print(id2doc)
for i in range(top_n):
    indice_document = indices_tries[i]
    score_similarite = similarites[0, indice_document]
    
    # Assurez-vous que l'indice est décalé de 1 pour correspondre à votre indexation
    indice_document += 1

    document = id2doc[indice_document]

    print(f"Score de similarité avec le document {document.titre} : {score_similarite}")
    print(f"Contenu du document : {document.texte}")
    print("\n")