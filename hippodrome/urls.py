from django.urls import path
from . import views  # Importation des vues définies dans le fichier views.py

# Définition d'un espace de noms pour l'application
# Cela permet de différencier les URLs de cette application des autres dans le projet
app_name = 'hippodrome'

# Déclaration des routes URL et association aux vues correspondantes
urlpatterns = [
    # Page d'accueil : redirige vers la liste des chevaux
    path('', views.cheval_list, name='index'),

    # URL pour afficher la liste des jockeys
    path('jockeys/', views.jockey_list, name='jockey_list'),

    # URL pour ajouter un jockey
    path('jockeys/add/', views.add_jockey, name='add_jockey'),

    # URL pour afficher la liste des chevaux
    path('chevaux/', views.cheval_list, name='cheval_list'),

    # URL pour ajouter un cheval
    path('chevaux/add/', views.add_cheval, name='add_cheval'),

    # URL pour afficher les détails d'un cheval spécifique
    # `cheval_id` est un paramètre qui correspond à l'identifiant du cheval
    path('chevaux/<int:cheval_id>/', views.cheval_detail, name='cheval_detail'),

    # URL pour supprimer un cheval
    # Utilisation d'une vue générique basée sur une classe (DeleteView)
    # `pk` est utilisé pour récupérer l'identifiant principal (primary key)
    path('chevaux-delete/<int:pk>', views.ChevalDeleteView.as_view(), name='chevaux_delete'),

    # URL pour afficher la liste des courses
    path('courses/', views.course_list, name='course_list'),

    # URL pour ajouter une nouvelle course
    path('courses/add/', views.add_course, name='add_course'),

    # URL pour afficher les détails d'une course spécifique
    # `course_id` correspond à l'identifiant de la course
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    # URL pour supprimer un jockey
    # Utilisation d'une vue générique basée sur une classe (DeleteView)
    path('jockeys-delete/<int:pk>', views.JockeyDeleteView.as_view(), name='jockeys_delete'),

    # URL pour mettre à jour un jockey
    # Utilisation d'une vue générique basée sur une classe (UpdateView)
    path('jockeys-update/<int:pk>', views.JockeyUpdateView.as_view(), name='jockeys_update'),

    path('ecuries/', views.stable_list, name='ecurie_list'),
    path('ecuries/add/', views.add_stable, name='add_ecurse'),
    path('zones/', views.zone_list, name='zone_list'),
    path('zones/add/', views.add_zone, name='add_zone'),
    path('zones/<int:zone_id>/', views.zone_detail, name='zone_detail'),

    #Admin
    path('gestion/chevaux/', views.cheval_admin_list, name='cheval_admin_list'),

    path('chevaux/<int:cheval_id>/assign-zone/', views.assign_cheval_to_zone, name='assign_cheval_to_zone'),
    path('chevaux/<int:cheval_id>/assign-ecurie/', views.assign_cheval_to_ecurie, name='assign_cheval_to_ecurie'),

]
