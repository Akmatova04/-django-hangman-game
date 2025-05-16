"""
URL configuration for hangman_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# hangman_project/urls.py
from django.contrib import admin
from django.urls import path, include # include функциясын кошууну унутпаңыз
# from wordgame.views import hangman_view # Эгер башкы бетти оюнга багыттагыңыз келсе

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hangman/', include('wordgame.urls')), # Биздин wordgame тиркемесинин URL'дарын кошобуз
    
    # Мисалы, башкы бетти түздөн-түз оюнга багыттоо үчүн:
    # path('', hangman_view, name='home_page_hangman'),
    # Же болбосо, эгер оюнга /hangman/play/ аркылуу кирүүнү кааласаңыз, муну кошпой эле коюңуз.
]