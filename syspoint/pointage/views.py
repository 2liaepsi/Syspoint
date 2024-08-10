from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pointage
import json
from .models import Etudiant
import logging
from .models import Pointage
from django.utils import timezone
from .models import Pointage, Etudiant
from django.views.decorators.csrf import csrf_exempt
from .models import Pointage, Etudiant
from django.core.exceptions import ObjectDoesNotExist



# Reste de votre code...



# def conn(request):
#     return render(request, 'connexion.html')

# def insc(request):
#     return render(request, 'inscription.html')

def dash(request):
    return render(request, 'dashbord.html')

def add(request):
    return render(request, 'ajout_classe.html')

def point(request):
    return render(request, 'ajout_pointage.html')




# Create your views here.
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

@login_required
def acceuil(request):
    return render(request, 'dashbord.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')



logger = logging.getLogger(__name__)

@csrf_exempt
def enregistrer_pointage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etudiant_id = data.get('etudiantId')
            
            print(f"Tentative de pointage pour l'étudiant ID: {etudiant_id}")
            
            if not etudiant_id:
                print("etudiantId manquant")
                return JsonResponse({'error': 'etudiantId manquant'}, status=400)
            
            try:
                etudiant = Etudiant.objects.get(numero_etudiant=etudiant_id)
                pointage = Pointage.objects.create(etudiant=etudiant)
                print(f"Pointage créé avec succès pour l'étudiant {etudiant.nom}")
                return JsonResponse({'message': 'Pointage enregistré', 'id': pointage.id}, status=201)
            except Etudiant.DoesNotExist:
                print(f"Étudiant non trouvé pour l'ID: {etudiant_id}")
                return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)
        
        except json.JSONDecodeError:
            print("JSON invalide reçu")
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du pointage : {str(e)}")
            return JsonResponse({'error': "Erreur lors de l'enregistrement du pointage"}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
def obtenir_pointages(request):
    pointages = Pointage.objects.order_by('-timestamp')[:5]
    
    data = [{'etuduiant_id': p.etudiant_id, 'timestamp': p.timestamp} for p in pointages]
    return JsonResponse(data, safe=False)


def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'liste_etudiants.html', {'etudiants': etudiants})





def liste_pointage(request):
    aujourd_hui = timezone.now().date()
    pointages = Pointage.objects.filter(timestamp__date=aujourd_hui).order_by('-timestamp')
    return render(request, 'liste_pointage.html', {'pointages': pointages})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Etudiant, Pointage
from django.contrib import messages

@login_required
def pointage_responsable(request):
    if request.method == 'POST':
        numero_etudiant = request.POST.get('numero_etudiant')
        try:
            etudiant = Etudiant.objects.get(numero_etudiant=numero_etudiant)
            Pointage.objects.create(etudiant=etudiant)
            messages.success(request, f"Pointage enregistré pour {etudiant.nom} {etudiant.prenom}")
        except Etudiant.DoesNotExist:
            messages.error(request, "Étudiant non trouvé")
        return redirect('pointage_responsable')

    aujourd_hui = timezone.now().date()
    pointages_du_jour = Pointage.objects.filter(timestamp__date=aujourd_hui).order_by('-timestamp')
    return render(request, 'pointage_responsable.html', {'pointages': pointages_du_jour})

