# Generated by Django 4.2 on 2024-10-29 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activite', '0001_initial'),
        ('reservations', '0003_remove_reservation_admin_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='activite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='activite.activite'),
        ),
    ]
