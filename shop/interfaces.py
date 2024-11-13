from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os

class ReceiptGenerator(ABC):
    @abstractmethod
    def generate_receipt(user: User, games: list, id: int) -> str:
        """Generate a receipt in some format"""
        pass

class PDFReceiptGenerator(ReceiptGenerator):
    def generate_receipt(user: User, games: list, id: int) -> str:
        file_path = os.path.join(settings.MEDIA_ROOT, f'receipts/receipt_{user.username}{id}.pdf')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        c = canvas.Canvas(file_path, pagesize=A4)
        self._draw_header(c, user, id)
        
        y_position = 740
        total_price = 0
        for game in games:
            self._draw_game_details(c, game, y_position)
            total_price += game.price
            y_position -= 20

        self._draw_footer(c, total_price, y_position)
        c.save()
        return file_path

class TextReceiptGenerator(ReceiptGenerator):
    def generate_receipt(user: User, games: list, id: int) -> str:
        file_path = os.path.join(settings.MEDIA_ROOT, f'receipts/receipt_{user.username}{id}.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        receipt_content = f"Receipt for Order #{id}\n"
        receipt_content += "--------------------------------\n"
        receipt_content += "Item Name        Price\n"
        
        total_price = 0
        for game in games:
            receipt_content += f"{game.title}          ${game.price}\n"
            total_price += game.price

        receipt_content += "--------------------------------\n"
        receipt_content += f"Total: ${total_price:.2f}\n"
        
        with open(file_path, 'w') as file:
            file.write(receipt_content)

        return file_path
