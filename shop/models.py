from django.db import models
from django.contrib.auth.models import User


# ========== GAME ==========
class Game(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()


class Stock(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=1)


# ========== CART ==========
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_carts')


class CartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)


# ========== CATEGORIES ==========
class Category(models.Model):
    name = models.CharField(max_length=255)
    desciption = models.CharField(max_length=255)


class GameCategories(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='game_categories')


# ========== USER/GAME INTERACTIONS =========
class GameOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_owner')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_owner')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='review')
    comment = models.CharField(max_length=255)
