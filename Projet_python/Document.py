

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte="", document_type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = document_type
    # =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tType : {self.type}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}, Source : {self.type}"

# =============== 2.3 : Classe fille RedditDocument ===============
class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", num_comments=0):
        # Appeler le constructeur de la classe mère
        super().__init__(titre, auteur, date, url, texte, document_type="Reddit")
        # Ajouter la variable spécifique à RedditDocument
        self.num_comments = num_comments

    # Accesseurs/mutateurs pour le champ spécifique à RedditDocument
    def get_num_comments(self):
        return self.num_comments

    def set_num_comments(self, num_comments):
        self.num_comments = num_comments

    # Méthode spécifique pour l'affichage de l'objet
    def __str__(self):
        # Appeler la méthode __str__ de la classe mère pour réutiliser le code
        return f"{super().__str__()}, Nombre de commentaires : {self.num_comments}"

# =============== 2.3 : La classe ArxivDocument ===============
class ArxivDocument(Document):
        # Initialisation des variables de la classe ArxivDocument
        def __init__(self, titre="", auteurs=None, date="", url="", texte="", co_auteurs=None):
            # Appel du constructeur de la classe mère
            super().__init__(titre, auteurs, date, url, texte, document_type="Arxiv")
            # Ajout de la nouvelle variable spécifique à ArxivDocument
            self.co_auteurs = co_auteurs if co_auteurs else []

        # Accesseurs/Mutateurs pour la variable co_auteurs
        def get_co_auteurs(self):
            return self.co_auteurs

        def set_co_auteurs(self, co_auteurs):
            self.co_auteurs = co_auteurs

        # Méthode spécifique pour afficher l'objet ArxivDocument
        def __str__(self):
            return f"{super().__str__()}, Co-auteurs : {', '.join(self.co_auteurs)}"


# Exemple d'utilisation
#reddit_doc = RedditDocument("Title1", "Author1", "2023-11-30", "http://example.com", "Text1", 50)
#print(reddit_doc)

#arxiv_doc = ArxivDocument(titre="Titre de l'article", auteurs=["Auteur1", "Auteur2"], date="2023-11-30", url="http://exemple.com", texte="Contenu de l'article", co_auteurs=["CoAuteur1", "CoAuteur2"])
#print(arxiv_doc)


from abc import ABC, abstractmethod
import datetime

# =============== 3.1 : CLASSE D'USINE ===============
class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self, **kwargs):
        pass

# =============== 3.2 : IMPLEMENTATION DE DOCUMENTFACTORY ===============
class RedditDocumentFactory(DocumentFactory):
    def create_document(self, titre="", auteur="", date="", url="", texte="", num_comments=0):
        return RedditDocument(titre, auteur, date, url, texte, num_comments)

class ArxivDocumentFactory(DocumentFactory):
    def create_document(self, titre="", auteurs=None, date="", url="", texte="", co_auteurs=None):
        return ArxivDocument(titre, auteurs, date, url, texte, co_auteurs)

# =============== 3.3 : UTILISATION DE L'USINE ===============
reddit_factory = RedditDocumentFactory()
arxiv_factory = ArxivDocumentFactory()

# Création d'instances de documents avec les usines
reddit_doc = reddit_factory.create_document(titre="Reddit Title", auteur="Reddit Author", date=datetime.datetime.now(), texte="Reddit Text", num_comments=42)
arxiv_doc = arxiv_factory.create_document(titre="ArXiv Title", auteurs=["ArXiv Author"], date=datetime.datetime.now(), texte="ArXiv Text", co_auteurs=["Co-Auteur1", "Co-Auteur2"])

# Affichage des documents
print(reddit_doc)
print(arxiv_doc)

########PRINCIPE DU TD: modéliser différents types de documents (Reddit et Arxiv) avec des attributs spécifiques à chaque type, de les ajouter à un corpus, et d'afficher les détails de ces documents.############