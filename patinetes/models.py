from django.db import models
# Create your models here.

class Patinete (models.Model):
    numero = models.IntegerField()
    tipo = models.CharField(max_length=100)
    precio_desbloqueo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    precio_minuto = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return f"{self.numero} - {self.tipo}"
    class Meta:
        verbose_name_plural = "Patinetes"


class Usuario (models.Model):
    debito = models.CharField(max_length=20,default=0)
    def __str__(self):
        return f"{self.debito}"
    class Meta:
        verbose_name_plural = "Usuarios"

class Alquiler(models.Model):

    usuario = models.ForeignKey(Usuario, models.CASCADE)
    patinete = models.ForeignKey(Patinete, models.CASCADE)
    fecha_desbloqueo = models.DateField()
    fecha_entrega = models.DateField()
    coste_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def __str__(self):
        return f"{self.usuario} - {self.patinete} - {self.fecha_entrega}"

    class Meta:
        verbose_name_plural = "Alquileres"


