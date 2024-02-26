from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Crea dos modelos: uno para los libros y otro para los usuarios de la biblioteca.
# El modelo de libro debe incluir campos como título, autor, género,
# año de publicación, etc.
# El modelo de usuario debe contener información básica como nombre, apellido,
# correo electrónico, etc.

class Libros(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.numero} - {self.tipo}"
    class Meta:
        verbose_name_plural = "Patinetes"


class Usuario (models.Model):
    debito = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.debito}"
    class Meta:
        verbose_name_plural = "Usuarios"


