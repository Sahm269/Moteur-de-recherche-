import unittest
from classes.Author import Author

class TestAuthorClass(unittest.TestCase):

    def test_author_creation(self):
        # Teste la création d'un auteur
        author_name = "John Doe"
        author = Author(author_name)

        # Vérifie que les attributs sont correctement initialisés
        self.assertEqual(author.name, author_name)
        self.assertEqual(author.ndoc, 0)
        self.assertEqual(author.production, [])

    def test_author_add_production(self):
        # Teste l'ajout d'une production à un auteur
        author_name = "Jane Doe"
        author = Author(author_name)

        # Crée une production fictive
        production_title = "Sample Title"
        production_type = "Article"
        production = {"title": production_title, "type": production_type}

        # Ajoute la production à l'auteur
        author.add(production)

        # Vérifie que les attributs ont été mis à jour correctement
        self.assertEqual(author.ndoc, 1)
        self.assertEqual(author.production, [production])

    def test_author_str_representation(self):
        # Teste la représentation en chaîne de caractères d'un auteur
        author_name = "Alice Wonderland"
        author = Author(author_name)

        # Vérifie que la méthode __str__ renvoie la représentation attendue
        expected_str = f"Auteur : {author_name}\t# productions : 0"
        self.assertEqual(str(author), expected_str)

if __name__ == '__main__':
    unittest.main()
