from django.shortcuts import render
from django.views.generic import View


# =========================HOME=========================
class Home(View):
    template_name = "home.html"


# =========================LOGIN=========================
class Login(View):
    template_name = "login.html"


# =========================SIGNUP=========================
class Signup(View):
    template_name = "signup.html"


# =========================GAMES=========================
class Games(View):
    template_name = "games.html"


# =========================GAME=========================
class Game(View):
    template_name = "game.html"


# =========================CART=========================
class Cart(View):
    template_name = "cart.html"

