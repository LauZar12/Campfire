# Miguel Angel Cock Cano
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import SignUpForm
from django.urls import reverse_lazy
from .models import Game, ShoppingCart, CartItem, GameOwner, Review, Wallet, Receipt

# REST
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import GamesSerializer


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
    # Redirect to login page after successful registration
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Log in the user immediately after registration
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


# =========================GAMES=========================
class Games(LoginRequiredMixin, View):
    template_name = "games.html"

    def get(self, request):
        sort_by_price = request.GET.get('sort_by_price', None)

        if sort_by_price == 'asc':
            games = Game.objects.all().order_by('price')  # Sort ascending
        elif sort_by_price == 'desc':
            games = Game.objects.all().order_by('-price')  # Sort descending
        else:
            games = Game.objects.all()

        return render(request, self.template_name, {
            'games': games,
        })

    def post(self, request):
        if 'game_id' in request.POST:
            game_id = request.POST.get('game_id')
            game = get_object_or_404(Game, id=game_id)
            shopping_cart, created = ShoppingCart.objects.get_or_create(
                user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                shopping_cart=shopping_cart, game=game)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('games')
        elif 'search' in request.POST:
            search_term = request.POST.get('search')
            games = Game.objects.filter(title__icontains=search_term)

            return render(request, self.template_name, {
                'games': games,
            })


# =========================GAME=========================
class GameView(LoginRequiredMixin, View):
    template_name = "game.html"

    def get(self, request):
        game_id = request.GET.get('game_id')
        game = get_object_or_404(Game, id=game_id)

        if 'sort_by' in request.GET:
            reviews = Review.objects.filter(game=game).order_by('-rating')
        else:
            reviews = Review.objects.filter(game=game)

        categories = game.game_categories.all()
        category_names = [category.category.name for category in categories]

        return render(request, self.template_name, {
            'game': game,
            'reviews': reviews,
            'categories': category_names,
        })

    def post(self, request):
        game_id = request.POST.get('game_id')
        game = get_object_or_404(Game, id=game_id)

        if 'comment' in request.POST and 'rating' in request.POST:
            comment = request.POST.get('comment')
            rating = request.POST.get('rating')

            Review.objects.create(
                user=request.user, game=game, comment=comment, rating=rating)

        reviews = Review.objects.filter(game=game)

        categories = game.game_categories.all()
        category_names = [category.category.name for category in categories]

        return render(request, self.template_name, {
            'game': game,
            'reviews': reviews,
            'categories': category_names,
        })


# =========================CART=========================
class Cart(LoginRequiredMixin, View):
    template_name = "cart.html"

    def get(self, request):
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            user=request.user)
        cart_items = shopping_cart.cart_items.all()
        return render(request, self.template_name, {'cart_items': cart_items})

    def post(self, request):

        games_id = request.POST.getlist('game_id')

        shopping_cart, created = ShoppingCart.objects.get_or_create(
            user=request.user)
        
        games = []

        wallet, create = Wallet.objects.get_or_create(user=request.user)

        for game_id in games_id:

            game = get_object_or_404(Game, id=game_id)

            if wallet.balance - game.price >= 0: 
                game_owner, created = GameOwner.objects.get_or_create(
                    game=game, user=request.user)
                if created:
                    game_owner.save()
                wallet.balance -= game.price
                wallet.save()

                games.append(game)

                shopping_cart.cart_items.get(game=game).delete()
        
        receipt = Receipt.objects.create(wallet=wallet)
        receipt.save()
        receipt.generate_receipt(games)

        return redirect('cart')


# =========================ACCOUNT=========================
class Account(LoginRequiredMixin, View):
    template_name = "account.html"

    def get(self, request):
        owned_games = GameOwner.objects.filter(user=request.user)
        wallet, created = Wallet.objects.get_or_create(user=request.user)

        if 'sort_by_name' in request.GET:
            owned_games = owned_games.select_related(
                'game').order_by('game__title')

        return render(request, self.template_name, {
                      'user': request.user,
                      'owned_games': owned_games,
                      "wallet": wallet,
                      })
    
    def post(self, request):
        balance = int(request.POST.get('balance', 0))
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += balance
        wallet.save()

        return redirect('account')


# =========================REST=========================
class GamesRest(APIView):
    def get(self, request):
        books = Game.objects.all()
        serializer = GamesSerializer(books, many=True)
        return Response(serializer.data)