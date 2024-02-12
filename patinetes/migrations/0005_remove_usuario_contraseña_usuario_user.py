# Generated by Django 4.1.13 on 2024-02-12 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patinetes', '0004_usuario_contraseña'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='contraseña',
        ),
        migrations.AddField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
