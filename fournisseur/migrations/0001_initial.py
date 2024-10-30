# Generated by Django 4.2 on 2024-10-25 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('type_service', models.CharField(choices=[('hotel', 'Hôtel'), ('compagnie_aerienne', 'Compagnie Aérienne'), ('activite', 'Activité')], max_length=30)),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('evaluation', models.FloatField(default=0.0)),
            ],
        ),
    ]
