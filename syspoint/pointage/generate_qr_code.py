from django.core.management.base import BaseCommand
from pointage.models import Etudiant
from pointage.views import generate_qr_code

class Command(BaseCommand):
    help = 'Génère des QR codes pour les étudiants qui n\'en ont pas'

    def handle(self, *args, **kwargs):
        etudiants = Etudiant.objects.filter(qr_code__isnull=True)
        for etudiant in etudiants:
            generate_qr_code(etudiant)
            etudiant.save()
            self.stdout.write(self.style.SUCCESS(f'QR code généré pour {etudiant.nom} {etudiant.prenom}'))
