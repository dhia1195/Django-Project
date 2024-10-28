from django.test import TestCase
from .models import Fournisseur

class FournisseurModelTest(TestCase):

    def setUp(self):
        # Créer un fournisseur pour les tests
        self.fournisseur = Fournisseur.objects.create(
            nom='Hotel Example',
            email='contact@example.com',
            telephone='123456789',
            adresse='123 Example St',
            evaluation=4.5
        )

    def test_fournisseur_creation(self):
        # Vérifiez que l'objet fournisseur a été créé correctement
        self.assertEqual(self.fournisseur.nom, 'Hotel Example')
        self.assertEqual(self.fournisseur.email, 'contact@example.com')
        self.assertEqual(self.fournisseur.telephone, '123456789')
        self.assertEqual(self.fournisseur.adresse, '123 Example St')
        self.assertEqual(self.fournisseur.evaluation, 4.5)

    def test_str_method(self):
        # Vérifiez que la méthode __str__ renvoie le bon nom
        self.assertEqual(str(self.fournisseur), 'Hotel Example')
