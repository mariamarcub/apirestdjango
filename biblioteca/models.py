from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Crea dos modelos: uno para los libros y otro para los usuarios de la biblioteca.
# El modelo de libro debe incluir campos como título, autor, género,
# año de publicación, etc.
# El modelo de usuario debe contener información básica como nombre, apellido,
# correo electrónico, etc.




class Usuario (models.Model):

    TIPO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    genero = models.CharField(max_length=50, choices=TIPO_CHOICES)
    email = models.EmailField()
    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} - {self.user.last_name}"
    class Meta:
        verbose_name_plural = "Usuarios"


class Libro(models.Model):

    usuario = models.ForeignKey(User, models.PROTECT)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    anyo_publicacion = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.usuario.user.username}"
    class Meta:
        verbose_name_plural = "Libros"


class Alquiler(models.Model):

    libro = models.ForeignKey(Libro, models.PROTECT)
    usuario = models.ForeignKey(Usuario, models.PROTECT)
    inicio = models.DateTimeField()
    fin = models.DateTimeField(blank=True,null=True)
    def __str__(self):  # Python nos permite redefinir el método que se debe ejecutar mediante __str__(self)
        # Para que aparezca de forma legible en el Admin, porque sino, sale los ID de los objetos
        return f'{self.libro.titulo} - {self.usuario.user.username}'
    class Meta:
        verbose_name_plural = 'Alquileres'


