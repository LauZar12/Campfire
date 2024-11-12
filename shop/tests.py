from django.test import TestCase
from django.urls import reverse
from .models import Game
from django.contrib.auth.models import User

# Create your tests here.
class GameTest(TestCase):
    def setUp(self):
        Game.objects.create(
            title='bluelabel',
            author='labelblue',
            price=10500,
            description='el blue label es un elizir'
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

    # test 1
    def test_game_creation(self):
        game = Game.objects.get(title='bluelabel')
        self.assertEqual(game.author, 'labelblue')
        self.assertEqual(str(game), "GAME: bluelabel")
    
    # test 2
    def test_game_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bluelabel")