from django.shortcuts import render
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import SignUpForm
from django.urls import reverse_lazy
from .models import Game


# =========================HOME=========================
class Home(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================LOGIN=========================
class Login(LoginView):
    template_name = 'login.html'


class Logout(LogoutView):
    template_name = 'logout.html'


# =========================SIGNUP=========================
class Signup(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        # Log in the user immediately after registration
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


# =========================GAMES=========================
class Games(LoginRequiredMixin, View):
    template_name = "games.html"

    def get(self, request):
        games = Game.objects.all()
        return render(request, self.template_name, {
                      'games': games,
                      })


# =========================GAME=========================
class GameView(LoginRequiredMixin, View):
    template_name = "game.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================CART=========================
class Cart(LoginRequiredMixin, View):
    template_name = "cart.html"

    def get(self, request):
        return render(request, self.template_name, {})


# =========================ACCOUNT=========================
class Account(LoginRequiredMixin, View):
    template_name = "account.html"

    def get(self, request):
        return render(request, self.template_name, {})
