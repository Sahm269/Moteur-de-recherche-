
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
    
    def get_type(self):
        return "Reddit"

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

        
        def get_type(self):
            return "Arxiv"

        # Méthode spécifique pour afficher l'objet ArxivDocument
        def __str__(self):
            return f"{super().__str__()}, Co-auteurs : {', '.join(self.co_auteurs)}"
        
   



### ========================== Generateur de document ============
class DocumentFactory:
    def create_document(self, document_type, **kwargs):
        if document_type == "Reddit":
            return RedditDocument(**kwargs)
        elif document_type == "Arxiv":
            return ArxivDocument(**kwargs)
        else:
            raise ValueError(f"Type de document inconnu : {document_type}")


