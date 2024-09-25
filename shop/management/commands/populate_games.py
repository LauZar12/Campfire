import random
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Game, Category, GameCategories


class Command(BaseCommand):
    help = 'Populate the database with random data for Game, Category, and GameCategories models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        categories = []
        for _ in range(20):
            category = Category.objects.create(
                name=fake.word(),
                desciption=fake.sentence()
            )
            categories.append(category)

        games = []
        for _ in range(100):
            game = Game.objects.create(
                title=fake.sentence(nb_words=3),
                author=fake.name(),
                price=random.randint(1000, 20000),
                description=fake.text()
            )
            games.append(game)

        for game in games:
            selected_categories = random.sample(
                categories, random.randint(1, 3))
            for category in selected_categories:
                GameCategories.objects.create(
                    game=game,
                    category=category
                )

        self.stdout.write(self.style.SUCCESS(
            'Random data has been inserted successfully!'))
