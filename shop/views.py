from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import SignUpForm
from django.urls import reverse_lazy
from .models import Game, ShoppingCart, CartItem, GameOwner


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

    def post(self, request):
        game_id = request.POST.get('game_id')
        game = get_object_or_404(Game, id=game_id)
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(shopping_cart=shopping_cart, game=game)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('games')


# =========================GAME=========================
class GameView(LoginRequiredMixin, View):
    template_name = "game.html"

    def post(self, request):
        id = request.POST.get('game_id')
        game = get_object_or_404(Game, id=id)
        return render(request, self.template_name, {'game': game})


# =========================CART=========================
class Cart(LoginRequiredMixin, View):
    template_name = "cart.html"

    def get(self, request):
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_items = shopping_cart.cart_items.all()
        return render(request, self.template_name, {'cart_items': cart_items})

    def post(self, request):

        games_id = request.POST.getlist('game_id')

        shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)

        for game_id in games_id:
            game = get_object_or_404(Game, id=game_id)
            GameOwner.objects.create(user=request.user, game=game)

        shopping_cart.cart_items.all().delete()

        return redirect('cart')


# =========================ACCOUNT=========================
class Account(LoginRequiredMixin, View):
    template_name = "account.html"

    def get(self, request):
        owned_games = GameOwner.objects.filter(user=request.user)
        return render(request, self.template_name, {'owned_games': owned_games})
