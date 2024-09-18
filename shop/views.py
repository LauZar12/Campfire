from django.shortcuts import render
from django.views.generic import View


# =========================HOME=========================
class Home(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================LOGIN=========================
class Login(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================SIGNUP=========================
class Signup(View):
    template_name = "signup.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================GAMES=========================
class Games(View):
    template_name = "games.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================GAME=========================
class Game(View):
    template_name = "game.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================CART=========================
class Cart(View):
    template_name = "cart.html"

    def get(self, request):
        return render(request, self.template_name, {})
