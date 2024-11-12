# Miguel Angel Cock Cano
from django.db import models
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os


# ========== GAME ==========
class Game(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"GAME: {self.title}"


class Stock(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"STOCK: {self.game.title} {self.quantity}"


# ========== CART ==========
class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_carts')

    def __str__(self):
        return f"SHOPPING_CART: {self.user.username}"


class CartItem(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CART_ITEM: {self.game.title} {self.quantity}"


# ========== CATEGORIES ==========
class Category(models.Model):
    name = models.CharField(max_length=255)
    desciption = models.CharField(max_length=255)

    def __str__(self):
        return f"CATEGORY: {self.name}"


class GameCategories(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='game_categories')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='game_categories')

    def __str__(self):
        return f"GAME_CATEGORY: {self.game.title} {self.category.name}"


# ========== USER/GAME INTERACTIONS =========
class GameOwner(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='game_owner')
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='game_owner')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"GAME_OWNER: {self.user.username} {self.game.title}"


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='review')
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(
        default=1, choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"REVIEW: {self.user.username} {self.game.title}"


# ========== Wallet ==========
class Wallet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.IntegerField(default=0)


class Receipt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_receipt')

    def generate_receipt(self, games: list[Game]):
        # Define file path
        file_path = os.path.join(settings.MEDIA_ROOT, f'receipts/receipt_{self.user.username}{self.id}.pdf')
    
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        c = canvas.Canvas(file_path, pagesize=A4)
        
        # Receipt content (example)
        c.drawString(100, 800, f"Receipt for Order #{self.user.username}")
        c.drawString(100, 780, "--------------------------------")
        c.drawString(100, 760, "Item Name        Price")
        
        y_position = 740
        total_price = 0
        
        # List items
        for game in games:
            c.drawString(100, y_position, f"{game.title}          ${game.price}")
            total_price += game.price
            y_position -= 20

        # Add total price
        c.drawString(100, y_position - 20, "--------------------------------")
        c.drawString(100, y_position - 40, f"Total: ${total_price:.2f}")
        
        # Save the PDF
        c.save() 