# Generated by Django 5.0.6 on 2024-07-22 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0004_alter_pointage_etudiant'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointage',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes'),
        ),
    ]
