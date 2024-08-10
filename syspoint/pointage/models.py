from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.db import migrations, models
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import json
import logging




class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)  
    mot_de_passe = models.CharField(max_length=50)


    import logging

logger = logging.getLogger(__name__)

class Etudiant(models.Model):
    # ... autres champs ...
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_etudiant = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True )


    def save(self, *args, **kwargs):
        logger.info(f"Début de la génération du QR code pour l'étudiant {self.numero_etudiant}")
        qrcode_img = qrcode.make(self.numero_etudiant)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.numero_etudiant}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        logger.info(f"QR code généré avec succès pour l'étudiant {self.numero_etudiant}")
        super().save(*args, **kwargs)



class Pointage(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True )


    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.etudiant)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.etudiant}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
        
        

class forward_func:
        

    def forward_func(apps, schema_editor):
        Pointage = apps.get_model('pointage', 'Pointage')
        Etudiant = apps.get_model('pointage', 'Etudiant')
    
    # Créez un étudiant par défaut si nécessaire
        etudiant_par_defaut, _ = Etudiant.objects.get_or_create(nom="Par défaut", prenom="Étudiant")
    
    # Mettez à jour tous les pointages avec un étudiant null
        Pointage.objects.filter(etudiant__isnull=True).update(etudiant=etudiant_par_defaut)

class Migration(migrations.Migration):

    dependencies = [
        ('pointage', 'previous_migration'),
    ]

    operations = [
        migrations.RunPython(forward_func),
    ]

class Migration(migrations.Migration):

    dependencies = [
        ('pointage', 'previous_custom_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointage',
            name='etudiant',
            field=models.ForeignKey(to='Etudiant', on_delete=models.CASCADE),
        ),
    ]


    

