from django.contrib import admin
from .models import Game, Category, Stock, GameCategories, GameOwner, Review


# Register your models here
admin.site.register(Game)
admin.site.register(GameOwner)
admin.site.register(GameCategories)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Review)
