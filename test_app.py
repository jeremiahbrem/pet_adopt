from unittest import TestCase

from app import app
from models import db, Pet
from forms import AddPetForm

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_adopt'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    """Tests views for Pet."""

    def setUp(self):
        """Add sample Pet."""

        db.create_all()
        pet = Pet(name="Frito", species="cat", age=4, notes="So sweet")
        db.session.add(pet)
        db.session.commit()
        self.pet = pet

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        db.drop_all()

    def test_show_pet_list(self):
        """Testing if available pet list shows"""

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Available Pets", html)
            self.assertIn("Frito</a> <b>is available</b>", html)
            self.assertIn(self.pet.name, html)

    def test_show_add_form_get(self):
        """Testing if add pet form page displays"""

        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add Pet", html)
    
    def test_show_add_form_post(self):
        """Testing if add pet form page displays"""

        with app.test_client() as client:
            d = {"name": "Gracie", "species": "dog", "age": 5}
            resp = client.post("/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Gracie</a> <b>is available</b>", html)

    def test_show_pet_details(self):
        """Testing if pet details page displays"""

        with app.test_client() as client:
            resp = client.get(f"/{self.pet.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.pet.name, html)

    def test_edit_pet(self):
        """Testing if pet is correctly edited"""

        with app.test_client() as client:
            d = {"notes": "Now he's mean", "available": "false"}
            resp = client.post(F"/{self.pet.id}", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Frito updated", html)
            self.assertEqual(self.pet.available, False)
            self.assertEqual(self.pet.notes, "Now he's mean")

    def test_unavailable_list(self):
        """Testing if unavailable pet shows in correct list on pet list"""

        with app.test_client() as client:
            self.pet.available = False
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Frito</a> <b>is not available</b>", html)       

