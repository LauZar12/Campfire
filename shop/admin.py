from django.contrib import admin
from .models import Game, Category, Stock, GameCategories


# Register your models here
admin.site.register(Game)
admin.site.register(GameCategories)
admin.site.register(Category)
admin.site.register(Stock)
