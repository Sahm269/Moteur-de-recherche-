import unittest
from classes.Corpus import Corpus  
from classes.Document import Document

class TestCorpus(unittest.TestCase):

    def setUp(self):
        # Initialisation de données de test 
        pass

    def test_add_document(self):
        # Teste la méthode add pour s'assurer qu'elle ajoute correctement un document au corpus
        corpus = Corpus("TestCorpus")
        doc = Document("Test Titre", "Test Auteur", "2022-01-09", "http://example.com", "Ceci est un test.", "Type Test")
        corpus.add(doc)

        self.assertEqual(len(corpus.id2doc), 1)
        self.assertEqual(len(corpus.authors), 1)

    def test_search(self):
        # Teste la méthode search pour s'assurer qu'elle trouve correctement les passages
        corpus = Corpus("TestCorpus")
        doc1 = Document("Test Titre 1", "Test Auteur", "2022-01-09", "http://example.com", "Ceci est un test.", "Type Test")
        doc2 = Document("Test Titre 2", "Test Auteur", "2022-01-10", "http://example.com", "Un autre test.", "Type Test")
        corpus.add(doc1)
        corpus.add(doc2)

        passages = corpus.search("test")
        self.assertEqual(len(passages), 2)

    def test_nettoyer_texte(self):
        # Test de la méthode nettoyer_texte
        mon_corpus = Corpus('test')

        # Exemple en anglais avec des caractères spéciaux et des chiffres
        texte_original = "This is a test text with some special characters: @#$%^&* and numbers 1234."
        texte_nettoye = mon_corpus.nettoyer_texte(texte_original)

        # Assure  que le texte nettoyé correspond aux attentes
        self.assertEqual(texte_nettoye, "test text special characters numbers")

        # Autre exemple en anglais avec des stopwords
        texte_original_stopwords = "The quick brown fox jumps over the lazy dog."
        texte_nettoye_stopwords = mon_corpus.nettoyer_texte(texte_original_stopwords)

        # Assure  que le texte nettoyé correspond aux attentes
        self.assertEqual(texte_nettoye_stopwords, "quick brown fox jumps lazy dog")


    
if __name__ == '__main__':
    unittest.main()
