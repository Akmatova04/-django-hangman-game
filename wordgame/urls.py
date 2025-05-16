# wordgame/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Оюндун негизги барагы
    path('play/', views.hangman_view, name='hangman_play'),
    
    # Жаңы оюн баштоо үчүн URL
    path('new/', views.new_hangman_game_view, name='hangman_new_game'),
]