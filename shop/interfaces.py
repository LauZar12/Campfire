from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from .models import Game

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os

class ReceiptGenerator(ABC):
    @abstractmethod
    def generate_receipt(user: User, games: list[Game], id: int) -> str:
        pass


class PDFReceiptGenerator(ReceiptGenerator):
    def generate_receipt(user: User, games: list[Game], id: int) -> str:
        file_path = os.path.join(settings.MEDIA_ROOT, f'receipts/receipt_{user.username}{id}.pdf')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        c = canvas.Canvas(file_path, pagesize=A4)
        c.drawString(100, 800, f"Receipt for Order #{user.username}{id}")
        c.drawString(100, 780, "--------------------------------")
        c.drawString(100, 760, "Item Name        Price")
        
        y_position = 740
        total_price = 0
        
        for game in games:
            c.drawString(100, y_position, f"{game.title}          ${game.price}")
            total_price += game.price
            y_position -= 20

        c.drawString(100, y_position - 20, "--------------------------------")
        c.drawString(100, y_position - 40, f"Total: ${total_price:.2f}")
        
        c.save()
        return file_path

class TextReceiptGenerator(ReceiptGenerator):
    def generate_receipt(user: User, games: list[Game], id: int) -> str:
        file_path = os.path.join(settings.MEDIA_ROOT, f'receipts/receipt_{user.username}{id}.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        receipt_content = f"Receipt for Order #{user.username}{id}\n"
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
