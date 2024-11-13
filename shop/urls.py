# Miguel Angel Cock Cano
from django.urls import path
from .views import Home, Login, Logout, Signup, Games, GameView, Cart, Account, GamesRest, productos_aliados

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', Signup.as_view(), name='signup'),
    path('games/', Games.as_view(), name='games'),
    path('game/', GameView.as_view(), name='game'),
    path('cart/', Cart.as_view(), name='cart'),
    path('account/', Account.as_view(), name='account'),

    path('gamesAPI/', GamesRest.as_view(), name=''),
    path('productos-aliados/', productos_aliados.as_view(), name='productos_aliados')
]
