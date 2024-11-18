from lib2to3.fixes.fix_input import context
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from .models import Jockey, Cheval, Course, Ecurie, Zone
from .forms import JockeyForm, ChevalForm, CourseForm, EcurieForm, ZoneForm


# Affiche la page d'accueil
def index(request):
    return render(request, "base.html")

# Liste tous les jockeys dans la base de données
def jockey_list(request):
    jockeys = Jockey.objects.all()  # Récupère tous les jockeys
    return render(request, 'hippodrome/jockey_list.html', {'jockeys': jockeys})  # Passe les jockeys au template

# Permet d'ajouter un nouveau jockey
def add_jockey(request):
    message = ''  # Message par défaut, vide
    if request.method == 'POST':  # Si le formulaire est soumis
        form = JockeyForm(request.POST, request.FILES)  # Instancie le formulaire avec les données soumises
        if form.is_valid():  # Vérifie si le formulaire est valide
            form.save()  # Sauvegarde l'objet dans la base de données
            return redirect('hippodrome:jockey_list')  # Redirige vers la liste des jockeys
        else:
            message = "Une erreur s'est produite. Veuillez vérifier les champs et réessayer."  # Message d'erreur
    else:  # Si la méthode n'est pas POST, afficher un formulaire vide
        form = JockeyForm()
    return render(request, 'hippodrome/add_jockey.html', {'form': form, 'message': message})  # Affiche le formulaire et le message

# Liste tous les chevaux
def cheval_list(request):
    # Récupère la valeur du filtre "unassigned" depuis les paramètres GET
    show_unassigned = request.GET.get('unassigned', 'false') == 'true'

    # Filtre les chevaux selon le statut du filtre
    if show_unassigned:
        chevaux = Cheval.objects.filter(jockey__isnull=True)  # Chevaux sans jockey
    else:
        chevaux = Cheval.objects.all()  # Tous les chevaux

    # Ajout de la pagination (8 chevaux par page)
    paginator = Paginator(chevaux, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexte envoyé au template
    context = {
        'object_list': page_obj,  # Liste des chevaux paginée
        'is_paginated': page_obj.has_other_pages(),  # Indique si la pagination est active
        'paginator': paginator,  # Objet de pagination
        'page_obj': page_obj,  # Objet représentant la page actuelle
        'show_unassigned': show_unassigned,  # Indique si le filtre "unassigned" est activé
    }

    return render(request, 'hippodrome/cheval_list.html', context)
# Permet d'ajouter un nouveau cheval
def add_cheval(request):
    message = ''  # Message par défaut, vide
    if request.method == 'POST':  # Si le formulaire est soumis
        form = ChevalForm(request.POST, request.FILES)  # Instancie le formulaire avec les données soumises
        if form.is_valid():  # Vérifie si le formulaire est valide
            form.save()  # Sauvegarde l'objet dans la base de données
            return redirect('hippodrome:cheval_admin_list')  # Redirige vers la liste des chevaux
        else:
            message = "Une erreur s'est produite. Veuillez vérifier les champs et réessayer."  # Message d'erreur
    else:  # Si la méthode n'est pas POST, afficher un formulaire vide
        form = ChevalForm()
    return render(request, 'hippodrome/add_cheval.html', {'form': form, 'message': message})  # Affiche le formulaire et le message

# Affiche les détails d'un cheval spécifique
def cheval_detail(request, cheval_id):
    cheval = get_object_or_404(Cheval, id=cheval_id)  # Récupère un cheval par son ID ou renvoie une erreur 404
    return render(request, 'hippodrome/cheval_detail.html', {'cheval': cheval})  # Passe le cheval au template

# Supprime un cheval (vue générique)
class ChevalDeleteView(DeleteView):
    model = Cheval  # Modèle associé à cette vue
    template_name = 'hippodrome/admin/cheval_list.html'  # Template à utiliser après la suppression
    success_url = reverse_lazy('hippodrome:cheval_admin_list')  # URL de redirection après succès

# Liste toutes les courses
def course_list(request):
    courses = Course.objects.all()  # Récupère toutes les courses
    return render(request, 'hippodrome/course_list.html', {'courses': courses})  # Passe les courses au template

# Affiche les détails d'une course spécifique
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Récupère une course par son ID ou renvoie une erreur 404
    return render(request, 'hippodrome/course_detail.html', {'course': course})  # Passe la course au template

# Permet d'ajouter une nouvelle course
def add_course(request):
    message = ''  # Message par défaut, vide
    if request.method == 'POST':  # Si le formulaire est soumis
        form = CourseForm(request.POST)  # Instancie le formulaire avec les données soumises
        if form.is_valid():  # Vérifie si le formulaire est valide
            form.save()  # Sauvegarde l'objet dans la base de données
            return redirect('hippodrome:course_list')  # Redirige vers la liste des courses
        else:
            message = "Une erreur s'est produite. Veuillez vérifier les champs et réessayer."  # Message d'erreur
    else:  # Si la méthode n'est pas POST, afficher un formulaire vide
        form = CourseForm()
    return render(request, 'hippodrome/add_course.html', {'form': form, 'message': message})  # Affiche le formulaire et le message

# Supprime un jockey (vue générique)
class JockeyDeleteView(DeleteView):
    model = Jockey  # Modèle associé à cette vue
    template_name = 'hippodrome/jockey_list.html'  # Template à utiliser après la suppression
    success_url = reverse_lazy('hippodrome:jockey_list')  # URL de redirection après succès

# Met à jour un jockey (vue générique)
class JockeyUpdateView(UpdateView):
    model = Jockey  # Modèle associé à cette vue
    form_class = JockeyForm  # Formulaire utilisé pour mettre à jour le jockey
    template_name = 'hippodrome/edit_jockey.html'  # Template utilisé pour l'édition
    success_url = reverse_lazy('hippodrome:jockey_list')  # URL de redirection après succès


# Gestion des ecuries
def stable_list(request):
    ecuries = Ecurie.objects.all()
    return render(request, 'hippodrome/ecurie_list.html', {'object_list': ecuries})

def stable_detail(request, ecurie_id):
    ecurie = get_object_or_404(Ecurie, id=ecurie_id)
    chevaux = ecurie.chevaux.all()
    return render(request, 'hippodrome/ecurie_detail.html', {'ecurie': ecurie, 'chevaux': chevaux})

def add_stable(request):
    message = ''
    if request.method == 'POST':
        form = EcurieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Écurie ajoutée avec succès.")
            return redirect('hippodrome:ecurie_list')
    else:
        form = EcurieForm()
    return render(request, 'hippodrome/add_ecurie.html', {'form': form, 'message':message})

#Gestion des zones
def zone_list(request):
    zones = Zone.objects.all()
    return render(request, 'hippodrome/zone_list.html', {'object_list': zones})
def add_zone(request):
    message = ''
    if request.method == 'POST':
        form = ZoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hippodrome:zone_list')  # Redirection vers la liste des zones après création
        else:
            message = "Une erreur s'est produite. Veuillez vérifier les champs."
    else:
        form = ZoneForm()

    return render(request, 'hippodrome/add_zone.html', {'form': form, 'message': message})

def zone_detail(request, zone_id):
    zone = get_object_or_404(Zone, id=zone_id)  # Récupère une zone par son ID ou renvoie une erreur 404
    return render(request, 'hippodrome/zone_detail.html', {'zone': zone})  # Passe la zone au template


def cheval_admin_list(request):
    chevaux = Cheval.objects.all()  # Chevaux sans jockey


    # Ajout de la pagination (8 chevaux par page)
    paginator = Paginator(chevaux, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Contexte envoyé au template
    context = {
        'object_list': page_obj,  # Liste des chevaux paginée
        'is_paginated': page_obj.has_other_pages(),  # Indique si la pagination est active
        'paginator': paginator,  # Objet de pagination
        'page_obj': page_obj,  # Objet représentant la page actuelle
    }

    return render(request, 'hippodrome/admin/cheval_list.html', context)


def assign_cheval_to_zone(request, cheval_id):
    cheval = get_object_or_404(Cheval, id=cheval_id)
    zones = Zone.objects.all()  # Toutes les zones disponibles

    if request.method == 'POST':
        zone_id = request.POST.get('zone')
        new_zone = get_object_or_404(Zone, id=zone_id)

        # Vérifier si le cheval est déjà affecté à une autre zone
        old_zone = Zone.objects.filter(cheval=cheval).first()
        if old_zone:
            # Libérer la zone actuelle
            old_zone.cheval = None
            old_zone.save()

        # Vérifier si la nouvelle zone est disponible
        if new_zone.is_occupied():
            message = f"La zone {new_zone.name} est déjà occupée."
        else:
            # Associer le cheval à la nouvelle zone
            new_zone.cheval = cheval
            new_zone.save()
            return redirect('hippodrome:cheval_admin_list')

    return render(request, 'hippodrome/admin/assign_cheval_to_zone.html', {
        'cheval': cheval,
        'zones': zones,
        'message': locals().get('message', None),
    })

def assign_cheval_to_ecurie(request, cheval_id):
    cheval = get_object_or_404(Cheval, id=cheval_id)
    ecuries = Ecurie.objects.annotate(cheval_count=Count('chevaux'))

    if request.method == 'POST':
        ecurie_id = request.POST.get('ecurie')
        new_ecurie = get_object_or_404(Ecurie, id=ecurie_id)

        cheval_count= Cheval.objects.filter(ecurie=new_ecurie).count()

        # Vérifier si l'écurie cible a atteint son nombre maximum de chevaux
        if cheval_count >= new_ecurie.max_chevaux:
            message = f"L'écurie {new_ecurie.name} a atteint sa capacité maximale ({new_ecurie.max_chevaux} chevaux)."
        else:
            # Retirer le cheval de son ancienne écurie
            old_ecurie = cheval.ecurie
            cheval.ecurie = None
            cheval.save()

            # Assigner le cheval à la nouvelle écurie
            cheval.ecurie = new_ecurie
            cheval.save()

            # Message de succès
            return redirect('hippodrome:cheval_admin_list')

    return render(request, 'hippodrome/admin/assign_cheval_to_ecurie.html', {
        'cheval': cheval,
        'ecuries': ecuries,
        'message': locals().get('message', None),
    })

