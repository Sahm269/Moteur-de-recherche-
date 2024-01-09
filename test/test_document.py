import unittest
from classes.Document import Document, RedditDocument, ArxivDocument, DocumentFactory

class TestDocumentClasses(unittest.TestCase):

    def test_document_repr_and_str(self):
        # Teste les méthodes __repr__ et __str__ de la classe Document
        doc = Document("Title", "Author", "2023/01/01", "URL", "Text", "Type")
        expected_repr = "Titre : Title\tAuteur : Author\tDate : 2023/01/01\tURL : URL\tTexte : Text\tType : Type\t"
        expected_str = "Title, par Author, Source : Type"
        self.assertEqual(repr(doc), expected_repr)
        self.assertEqual(str(doc), expected_str)

    def test_reddit_document(self):
        # Teste la classe RedditDocument
        reddit_doc = RedditDocument("Reddit Title", "Reddit Author", "2023/02/02", "Reddit URL", "Reddit Text", 42)
        expected_str = "Reddit Title, par Reddit Author, Source : Reddit, Nombre de commentaires : 42"
        self.assertEqual(str(reddit_doc), expected_str)
        self.assertEqual(reddit_doc.get_type(), "Reddit")

    def test_arxiv_document(self):
        # Teste la classe ArxivDocument
        arxiv_doc = ArxivDocument("Arxiv Title", ["Author1", "Author2"], "2023/03/03", "Arxiv URL", "Arxiv Text", ["CoAuthor1", "CoAuthor2"])
        expected_str = "Arxiv Title, par ['Author1', 'Author2'], Source : Arxiv, Co-auteurs : CoAuthor1, CoAuthor2"
        self.assertEqual(str(arxiv_doc), expected_str)
        self.assertEqual(arxiv_doc.get_type(), "Arxiv")

    def test_document_factory(self):
        # Teste la classe DocumentFactory
        factory = DocumentFactory()

        # Crée un document Reddit
        reddit_kwargs = {
            "titre": "Reddit Title",
            "auteur": "Reddit Author",
            "date": "2023/02/02",
            "url": "Reddit URL",
            "texte": "Reddit Text",
            "num_comments": 42
        }
        reddit_doc = factory.create_document("Reddit", **reddit_kwargs)
        self.assertIsInstance(reddit_doc, RedditDocument)
        self.assertEqual(reddit_doc.get_type(), "Reddit")

        # Crée un document Arxiv
        arxiv_kwargs = {
            "titre": "Arxiv Title",
            "auteurs": ["Author1", "Author2"],
            "date": "2023/03/03",
            "url": "Arxiv URL",
            "texte": "Arxiv Text",
            "co_auteurs": ["CoAuthor1", "CoAuthor2"]
        }
        arxiv_doc = factory.create_document("Arxiv", **arxiv_kwargs)
        self.assertIsInstance(arxiv_doc, ArxivDocument)
        self.assertEqual(arxiv_doc.get_type(), "Arxiv")

        # Teste un type de document inconnu
        with self.assertRaises(ValueError):
            unknown_doc = factory.create_document("UnknownType", titre="Unknown Title")

if __name__ == '__main__':
    unittest.main()
