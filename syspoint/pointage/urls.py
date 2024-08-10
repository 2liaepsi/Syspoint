from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from pointage import views

urlpatterns = [
    #path('', views.conn, name='conn'),
    #path('inscription1/', views.insc, name='insc'),
    #path('dashbord/', views.dash, name='dash'),
    path('ajout_classe/', views.add, name='add'),
    path('ajout_pointage/', views.point, name='point'),
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('pointage/', views.enregistrer_pointage, name='enregistrer_pointage'),
    path('pointages/', views.obtenir_pointages, name='obtenir_pointages'),
    path('liste-pointages/', views.liste_pointage, name='liste_pointage'),
    path('pointage-responsable/', views.pointage_responsable, name='pointage_responsable'),


]

