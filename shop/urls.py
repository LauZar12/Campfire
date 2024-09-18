from django.urls import path
from .views import Home, Login, Signup, Games, Game,Cart

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('games/', Games.as_view(), name='games'),
    path('game/', Game.as_view(), name='game'),
    path('cart/', Cart.as_view(), name='cart'),
]
